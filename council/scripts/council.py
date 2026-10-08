#!/usr/bin/env python3
"""LLM Council runner (Phase A).

Runs one council meeting in three stages, following karpathy/llm-council:
  1. every member answers the question independently,
  2. members review the anonymized answers and rank them,
  3. a chair writes the final synthesis.

Commands:
  check                     check member commands, API keys and local servers
  new "<topic>"             create a run folder (question.md, fact-sheet.md)
  stage1 <run>              write prompts and collect independent answers
  stage2 <run>              anonymize answers and collect peer reviews
  aggregate <run>           parse FINAL RANKING lines and average the ranks
  stage3 <run> [--chair X]  build (and, if automated, run) the chair prompt
  finalize <run>            write decision-log.md and reveal the label mapping
  status <run>              show which prompts still need a response

Members of type "subagent" (Claude Code fills the answer with a subagent) and
"manual" (a person pastes an answer from a browser) are not run here: the
script writes their prompt file and waits for their response file.

Only the Python standard library is used, so it runs on a fresh Windows
install with Python 3.10+.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import random
import re
import shutil
import string
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

AUTOMATED_TYPES = {"command", "openai_compatible"}
PING_PROMPT = "Reply with exactly one word: OK"
WAITING_TYPES = {"subagent", "manual"}
DEFAULT_COUNCIL_DIR = Path(__file__).resolve().parent.parent

FACT_SHEET_TEMPLATE = """# 자료 (Fact Sheet)

<!-- 규칙: 모든 항목에 출처(링크·파일·날짜)를 적는다. 출처가 없는 내용은 [추론]으로 표시한다. -->

| # | 내용 | 출처 | 수집일 |
|---|---|---|---|
| 1 |  |  |  |

