# LLM Council (Phase A)

여러 LLM에게 같은 안건을 독립적으로 묻고 → 익명으로 서로 평가하게 한 뒤 → 의장이 종합하는 회의 도구입니다. 구조는 [karpathy/llm-council](https://github.com/karpathy/llm-council)의 3단계를 따르고, 설계 배경은 [`docs/llm-council/`](../docs/llm-council/) 문서에 있습니다.

> 표기: 링크 = 출처로 확인한 사실 / [추론] = 출처 없는 판단 / ⚠️ = 확인 필요

## 위원 구성 ($0)

| id | 위원 | 실행 방식 | 비용 |
|---|---|---|---|
| `claude` | Claude | Claude Code 서브에이전트가 답변 | Claude Max 구독 |
| `gemini` | Gemini | Gemini CLI 자동 호출 | Google AI Pro 구독 (하루 1,500회, [Gemini CLI Quotas](https://geminicli.com/docs/resources/quota-and-pricing/)) |
| `codex` | GPT | Codex CLI 자동 호출 | ChatGPT 무료 계정 ([OpenAI Help](https://help.openai.com/en/articles/11369540-codex-usage-limits), 무료 한도 ⚠️) |
| `meta-ai` | Meta AI | 브라우저에서 사람이 붙여넣기 (Stage 1만) | 무료 계정 |
| `perplexity` | Perplexity | 브라우저에서 사람이 붙여넣기 (Stage 1만) | 무료 계정 |
| `grok-web` | Grok | 브라우저에서 사람이 붙여넣기 (Stage 1만) | 무료 계정 |

- 꺼져 있는 예비 위원: `llama-local`(로컬 Ollama), `claude-cli`(Claude Code 밖에서 실행할 때), `openrouter-free`(OpenRouter 무료 모델)
- 유료 위원(`grok`, `perplexity-api`)은 `"paid": true`라 `--allow-paid` 없이는 실행되지 않습니다. 사용자가 요청할 때까지 보류합니다.
- 브라우저 위원(`meta-ai`, `perplexity`, `grok-web`)은 회의마다 방식을 고릅니다: **A. 사용자가 지켜보는 가운데 Claude in Chrome이 붙여넣기·복사**, **B. 사용자가 직접 붙여넣기**, **C. 생략**. 로그인·CAPTCHA·동의 화면이 나오면 Claude는 멈추고 사용자에게 넘깁니다.
- ⚠️ 각 사이트 약관의 자동화 관련 조항은 원문으로 확인하지 못했습니다(서드파티 정리 자료만 확인). 각 사이트 하단의 Terms 링크에서 직접 확인하세요.

## Windows 설치

1. **Python 3.10+** — [python.org](https://www.python.org/downloads/). 이 도구는 표준 라이브러리만 씁니다.
2. **Node.js (LTS)** — [nodejs.org](https://nodejs.org/). Gemini CLI와 Codex CLI 설치에 필요합니다.
3. **Gemini CLI** — `npm install -g @google/gemini-cli` 후 `gemini`를 한 번 실행해 Google 계정으로 로그인 ([Gemini CLI 문서](https://geminicli.com/docs)). 2026-10-08 이 환경에서 0.63.0 설치·도움말 확인.
4. **Codex CLI** — `npm install -g @openai/codex` 후 `codex login`으로 ChatGPT 계정 로그인 ([Codex Auth](https://developers.openai.com/codex/auth)). 2026-10-08 이 환경에서 0.161.0 설치·도움말 확인.
5. 점검: `python council/scripts/council.py check`

## 사용법

자세한 사용법은 [사용 가이드](../docs/llm-council/03-claude-code-usage-guide.md)를 보세요. Claude Code에서 `/llm-council <안건>`이라고 하면 [스킬](../.claude/skills/llm-council/SKILL.md)이 아래 순서를 진행합니다. 직접 실행할 때는:

```powershell
python council/scripts/council.py new "최근 6~12개월 글로벌 급성장 채널 분석" --rubric youtube-growth
python council/scripts/council.py stage1 council/runs/<run>
#  → claude / 수동 위원 응답을 stage1/responses/<id>.md 에 저장
python council/scripts/council.py stage2 council/runs/<run>
#  → claude 평가를 stage2/responses/claude.md 에 저장
python council/scripts/council.py stage3 council/runs/<run>
python council/scripts/council.py finalize council/runs/<run>
python council/scripts/council.py status council/runs/<run>
```

## 편향 완화 장치

| 장치 | 위치 | 이유 |
|---|---|---|
| 답변 익명화 (Response A, B…) | stage2 | 원본 llm-council과 같은 이유: "the LLM can't play favorites" ([karpathy/llm-council](https://github.com/karpathy/llm-council)) |
| 자기 소개 문구 가리기 ("I am Claude", "저는 Gemini") | stage2·3 | LLM 평가자는 자기 글을 알아보고 선호함 ([Panickssery et al., 2024](https://arxiv.org/abs/2404.13076)) |
| 평가자마다 답변 순서 섞기 | stage2 | LLM 평가자의 위치 편향 ([Zheng et al., 2023](https://arxiv.org/abs/2306.05685)) |
| 채점 기준(루브릭) | `rubrics/` | 의장이 '누가 말했나'가 아니라 기준으로 판단 [추론] |
| 반론자 순환 | stage2 | 집단사고 방지 [추론] |
| 의장 교대 (claude ↔ gemini) | stage3 | 의장이 늘 Claude면 결론이 Claude 쪽으로 기울 수 있음 [추론] |
| 소수 의견 기록 | stage3·decision-log | 나중에 결과와 대조 [추론] |
| CLI 위원은 빈 임시 폴더에서 실행 | 스크립트 | 에이전트형 CLI가 다른 위원의 답 파일을 읽지 못하게 함 [추론] |

## 폴더 구조

```
council/
├─ members.json            위원 설정 (enabled, paid, 실행 명령)
├─ prompts/                stage1·2·3 질문 템플릿, 반론자 지시문
├─ rubrics/                채점 기준 (general, youtube-growth)
├─ scripts/council.py      실행 스크립트
├─ tests/test_council.py   테스트: python -m unittest discover -s council/tests -v
└─ runs/<날짜_안건>/        회의 기록
   ├─ question.md, fact-sheet.md
   ├─ stage1/ prompts/ responses/
   ├─ stage2/ prompts/ responses/ aggregate.md
   ├─ stage3/ prompt.md final.md
   └─ decision-log.md
```

## 주의

- Claude Code 세션 안에서 `claude -p`를 다시 부르면 중첩 세션 차단에 걸리거나 멈추는 사례가 보고되어 있습니다([claudeissues #26190](https://claudeissues.com/issue/26190-nested-claude-p-instances-hang-when-claudecode-env-var-is-inherited), [#29543](https://claudeissues.com/issue/29543-bug-claude-print-produces-no-output-when-claudecode-env-var-is-unset-inside-a-se)). 그래서 세션 안에서는 서브에이전트를 쓰고, 일반 터미널에서 돌릴 때만 `claude-cli`를 켭니다.
- Groq는 2026-08-16 무료·개발자 등급에서 Llama 모델을 종료했습니다([Groq Deprecations](https://console.groq.com/docs/deprecations)). Meta Llama를 무료로 쓰려면 로컬 Ollama(`llama-local`)를 켜야 합니다.
