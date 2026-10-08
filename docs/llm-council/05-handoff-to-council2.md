# LLM Council 인수인계: 클라우드 세션(Council 1) → 로컬 PC 세션(LLM Council 2)

> 작성일: 2026-10-08 · 작성: 클라우드 세션 «LLM Council 1» (Claude Code on the web)
> 기준 커밋: `0216f6e` (이 문서 직전) · 브랜치: `claude/llm-concile-usage-interview-pnttr8`
>
> 이관 근거: 대표님 «LLM Concile 1의 내용을 모두 가져 와서 현재 세션에서 이어 가세요» · «깃허브를 활용» (Council 2 전달), 그리고 Council 1에 직접 «세션 내용을 깃허브에 커밋하고 세션 내용을 LLM Council 2 세션에 인계».
>
> **이 문서를 푸시한 뒤 Council 1은 이 브랜치를 더 고치지 않습니다.** 이후 수정은 Council 2가 합니다.
>
> 표기: «…» = 대표님 원문 인용(오탈자 포함 그대로) / 링크 = 출처 / [추론] = 출처 없는 Claude 판단 / [미확인] = 검증 안 됨

이 문서는 01~04 문서, `council/README.md`, `.claude/skills/llm-council/SKILL.md`, `council/members.json`에 **아직 없는 것** 위주로 적었습니다.

---

## ① 대표님 결정 전부 (모두 2026-10-08)

### 1-1. 인터뷰에서 정한 방향

| # | 주제 | 대표님 원문 | 반영 |
|---|---|---|---|
| D1 | 주 용도 | «유투브 영상 제작을 자동화 하려고 합니다. 그런데 유투브 영상 제작을 하려면 기획 부터 발행, 마케팅, 고객분석등 수익창출등 해야 할 일들이 많지만 사용자 혼자 또는 클로드 만으로는 편향되기에 다양한 llm의 의견을 토대로 진행하기를 원합니다.» + 논문·연구 검증, 코드 학습·리뷰, 커리어·의사결정, 독서·개념 학습도 선택 | 01 문서 |
| D2 | 당시 사용 방식 | «사용자가 클로드 코드 세션에서 브라우저 형태로 의견을 교신 하도록 명령 해서 자동으로 의견을 취합 합니다.» | 공식 CLI/API 경로로 전환 (아래 D17·D18) |
| D3 | 원하는 결과 | «실제로 llm concile을 활용 하고자 하며, 다음 단계로 개발 또한 코덱스, 클로드 코드등 을 활용해서 개발을 하기를 희망합니다.» | Phase A 구현 |
| D4 | 비용 우선순위 | «1. 가능하다면 무료로 로컬로 활용 하고 싶고( 한계성을 알아야 함), 2. 최소비용, 3.유료 api 를 해보려 합니다.» | $0 구성 |
| D5 | 예산 | «잘 모르겠습니다. 수익성으로 봤을 때 투자할 가치가 있다면 투자 할 의향이 분명히 있습니다.» | 유료는 D14로 보류 |
| D6 | 첫 적용 단계 | «유투브 6개월~1년내 가장 빠르고 큰 성장률(조회수/구독자등)을 낸 채널들의 / 영상 분석을 통한 기획/주제 선정/수익화 전략» | 첫 안건 |
| D7 | 채널 상태 | «이미 운영중이고 부진한 관계로 새 채널을 고민 중임» | — |
| D8 | 타깃 | «영어권 시청자 및 다국어 고려중입니다 결론: 글로벌» | — |
| D9 | 사용 방식 | «클로드 코드를 통해 타겟을 달성하기 위한 과정 내내 llm간 의견을 교신 하게 하고 데이터에 근거해서 결론을 정하고 이런 과정을 지속적으로 반복하게 합니다. 또한 정기적으로 체크 해야 할 내용들, 새로운 트랜드 / 방식등을 매일 흡수하고 검증하며 필요에 따라 적재적소에 투입 하고자 합니다.» | 매일 루틴은 미구현 (③) |
| D10 | 우선순위 | «실전에 활용 하고 이를 통해서 포트폴리오(링크드인 블로그/영상)으로 남겨서 공유 합니다.» | Decision Log를 포트폴리오 원천으로 |
| D11 | 제3 위원 | «무료 오픈모델로 시작» | 이후 D12로 확장 |
| D12 | **첫 안건·기존 채널** | «기존 채널을 진단하면 급성장 채널을 분석하면 왜곡될 수 있기에 글로벌 급성장 채널 분석이 우선이며 우리 채널은 사용자의 요청이 있을때에만 분석합니다.» | **기존 채널 진단은 요청 시에만** |
| D13 | 위원 확장 | «추가로 메타,크록,퍼플렉시티,gpt 외 연결을 희망합니다» | 02 문서, 브라우저 위원 |
| D14 | **유료 보류** | «유료 요금제는 사용자 요청이 있기까지 보류 하겠습니다. Phase A를 시작» | `paid: true` 위원은 `--allow-paid` 없이 실행 안 됨 |
| D15 | Perplexity 구독 | «Perplexity는 현재 구독중이 아닙니다.» | 구독 불필요 경로만 기록 |
| D16 | 편향 대책의 위치 | «이부분을 위해서 llm concile을 사용하는 겁니다.» (익명화·순서 섞기·채점 기준·의장 교대·소수 의견 기록에 대해) | 01 문서 2.2 "두 층의 편향"으로 보완 |
| D17 | **브라우저 위원 자동 보조** | «사용자가 보고 있기에 사이트 탐지 회피가 아닙니다 . 수동 조작을 하지 않을 뿐이죠.» | `browser_mode: assist` (Claude in Chrome, 대표님이 지켜봄) |
| D18 | **동시 실행** | «/llm-council을 할 때 Gemini·GPT 호출과 동시에 브라우저 위원을 자동으로 실행해야 합니다.» | `--prepare` + 병렬 호출 + 브라우저·서브에이전트 동시 진행 |
| D19 | **의장 Gemini 고정** | «의장은 항상 제미나이로 고정하세요.» | `chair_rotation: ["gemini"]` |
| D20 | **Gemini 대체 = 1-b** | 선택지 응답: «1-b: API키+스크립트 직접 (추천)» | Gemini API(OpenAI 호환) + `GEMINI_API_KEY` |
| D21 | **임시 의장 없음 → 회의 보류** | 선택지 응답: «회의 보류» (Codex 임시 의장·Claude 임시 의장 선택지를 고르지 않음) | `new`가 의장 미준비 시 거부 |
| D22 | 이관 | 위 머리말 인용 | 이 문서 |