## 비고
"""


class MemberError(Exception):
    pass


# ---------------------------------------------------------------- files


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_json(path: Path, default=None):
    if not path.exists():
        return default
    return json.loads(read(path))


def save_json(path: Path, data) -> None:
    write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def strip_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()


def render(template: str, **values: str) -> str:
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


# ---------------------------------------------------------------- config


class Council:
    def __init__(self, council_dir: Path):
        self.dir = council_dir
        self.config = load_json(council_dir / "members.json")
        if self.config is None:
            raise SystemExit(f"members.json not found in {council_dir}")
        self.settings = self.config.get("settings", {})
        self.members = {m["id"]: m for m in self.config["members"]}

    def prompt_template(self, name: str) -> str:
        return read(self.dir / "prompts" / f"{name}.md")

    def rubric(self, name: str) -> str:
        path = self.dir / "rubrics" / f"{name}.md"
        if not path.exists():
            raise SystemExit(f"rubric not found: {path}")
        return strip_comments(read(path))

    def active(self, stage: int, allow_paid: bool) -> list[dict]:
        result = []
        for m in self.config["members"]:
            if not m.get("enabled"):
                continue
            if m.get("paid") and not allow_paid:
                print(f"  - {m['id']}: 유료 위원이라 건너뜀 (--allow-paid 없이 실행)")
                continue
            if stage not in m.get("stages", [1, 2, 3]):
                continue
            result.append(m)
        return result


def run_meta(run: Path) -> dict:
    meta = load_json(run / ".meta.json")
    if meta is None:
        raise SystemExit(f"{run} 는 council run 폴더가 아닙니다 (.meta.json 없음)")
    return meta


# ---------------------------------------------------------------- members


def call_member(member: dict, prompt: str) -> str:
    kind = member.get("type")
    if kind == "command":
        return call_command(member, prompt)
    if kind == "openai_compatible":
        return call_openai_compatible(member, prompt)
    raise MemberError(f"{member['id']}: 자동 실행할 수 없는 유형입니다 ({kind})")


def call_command(member: dict, prompt: str) -> str:
    command = list(member["command"])
    exe = shutil.which(command[0])
    if exe is None:
        raise MemberError(f"명령을 찾을 수 없습니다: {command[0]}")
    env = os.environ.copy()
    for name in member.get("unset_env", []):
        env.pop(name, None)
    # Run in an empty folder so an agent-style CLI cannot read other
    # members' answers from the run directory.
    with tempfile.TemporaryDirectory(prefix="council-") as workdir:
        output_file = Path(workdir) / "last-message.txt"
        args = [exe] + [a.replace("{output_file}", str(output_file)) for a in command[1:]]
        try:
            proc = subprocess.run(
                args,
                input=prompt.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=workdir,
                env=env,
                timeout=member.get("timeout", 600),
            )
        except subprocess.TimeoutExpired:
            raise MemberError(f"시간 초과 ({member.get('timeout', 600)}초)")
        stdout = proc.stdout.decode("utf-8", errors="replace")
        stderr = proc.stderr.decode("utf-8", errors="replace")
        if proc.returncode != 0:
            raise MemberError(f"종료 코드 {proc.returncode}: {stderr.strip()[-800:]}")
        if member.get("output") == "file":
            if not output_file.exists():
                raise MemberError("출력 파일이 만들어지지 않았습니다")
            text = output_file.read_text(encoding="utf-8", errors="replace")
        else:
            text = stdout
    text = text.strip()
    if not text:
        raise MemberError("빈 응답")
    return text


def call_openai_compatible(member: dict, prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    key_env = member.get("api_key_env")
    if key_env:
        key = os.environ.get(key_env)
        if not key:
            raise MemberError(f"환경변수 {key_env} 가 설정되지 않았습니다")
        headers["Authorization"] = f"Bearer {key}"
    body = {"model": member["model"], "messages": [{"role": "user", "content": prompt}]}
    url = member["base_url"].rstrip("/") + "/chat/completions"
    request = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=member.get("timeout", 600)) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:800]
        raise MemberError(f"HTTP {e.code}: {detail}")
    except (urllib.error.URLError, TimeoutError) as e:
        raise MemberError(f"연결 실패: {e}")
    try:
        text = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise MemberError(f"예상과 다른 응답 형식: {str(data)[:300]}")
    if not text or not text.strip():
        raise MemberError("빈 응답")
    return text.strip()


def collect(run: Path, stage_dir: str, members: list[dict], prompts: dict[str, str], force: bool) -> list[str]:
    """Write each member's prompt; run automated members; return waiting ids."""
    waiting = []
    for m in members:
        if m["id"] not in prompts:
            continue
        prompt_path = run / stage_dir / "prompts" / f"{m['id']}.md"
        response_path = run / stage_dir / "responses" / f"{m['id']}.md"
        write(prompt_path, prompts[m["id"]])
        if response_path.exists() and not force:
            print(f"  = {m['id']}: 응답이 이미 있어 건너뜀")
            continue
        if m.get("type") in WAITING_TYPES:
            waiting.append(m["id"])
            continue
        print(f"  > {m['id']}: 요청 중...", flush=True)
        try:
            text = call_member(m, prompts[m["id"]])
        except MemberError as e:
            print(f"  ! {m['id']}: 실패 - {e}")
            write(run / "logs" / f"{stage_dir}-{m['id']}.log", f"{dt.datetime.now().isoformat()}\n{e}\n")
            continue
        write(response_path, text + "\n")
        print(f"  ✓ {m['id']}: 저장 {response_path.relative_to(run)}")
    for member_id in waiting:
        print(f"  … {member_id}: 대기 - {stage_dir}/prompts/{member_id}.md 의 답을 "
              f"{stage_dir}/responses/{member_id}.md 에 저장하세요")
    return waiting


# ---------------------------------------------------------------- anonymity


def redact_self_reference(text: str, terms: list[str]) -> str:
    """Hide phrases where a member names itself, e.g. "As Claude" or "저는 Gemini".

    Plain mentions of a model or company (e.g. an AI tool channel that
    reviews ChatGPT) are kept, because they can be part of the analysis.
    """
    article = r"\s+(?:an?\s+|the\s+)?(?:AI\s+)?(?:model\s+)?"
    for term in sorted(terms, key=len, reverse=True):
        name = re.escape(term) + r"(?![A-Za-z])"
        # "I am Claude", "I'm Gemini", "저는 Claude"
        text = re.sub(r"(?i)(?:\bI am\b|\bI'm\b|저는|나는)" + article + name, "[익명 위원]", text)
        # "As Claude, ..." (capital As + comma, so "such as Claude Code" is kept)
        text = re.sub(r"(?<![A-Za-z])As" + article + name + r"\s*,", "[익명 위원],", text)
    return text


def stage_responses(run: Path, stage_dir: str) -> dict[str, str]:
    folder = run / stage_dir / "responses"
    if not folder.exists():
        return {}
    return {p.stem: read(p).strip() for p in sorted(folder.glob("*.md")) if read(p).strip()}


