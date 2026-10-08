# LLM Council (Phase A)

여러 LLM에게 같은 안건을 독립적으로 묻고 → 익명으로 서로 평가하게 한 뒤 → 의장이 종합하는 회의 도구입니다. 구조는 [karpathy/llm-council](https://github.com/karpathy/llm-council)의 3단계를 따르고, 설계 배경은 [`docs/llm-council/`](../docs/llm-council/) 문서에 있습니다.

> 표기: 링크 = 출처로 확인한 사실 / [추론] = 출처 없는 판단 / ⚠️ = 확인 필요

## 위원 구성 ($0)

| id | 위원 | 실행 방식 | 비용 |
|---|---|---|---|
| `claude` | Claude | Claude Code 서브에이전트가 답변 | Claude Max 구독 |
| `gemini` | Gemini (의장 고정) | 스크립트가 Gemini API를 직접 호출 (API 키) | 무료 API 키 — Google 로그인 방식 Gemini CLI는 2026-06-18 개인 계정 중단 ([공지 #28017](https://github.com/google-gemini/gemini-cli/discussions/28017)) |
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
2. **Node.js (LTS)** — [nodejs.org](https://nodejs.org/). Codex CLI 설치에 필요합니다.
3. **Gemini API 키** — 아래 "Gemini 연결" 절차.
4. **Codex CLI** — `npm install -g @openai/codex` 후 `codex login`으로 ChatGPT 계정 로그인 ([Codex Auth](https://developers.openai.com/codex/auth)). 2026-10-08 이 환경에서 0.161.0 설치·도움말 확인.
5. 점검: `python council/scripts/council.py check --ping`

### Gemini 연결 (API 키 방식)

1. [Google AI Studio](https://aistudio.google.com)에 Google 계정으로 로그인해 **API 키**를 만듭니다 ([Gemini API 키 문서](https://ai.google.dev/gemini-api/docs/api-key)).
2. 키를 Windows 환경변수 `GEMINI_API_KEY`에 넣습니다: Windows 검색에서 "계정의 환경 변수 편집" → 새로 만들기 → 이름 `GEMINI_API_KEY`, 값에 키. (명령어로 넣으면 PowerShell 기록에 남으므로 이 화면을 권장. **키를 Claude Code 채팅에 붙여넣지 마세요.**)
3. PowerShell과 Claude Code를 **새로 엽니다** (환경변수는 새로 연 창부터 적용).
4. 쓸 수 있는 모델 확인: `python council/scripts/council.py models gemini --filter flash`
5. 목록에서 Flash 모델 ID 하나를 골라 `council/members.json`의 `gemini` → `model`에 적습니다 (또는 Claude Code에 "members.json의 gemini 모델을 <ID>로 바꿔줘").
6. `python council/scripts/council.py check --ping` → `✓ gemini: 성공`과 `의장: gemini — 설정 확인됨`이 나오면 회의를 열 수 있습니다.

- 2026-06-18부터 무료·Google AI Pro·Ultra 개인 계정의 Gemini CLI 사용이 중단되었고, API 키 인증은 영향이 없습니다 ([Gemini CLI 공식 공지 #28017](https://github.com/google-gemini/gemini-cli/discussions/28017)). 그래서 Gemini는 CLI 대신 **API 키로 스크립트가 직접** 부릅니다 ([Gemini OpenAI 호환 문서](https://ai.google.dev/gemini-api/docs/openai)).
- 무료 등급은 Flash 계열 위주이고, 무료 등급 입력은 구글 제품 개선에 쓰일 수 있습니다 ⚠️ 출처 간 세부 차이 있음 ([Klymentiev](https://klymentiev.com/blog/gemini-api-free-tier), [GeoToolbox](https://geotoolbox.ai/blog/gemini-api-pricing)). 자료표에 비공개 정보를 넣지 마세요.
- **의장(gemini)이 준비되기 전에는 `new`가 회의를 시작하지 않습니다(회의 보류, 사용자 결정).**

## 사용법

자세한 사용법은 [사용 가이드](../docs/llm-council/03-claude-code-usage-guide.md)를 보세요. Claude Code에서 `/llm-council <안건>`이라고 하면 [스킬](../.claude/skills/llm-council/SKILL.md)이 아래 순서를 진행합니다. 직접 실행할 때는:

```powershell
python council/scripts/council.py new "최근 6~12개월 글로벌 급성장 채널 분석" --rubric youtube-growth
python council/scripts/council.py stage1 council/runs/<run> --prepare   # 프롬프트만 먼저 생성
python council/scripts/council.py stage1 council/runs/<run>             # Gemini·Codex 병렬 호출
#  → 같은 시간에 claude(서브에이전트)·브라우저 위원 응답을 stage1/responses/<id>.md 에 저장
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
| 의장 고정: Gemini (사용자 결정) | stage3 | 진행자(Claude Code)와 다른 회사 모델이 종합. 원본 llm-council의 기본 의장도 Gemini ([karpathy/llm-council](https://github.com/karpathy/llm-council)) |
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