### 1-2. 버린 것과 이유

| 버린 것 | 이유 | 근거 |
|---|---|---|
| Karpathy 원본 llm-council 설치 | OpenRouter 유료 크레딧 필요, 제작자가 "I'm not going to support it in any way", Windows 실행 안내 없음 | [karpathy/llm-council](https://github.com/karpathy/llm-council) |
| 브라우저 화면 자동 조작으로 **흔적을 숨기는** 방식 | 대표님 첫 요청 «자동 데이터 수집 근거 <head>를 남기지 마세요»를 Council 1이 "탐지 회피"로 이해해 거절 → 대표님이 D17로 "숨기는 것이 아니라 지켜보는 자동 보조"라고 정정. **흔적 숨기기 기능은 만들지 않음** | 대화 기록 |
| Groq 무료 Llama | Groq가 2026-08-16 무료·개발자 등급에서 Llama 3.x 종료(Scout는 07-17) | [Groq Deprecations](https://console.groq.com/docs/deprecations) (검색 결과 경유) |
| 로컬 Ollama를 주력 위원으로 | Radeon 780M은 Ollama ROCm 공식 목록에 없음, 32B 실측 약 4 tok/s → 보조로만 (`llama-local` 꺼둠) | 02 문서 1.1, [Radxa forum](https://forum.radxa.com/t/llama-cpp-benchmarks/27813/17) |
| Colab·Kaggle을 위원 서버로 | 무료 Colab은 노트북과 무관한 웹 서비스·프록시 금지로 알려짐, 세션 12시간·GPU 미보장 → 실험·학습용으로만 | 02 문서 1.6 |
| Claude Code 안에서 `claude -p` 호출 | 중첩 세션 차단·멈춤 보고 → Claude 위원·평가는 서브에이전트 | [claudeissues #26190](https://claudeissues.com/issue/26190-nested-claude-p-instances-hang-when-claudecode-env-var-is-inherited) |
| Gemini CLI + Google 로그인 | 2026-06-18 개인 계정(무료·AI Pro·Ultra) 중단, PC에서 `IneligibleTierError` | [Gemini CLI 공지 #28017](https://github.com/google-gemini/gemini-cli/discussions/28017) |
| 의장 교대(Claude ↔ Gemini) | D19로 Gemini 고정 | — |
| 임시 의장(Codex·Claude) | D21로 회의 보류 선택 | — |
| 2안 브라우저 Gemini | 자동 평가·의장에서 빠짐 → D19와 충돌 | 대화 기록 |
| 3안 Antigravity CLI(`agy`) | `agy -p` 멈춤이 v1.2.0(9/11)·v1.2.3(9/15)에도 재현 보고, 이슈는 9/3에 닫혔지만 닫힘 ≠ 해결 | [antigravity-cli #318](https://github.com/google-antigravity/antigravity-cli/issues/318) |
| Perplexity Pro 구독(API $5 크레딧용) | API는 구독과 별도 결제, $5 혜택 중단 보고도 있음 → 구독 불필요 | 02 문서 1.3 |
| 유료 위원(Grok API·Perplexity API·OpenRouter $10·Meta Model API) | D14 보류 | — |

---

## ② 대표님 요구·선호·금지 (문서에 아직 없는 것)

### 2-1. 대표님이 Claude 설정에 둔 상시 선호 (모든 답변에 적용)
1. «근거(출처) 없는 답변 금지.»
2. «클로드의 추론 일 경우 추론이라고 반드시 명시.»
3. «새로운 ai 트랜드 용어가 나올 경우 용어의 어원, 6하원칙에 입각한 설명, 박정훈이 어떻게 활용 하면 더 좋은 시너지를 낼 수 있을지 분석해서 설명하는 .md를 만들어 주시고 C:\Users\745ra\OneDrive\바탕 화면\Ai 용어 트랜드폴더에 저장하여 주세요.»
   - 클라우드 세션은 PC 폴더에 저장할 수 없어 저장소 `ai-terms/`에 만들었습니다: `ai-terms/LLM-Council.md`, `ai-terms/Llama.md`.
   - **Council 2 할 일**: 두 파일을 위 Windows 폴더로 복사 (로컬 세션은 직접 저장 가능). 앞으로 새 용어는 그 폴더에 바로 저장.

### 2-2. 일하는 방식에 대한 선호 (대화에서 드러난 것)
- **인터뷰식 확인을 선호**: 선택지 질문으로 결정하고, 모르는 부분은 «더 자세한 인터뷰가 필요합니다»라고 답함. 결정 전 장단점·근거를 먼저 원함.
- **실측 우선**: Council 2 보고서처럼 «[미실측]»·«[미확인]»을 구분하는 것을 기대함. "로그인하면 된다"처럼 시험 안 한 주장을 사실처럼 쓰면 안 됨 (Gemini 건에서 Council 1이 틀림).
- **자동화 지향**: «수동 조작을 하지 않을 뿐이죠» — 사람이 붙여넣는 단계보다 자동 보조를 원함. 단, 대표님이 **지켜보는 상태**가 전제(D17).
- **이해 확인 질문을 자주 함**: "이유가 있나요?", "이상 없나요?" → 이유가 없으면 "특별한 이유 없음"이라고 솔직히 답하고, 점검 결과를 표로 보여주는 방식이 잘 받아들여졌음.
- 답변·문서는 **한국어**. 쉬운 말로, 사실과 추론을 표시.

### 2-3. 금지·주의
- **API 키·토큰을 채팅이나 파일에 쓰지 않음.** 키는 대표님이 Windows 환경변수에 직접 등록 (SKILL.md 규칙 8).
- **사이트 탐지 회피·흔적 숨기기 기능은 만들지 않음** (①의 버린 것 참고). 브라우저 보조는 대표님이 보는 앞에서만, 로그인·CAPTCHA·동의 화면은 대표님에게 넘김.
- **유료 위원은 대표님 요청 전까지 실행 금지** (D14). OpenRouter 충전, xAI 데이터 공유 크레딧(학습 동의, 되돌릴 수 없다는 보고), Perplexity·Grok API 모두 포함.
- **기존(부진) 채널 분석은 요청 시에만** (D12).
- **PR 생성은 요청받지 않음** — 아직 main에 합치는 PR을 만들지 않았음.

### 2-4. 대표님 배경 (README 기준, 분석·제안에 활용)
- 24년 B2B 기술 영업(Intel·ASUS·CJ) → AI 엔지니어 전환 중, ACL 2025 Biomedical Co-Scientist Agent 공동 제1저자, AIGEN 3B Biomedical Agent(GDPO·SFT·Uncertainty Head), AIFFEL 15기, KAIST AIP 3기.
- 매일 루틴: LeetCode Easy 1문제, GDPO.py 50줄 한국어 주석, GitHub 커밋 (README "Daily Learning Routine").
- PC: AMD Ryzen 7 8700G + Radeon 780M(내장), RAM 32GB, Windows 11 Home.
- 계정: Claude Max(유료), Google AI Pro(유료, 단 Gemini CLI에는 소용없음), ChatGPT·meta.ai·perplexity.ai·grok.com은 무료 계정.