def assign_labels(member_ids: list[str], seed: int) -> dict[str, str]:
    ids = sorted(member_ids)
    random.Random(seed).shuffle(ids)
    if len(ids) > 26:
        raise SystemExit("위원이 26명을 넘을 수 없습니다")
    return {string.ascii_uppercase[i]: member_id for i, member_id in enumerate(ids)}


def parse_ranking(text: str, labels: list[str]) -> list[str] | None:
    line = None
    for candidate in reversed(text.splitlines()):
        if re.search(r"FINAL\s+RANKING", candidate, re.IGNORECASE):
            line = candidate
            break
    if line is None:
        return None
    tail = re.split(r"FINAL\s+RANKING\s*[:：]?", line, flags=re.IGNORECASE)[-1]
    ranking = []
    for token in re.findall(r"(?<![A-Za-z])([A-Z])(?![A-Za-z])", tail):
        if token in labels and token not in ranking:
            ranking.append(token)
    return ranking or None


def aggregate_rankings(rankings: dict[str, list[str]], labels: list[str]) -> list[dict]:
    rows = []
    for label in labels:
        positions = [r.index(label) + 1 for r in rankings.values() if label in r]
        rows.append({
            "label": label,
            "average": round(sum(positions) / len(positions), 2) if positions else None,
            "votes": len(positions),
            "positions": positions,
        })
    rows.sort(key=lambda r: (r["average"] is None, r["average"] or 0, r["label"]))
    return rows


def aggregate_table(rows: list[dict]) -> str:
    lines = ["| 답변 | 평균 순위 | 평가 수 | 받은 순위 |", "|---|---|---|---|"]
    for r in rows:
        average = "-" if r["average"] is None else f"{r['average']:.2f}"
        positions = ", ".join(str(p) for p in r["positions"]) or "-"
        lines.append(f"| Response {r['label']} | {average} | {r['votes']} | {positions} |")
    return "\n".join(lines)


# ---------------------------------------------------------------- commands


def cmd_check(council: Council, args) -> int:
    print(f"council 폴더: {council.dir}")
    for m in council.config["members"]:
        state = "사용" if m.get("enabled") else "꺼짐"
        if m.get("paid"):
            state += "·유료"
        kind = m.get("type")
        if kind == "command":
            found = shutil.which(m["command"][0])
            detail = f"명령 {m['command'][0]}: " + (f"있음 ({found})" if found else "없음")
        elif kind == "openai_compatible":
            key_env = m.get("api_key_env")
            if key_env:
                detail = f"환경변수 {key_env}: " + ("설정됨" if os.environ.get(key_env) else "없음")
            else:
                detail = f"로컬 서버 {m['base_url']}: " + ("응답함" if server_up(m["base_url"]) else "응답 없음")
            if "CHANGE_ME" in m.get("model", ""):
                detail += " / model 값을 바꿔야 함"
        elif kind == "subagent":
            detail = "Claude Code 서브에이전트가 응답을 채움"
        else:
            detail = "사용자가 브라우저 답변을 붙여넣음"
        print(f"- {m['id']:<16} [{state}] {kind:<18} {detail}")
    if not getattr(args, "ping", False):
        return 0
    print("\n실제 호출 시험 (--ping): 켜져 있는 자동 위원에게 짧은 질문을 보냅니다")
    failed = 0
    for m in council.config["members"]:
        if not m.get("enabled") or m.get("type") not in AUTOMATED_TYPES:
            continue
        if m.get("paid") and not args.allow_paid:
            print(f"  - {m['id']}: 유료 위원이라 건너뜀")
            continue
        started = time.monotonic()
        try:
            reply = call_member({**m, "timeout": min(m.get("timeout", 600), args.ping_timeout)}, PING_PROMPT)
        except MemberError as e:
            failed += 1
            print(f"  ! {m['id']}: 실패 ({time.monotonic() - started:.1f}초) - {e}")
            continue
        short = " ".join(reply.split())[:60]
        print(f"  ✓ {m['id']}: 성공 ({time.monotonic() - started:.1f}초) - {short}")
    return 1 if failed else 0


def server_up(base_url: str) -> bool:
    try:
        with urllib.request.urlopen(base_url.rstrip("/") + "/models", timeout=3):
            return True
    except Exception:
        return False


