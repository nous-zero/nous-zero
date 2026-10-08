---
name: llm-council
description: 여러 LLM(Claude·Gemini·GPT, 브라우저로 Meta AI·Perplexity·Grok)에게 같은 안건을 독립적으로 묻고, 익명 상호평가와 의장 종합을 거쳐 자료 근거 결론과 Decision Log를 만드는 LLM Council 회의 절차. 사용자가 "카운슬", "council", "위원회", "여러 LLM 의견", "교차 검증"을 말하거나, YouTube 기획·주제 선정·수익화처럼 한 모델의 편향 없이 판단해야 하는 안건을 낼 때 사용한다.
argument-hint: "<안건>"
---

# LLM Council 회의 진행

이 세션은 **진행자**다. 진행자는 의견을 내지 않고, 위원 답변을 고치거나 요약해서 다음 단계에 넘기지 않는다. 단계별 프롬프트 생성·익명화·순위 집계는 `council/scripts/council.py`가 한다.

명령 앞부분은 Windows에서 `python`, macOS·Linux에서 `python3`이다. 아래 `$RUN`은 `new`가 출력한 run 폴더 경로다.

## 지켜야 할 규칙

1. **유료 위원 금지**: `members.json`에서 `"paid": true`인 위원은 사용자가 이번 대화에서 명시적으로 요청하기 전까지 켜지 않는다. `--allow-paid`도 쓰지 않는다.
2. **Claude 위원·의장은 서브에이전트로**: 이 세션 안에서 `claude -p`를 실행하지 않는다(중첩 세션 차단 문제). Claude의 답변·평가·의장 종합은 Agent 도구의 새 서브에이전트가 만든다.
3. **서브에이전트에게는 프롬프트 파일 하나만**: 서브에이전트 프롬프트는 아래 문구를 그대로 쓴다. `.mapping.json`이나 다른 위원의 응답 파일을 보여주지 않는다.
   > `<프롬프트 파일 절대경로>` 파일을 읽고, 그 안의 지시에 따라 답변 텍스트만 작성해서 반환하세요. 다른 파일은 읽지 말고, 웹 검색·명령 실행·파일 수정도 하지 마세요.
4. **원문 그대로 저장**: 서브에이전트가 반환한 텍스트나 사용자가 붙여넣은 답변은 한 글자도 바꾸지 않고 응답 파일에 저장한다.
5. **사실과 추론 구분**: 자료(fact-sheet)의 모든 항목에는 출처를 적고, 출처 없는 내용은 `[추론]`으로 표시한다. 사용자에게 보고할 때도 같다.
6. 응답이 2개 미만이면 다음 단계로 가지 말고 사용자에게 알린다. 실패한 위원은 `$RUN/logs/`의 오류를 요약해 알린다.

## 절차

### 0. 점검
`python council/scripts/council.py check` — 꺼져 있거나 설치되지 않은 위원을 사용자에게 알린다.

### 1. 안건과 자료
1. `python council/scripts/council.py new "<안건>" [--rubric youtube-growth]` → 출력된 경로가 `$RUN`.
2. `$RUN/fact-sheet.md`를 채운다. 웹 검색·사용자가 준 데이터로 표를 만들고, 행마다 출처 링크와 수집일을 적는다.
3. 자료 요약을 사용자에게 보여주고, 빠진 데이터가 있는지 확인받는다.

### 2. Stage 1 — 독립 의견
1. `python council/scripts/council.py stage1 $RUN` — Gemini·Codex 같은 CLI 위원은 스크립트가 자동으로 부른다(몇 분 걸릴 수 있음).
2. `claude`(서브에이전트): 규칙 3의 문구로 `$RUN/stage1/prompts/claude.md`를 넘기고, 결과를 `$RUN/stage1/responses/claude.md`에 저장한다.
3. `meta-ai`·`perplexity`·`grok-web`(수동): 사용자에게 안내한다.
   - `$RUN/stage1/prompts/<id>.md` 내용을 복사해 meta.ai / perplexity.ai / grok.com에 붙여넣는다.
   - 받은 답변을 채팅에 붙여넣어 주면 진행자가 `$RUN/stage1/responses/<id>.md`에 원문 그대로 저장한다.
   - 사용자가 이번 회의에서 수동 위원을 건너뛰겠다고 하면 기다리지 않는다.
4. `python council/scripts/council.py status $RUN`으로 빠진 응답을 확인한다.

### 3. Stage 2 — 익명 상호평가
1. `python council/scripts/council.py stage2 $RUN` — 라벨(Response A, B…)을 무작위로 붙이고 평가자마다 순서를 섞는다. 반론자(Devil's Advocate)는 회의마다 돌아가며 정해진다.
2. `claude` 평가: `$RUN/stage2/prompts/claude.md`를 서브에이전트에 넘기고 결과를 `$RUN/stage2/responses/claude.md`에 저장한다.
3. `python council/scripts/council.py aggregate $RUN` — 평가 마지막 줄의 `FINAL RANKING`을 읽어 평균 순위를 낸다. 읽기 실패한 평가가 있으면 사용자에게 알린다.

### 4. Stage 3 — 의장 종합
1. `python council/scripts/council.py stage3 $RUN` — 의장은 회의마다 `chair_rotation`(claude ↔ gemini) 순서로 바뀐다. 사용자가 원하면 `--chair <id>`.
2. 의장이 `gemini`면 스크립트가 자동 실행한다. 의장이 `claude`면 `$RUN/stage3/prompt.md`를 서브에이전트에 넘기고 결과를 `$RUN/stage3/final.md`에 저장한다.

### 5. 기록과 보고
1. `python council/scripts/council.py finalize $RUN` → `$RUN/decision-log.md` (익명 해제 표 포함).
2. 사용자에게 보고한다: 최종 결론, 근거, 소수 의견, 확신도, 순위 집계, 익명 해제 결과, 다음 행동. 사실은 출처와 함께, 추론은 `[추론]`으로 표시한다.
3. run 폴더를 커밋할지 사용자에게 묻는다(포트폴리오 기록용).
