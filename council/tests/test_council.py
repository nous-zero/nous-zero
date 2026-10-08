"""Tests for council.py. Run from the repo root:

    python -m unittest discover -s council/tests -v
"""

import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

COUNCIL_DIR = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("council", COUNCIL_DIR / "scripts" / "council.py")
council = importlib.util.module_from_spec(spec)
spec.loader.exec_module(council)

# A fake CLI member: answers Stage 1 prompts, and ranks answers in Stage 2.
FAKE_MEMBER = r"""
import re, sys
prompt = sys.stdin.read()
if "의장 종합" in prompt:
    print("최종 결론: 테스트")
elif "FINAL RANKING" in prompt:
    labels = re.findall(r"### Response ([A-Z])", prompt)
    print("평가 내용\nFINAL RANKING: " + " > ".join("Response " + l for l in sorted(labels)))
else:
    print("I am Gemini. 테스트 답변")
"""


class UnitTests(unittest.TestCase):
    def test_parse_ranking_reads_last_final_ranking_line(self):
        text = "예시: FINAL RANKING: Response ? > ...\n본문\n**FINAL RANKING:** Response B > Response A > C"
        self.assertEqual(council.parse_ranking(text, ["A", "B", "C"]), ["B", "A", "C"])

    def test_parse_ranking_ignores_unknown_labels_and_missing_line(self):
        self.assertEqual(council.parse_ranking("FINAL RANKING: Response D > Response A", ["A", "B"]), ["A"])
        self.assertIsNone(council.parse_ranking("순위 없음", ["A", "B"]))

    def test_aggregate_rankings_orders_by_average_position(self):
        rows = council.aggregate_rankings({"r1": ["B", "A"], "r2": ["B", "A"], "r3": ["A", "B"]}, ["A", "B"])
        self.assertEqual([r["label"] for r in rows], ["B", "A"])
        self.assertEqual(rows[0]["average"], 1.33)

    def test_redact_hides_self_reference_but_keeps_mentions(self):
        terms = ["Claude", "Gemini", "ChatGPT"]
        self.assertEqual(council.redact_self_reference("I am Claude, 분석합니다", terms), "[익명 위원], 분석합니다")
        self.assertEqual(council.redact_self_reference("저는 Gemini입니다", terms), "[익명 위원]입니다")
        self.assertEqual(council.redact_self_reference("As ChatGPT, I think", terms), "[익명 위원], I think")
        kept = "ChatGPT 튜토리얼 채널이 성장했고 tools such as Claude Code가 언급됨"
        self.assertEqual(council.redact_self_reference(kept, terms), kept)

    def test_assign_labels_is_deterministic_for_a_seed(self):
        first = council.assign_labels(["gemini", "codex", "claude"], 7)
        self.assertEqual(first, council.assign_labels(["claude", "gemini", "codex"], 7))
        self.assertEqual(sorted(first), ["A", "B", "C"])


class PipelineTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for name in ("prompts", "rubrics"):
            shutil.copytree(COUNCIL_DIR / name, self.tmp / name)
        script = self.tmp / "fake_member.py"
        script.write_text(FAKE_MEMBER, encoding="utf-8")
        member = lambda mid, **kw: {
            "id": mid, "label": mid, "type": "command",
            "command": [sys.executable, str(script), mid], "output": "stdout",
            "enabled": True, "paid": False, **kw,
        }
        config = {
            "settings": {
                "chair_rotation": ["fake-a"], "devil_advocate_rotation": ["fake-b"],
                "self_reference_terms": ["Gemini"], "min_responses": 2,
            },
            "members": [
                member("fake-a"),
                member("fake-b"),
                {"id": "claude", "label": "Claude", "type": "subagent", "enabled": True},
                {"id": "web", "label": "Web", "type": "manual", "stages": [1], "enabled": True},
                member("paid-one", paid=True),
            ],
        }
        (self.tmp / "members.json").write_text(json.dumps(config), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_cli(self, *args):
        out = io.StringIO()
        with redirect_stdout(out):
            code = council.main(["--council-dir", str(self.tmp), *args])
        return code, out.getvalue()

    def test_full_meeting(self):
        code, out = self.run_cli("new", "테스트 안건")
        self.assertEqual(code, 0)
        run = Path(out.strip().splitlines()[-1])

        code, out = self.run_cli("stage1", str(run))
        self.assertIn("paid-one: 유료 위원이라 건너뜀", out)
        self.assertTrue((run / "stage1/responses/fake-a.md").exists())
        self.assertFalse((run / "stage1/responses/paid-one.md").exists())
        self.assertTrue((run / "stage1/prompts/claude.md").exists())
        self.assertTrue((run / "stage1/prompts/web.md").exists())

        # Claude Code (subagent) and a person (manual) fill their answers.
        (run / "stage1/responses/claude.md").write_text("서브에이전트 답변", encoding="utf-8")
        (run / "stage1/responses/web.md").write_text("브라우저 답변", encoding="utf-8")

        code, out = self.run_cli("stage2", str(run))
        self.assertEqual(code, 0)
        mapping = json.loads((run / ".mapping.json").read_text(encoding="utf-8"))
        self.assertEqual(sorted(mapping["responses"].values()), ["claude", "fake-a", "fake-b", "web"])
        self.assertFalse((run / "stage2/prompts/web.md").exists(), "manual member is Stage 1 only")
        review_prompt = (run / "stage2/prompts/fake-a.md").read_text(encoding="utf-8")
        for member_id in ("fake-a", "fake-b"):
            self.assertNotIn(member_id, review_prompt)
        self.assertNotIn("I am Gemini", review_prompt)
        self.assertIn("[익명 위원]", review_prompt)
        self.assertIn("Devil's Advocate", (run / "stage2/prompts/fake-b.md").read_text(encoding="utf-8"))
        self.assertNotIn("Devil's Advocate", review_prompt)

        (run / "stage2/responses/claude.md").write_text(
            "평가\nFINAL RANKING: Response D > Response C > Response B > Response A", encoding="utf-8")
        code, out = self.run_cli("stage3", str(run))
        self.assertEqual(code, 0)
        chair_prompt = (run / "stage3/prompt.md").read_text(encoding="utf-8")
        for member_id in ("fake-a", "fake-b"):
            self.assertNotIn(member_id, chair_prompt)
        self.assertIn("| Response A |", chair_prompt)
        self.assertTrue((run / "stage3/final.md").exists())

        code, out = self.run_cli("finalize", str(run))
        self.assertEqual(code, 0)
        log = (run / "decision-log.md").read_text(encoding="utf-8")
        self.assertIn("최종 결론: 테스트", log)
        self.assertIn("| Response A |", log)

    def test_stage2_needs_two_answers(self):
        _, out = self.run_cli("new", "응답 부족")
        run = Path(out.strip().splitlines()[-1])
        (run / "stage1/responses").mkdir(parents=True)
        (run / "stage1/responses/claude.md").write_text("하나뿐", encoding="utf-8")
        code, out = self.run_cli("stage2", str(run))
        self.assertEqual(code, 1)
        self.assertIn("최소 2개", out)


if __name__ == "__main__":
    unittest.main()