def slugify(text: str) -> str:
    slug = re.sub(r"[^\w-]+", "-", text.strip(), flags=re.UNICODE).strip("-_")
    return slug[:50] or "run"


def cmd_new(council: Council, args) -> int:
    runs_dir = council.dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    base = f"{dt.date.today().isoformat()}_{slugify(args.topic)}"
    run = runs_dir / base
    suffix = 2
    while run.exists():
        run = runs_dir / f"{base}-{suffix}"
        suffix += 1
    existing = [p for p in runs_dir.iterdir() if (p / ".meta.json").exists()]
    rubric = args.rubric or council.settings.get("default_rubric", "general")
    council.rubric(rubric)  # fail early if the rubric is missing
    write(run / "question.md", args.topic.strip() + "\n")
    write(run / "fact-sheet.md", FACT_SHEET_TEMPLATE)
    save_json(run / ".meta.json", {
        "created": dt.datetime.now().isoformat(timespec="seconds"),
        "topic": args.topic.strip(),
        "rubric": rubric,
        "seed": random.SystemRandom().randrange(2**32),
        "run_index": len(existing),
    })
    print(run)
    return 0


def common_values(council: Council, run: Path, meta: dict) -> dict[str, str]:
    return {
        "OUTPUT_LANGUAGE": council.settings.get("output_language", "Korean"),
        "QUESTION": read(run / "question.md").strip(),
        "FACT_SHEET": strip_comments(read(run / "fact-sheet.md")),
        "RUBRIC": council.rubric(meta["rubric"]),
    }


def cmd_stage1(council: Council, args) -> int:
    run = Path(args.run)
    meta = run_meta(run)
    members = council.active(1, args.allow_paid)
    prompt = render(council.prompt_template("stage1"), **common_values(council, run, meta))
    print("Stage 1: 독립 의견")
    collect(run, "stage1", members, {m["id"]: prompt for m in members}, args.force)
    return 0


def responses_block(responses: dict[str, str], order: list[str], terms: list[str]) -> str:
    parts = [f"### Response {label}\n\n{redact_self_reference(responses[label], terms)}" for label in order]
    return "\n\n---\n\n".join(parts)


def cmd_stage2(council: Council, args) -> int:
    run = Path(args.run)
    meta = run_meta(run)
    answers = stage_responses(run, "stage1")
    minimum = council.settings.get("min_responses", 2)
    if len(answers) < minimum:
        print(f"Stage 1 응답이 {len(answers)}개뿐입니다. 최소 {minimum}개가 필요합니다.")
        return 1
    mapping_path = run / ".mapping.json"
    mapping = load_json(mapping_path, {})
    if not mapping.get("responses") or set(mapping["responses"].values()) != set(answers):
        if mapping.get("responses"):
            print("  Stage 1 응답 구성이 바뀌어 라벨을 다시 매깁니다.")
        mapping = {"responses": assign_labels(list(answers), meta["seed"])}
        save_json(mapping_path, mapping)
    labels = sorted(mapping["responses"])
    by_label = {label: answers[mapping["responses"][label]] for label in labels}

    reviewers = council.active(2, args.allow_paid)
    if not reviewers:
        print("Stage 2에 참여할 위원이 없습니다.")
        return 1
    rotation = [r for r in council.settings.get("devil_advocate_rotation", []) if r in {m["id"] for m in reviewers}]
    devil = rotation[meta["run_index"] % len(rotation)] if rotation else None
    meta["devil_advocate"] = devil
    save_json(run / ".meta.json", meta)

    values = common_values(council, run, meta)
    terms = council.settings.get("self_reference_terms", [])
    devil_note = council.prompt_template("devil-advocate")
    prompts = {}
    for m in reviewers:
        order = list(labels)
        random.Random(f"{meta['seed']}:{m['id']}").shuffle(order)
        prompts[m["id"]] = render(
            council.prompt_template("stage2"),
            ROLE_NOTE=devil_note if m["id"] == devil else "",
            RESPONSES=responses_block(by_label, order, terms),
            LABELS=", ".join(f"Response {label}" for label in labels),
            **values,
        )
    print(f"Stage 2: 익명 상호평가 (답변 {len(labels)}개, 반론자: {devil or '없음'})")
    collect(run, "stage2", reviewers, prompts, args.force)
    return cmd_aggregate(council, args, quiet=True)


def cmd_aggregate(council: Council, args, quiet: bool = False) -> int:
    run = Path(args.run)
    mapping = load_json(run / ".mapping.json", {})
    if not mapping.get("responses"):
        print("아직 Stage 2를 시작하지 않았습니다.")
        return 1
    labels = sorted(mapping["responses"])
    reviews = stage_responses(run, "stage2")
    rankings, unparsed = {}, []
    for reviewer, text in reviews.items():
        ranking = parse_ranking(text, labels)
        if ranking:
            rankings[reviewer] = ranking
        else:
            unparsed.append(reviewer)
    rows = aggregate_rankings(rankings, labels)
    table = aggregate_table(rows)
    note = f"\n\n순위를 읽지 못한 평가: {len(unparsed)}개" if unparsed else ""
    write(run / "stage2" / "aggregate.md", table + note + "\n")
    save_json(run / "stage2" / "aggregate.json", {"rows": rows, "unparsed": unparsed})
    if not quiet or rankings:
        print(f"순위 집계: 평가 {len(rankings)}개 반영" + (f", 읽기 실패 {', '.join(unparsed)}" if unparsed else ""))
        print(table)
    return 0


def choose_chair(council: Council, meta: dict, requested: str | None, allow_paid: bool) -> dict:
    if requested:
        chair_id = requested
    else:
        rotation = [
            c for c in council.settings.get("chair_rotation", ["claude"])
            if c in council.members and council.members[c].get("enabled")
        ]
        if not rotation:
            raise SystemExit("chair_rotation에 사용 가능한 위원이 없습니다")
        chair_id = rotation[meta["run_index"] % len(rotation)]
    chair = council.members.get(chair_id)
    if chair is None:
        raise SystemExit(f"의장 후보를 찾을 수 없습니다: {chair_id}")
    if chair.get("paid") and not allow_paid:
        raise SystemExit(f"{chair_id} 는 유료 위원이라 의장으로 쓸 수 없습니다 (--allow-paid 필요)")
    return chair


def cmd_stage3(council: Council, args) -> int:
    run = Path(args.run)
    meta = run_meta(run)
    mapping = load_json(run / ".mapping.json", {})
    if not mapping.get("responses"):
        print("Stage 2를 먼저 실행하세요.")
        return 1
    labels = sorted(mapping["responses"])
    answers = stage_responses(run, "stage1")
    by_label = {label: answers[mapping["responses"][label]] for label in labels}
    terms = council.settings.get("self_reference_terms", [])

    reviews = stage_responses(run, "stage2")
    if not reviews:
        print("Stage 2 평가가 하나도 없습니다.")
        return 1
    reviewer_ids = sorted(reviews)
    random.Random(f"{meta['seed']}:reviewers").shuffle(reviewer_ids)
    mapping["reviewers"] = {str(i + 1): rid for i, rid in enumerate(reviewer_ids)}
    save_json(run / ".mapping.json", mapping)
    reviews_block = "\n\n---\n\n".join(
        f"### 평가자 {i + 1}\n\n{redact_self_reference(reviews[rid], terms)}" for i, rid in enumerate(reviewer_ids)
    )
    cmd_aggregate(council, args, quiet=True)
    aggregate = read(run / "stage2" / "aggregate.md").strip()

    chair = choose_chair(council, meta, args.chair, args.allow_paid)
    meta["chair"] = chair["id"]
    save_json(run / ".meta.json", meta)
    prompt = render(
        council.prompt_template("stage3"),
        RESPONSES=responses_block(by_label, labels, terms),
        REVIEWS=reviews_block,
        AGGREGATE=aggregate,
        **common_values(council, run, meta),
    )
    write(run / "stage3" / "prompt.md", prompt)
    final_path = run / "stage3" / "final.md"
    print(f"Stage 3: 의장 종합 (의장: {chair['id']})")
    if final_path.exists() and not args.force:
        print("  = final.md 가 이미 있어 건너뜀")
        return 0
    if chair.get("type") in WAITING_TYPES:
        print("  … 대기 - stage3/prompt.md 의 답을 stage3/final.md 에 저장하세요")
        return 0
    try:
        text = call_member(chair, prompt)
    except MemberError as e:
        print(f"  ! 의장 {chair['id']} 실패 - {e}")
        return 1
    write(final_path, text + "\n")
    print("  ✓ stage3/final.md 저장")
    return 0


def cmd_finalize(council: Council, args) -> int:
    run = Path(args.run)
    meta = run_meta(run)
    final_path = run / "stage3" / "final.md"
    if not final_path.exists():
        print("stage3/final.md 가 없습니다. Stage 3를 먼저 마치세요.")
        return 1
    mapping = load_json(run / ".mapping.json", {})

    def name(member_id: str) -> str:
        member = council.members.get(member_id)
        return member["label"] if member else member_id

    response_rows = "\n".join(
        f"| Response {label} | {name(mid)} |" for label, mid in sorted(mapping.get("responses", {}).items())
    )
    reviewer_rows = "\n".join(
        f"| 평가자 {num} | {name(mid)} |" for num, mid in sorted(mapping.get("reviewers", {}).items(), key=lambda x: int(x[0]))
    )
    aggregate_path = run / "stage2" / "aggregate.md"
    aggregate = read(aggregate_path).strip() if aggregate_path.exists() else "-"
    log = f"""# Decision Log — {meta['topic']}

- 회의일: {meta['created'][:10]}
- 의장: {name(meta.get('chair', '-'))}
- 반론자: {name(meta['devil_advocate']) if meta.get('devil_advocate') else '-'}
- 채점 기준: rubrics/{meta['rubric']}.md
- 자료: [fact-sheet.md](fact-sheet.md)

## 의장 종합

{read(final_path).strip()}

## 순위 집계

{aggregate}

## 익명 해제

| 라벨 | 위원 |
|---|---|
{response_rows}

| 평가자 | 위원 |
|---|---|
{reviewer_rows}

## 실행 결과 (추후 기입)

- 실행한 행동:
- 결과 지표:
- 결론이 맞았는가 / 소수 의견이 맞았는가:
- 재검토 일자:
"""
    write(run / "decision-log.md", log)
    print(run / "decision-log.md")
    return 0


def cmd_status(council: Council, args) -> int:
    run = Path(args.run)
    meta = run_meta(run)
    print(f"{meta['topic']}  (rubric: {meta['rubric']}, chair: {meta.get('chair', '-')}, "
          f"devil: {meta.get('devil_advocate', '-')})")
    for stage_dir in ("stage1", "stage2"):
        prompts = sorted((run / stage_dir / "prompts").glob("*.md")) if (run / stage_dir / "prompts").exists() else []
        for p in prompts:
            done = (run / stage_dir / "responses" / p.name).exists()
            print(f"  {stage_dir} {p.stem:<16} {'완료' if done else '대기'}")
    if (run / "stage3" / "prompt.md").exists():
        done = (run / "stage3" / "final.md").exists()
        print(f"  stage3 {'chair':<16} {'완료' if done else '대기'}")
    print(f"  decision-log     {'완료' if (run / 'decision-log.md').exists() else '대기'}")
    return 0


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="LLM Council runner")
    parser.add_argument("--council-dir", type=Path, default=DEFAULT_COUNCIL_DIR)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("check")
    p.add_argument("--ping", action="store_true", help="자동 위원에게 실제로 짧은 질문을 보내 응답 확인")
    p.add_argument("--ping-timeout", type=int, default=180, help="--ping 때 위원별 최대 대기 시간(초)")
    p.add_argument("--allow-paid", action="store_true", help="유료 위원 허용 (사용자 요청 시에만)")
    p = sub.add_parser("new")
    p.add_argument("topic")
    p.add_argument("--rubric")
    for name in ("stage1", "stage2", "stage3"):
        p = sub.add_parser(name)
        p.add_argument("run")
        p.add_argument("--force", action="store_true", help="이미 있는 응답도 다시 요청")
        p.add_argument("--allow-paid", action="store_true", help="유료 위원 허용 (사용자 요청 시에만)")
        if name == "stage3":
            p.add_argument("--chair")
    for name in ("aggregate", "finalize", "status"):
        sub.add_parser(name).add_argument("run")

    args = parser.parse_args(argv)
    council = Council(args.council_dir.resolve())
    handlers = {
        "check": cmd_check, "new": cmd_new, "stage1": cmd_stage1, "stage2": cmd_stage2,
        "aggregate": cmd_aggregate, "stage3": cmd_stage3, "finalize": cmd_finalize, "status": cmd_status,
    }
    return handlers[args.command](council, args)


if __name__ == "__main__":
    sys.exit(main())
