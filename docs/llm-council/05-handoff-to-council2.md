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

---

## ③ 미완료·보류 작업과 다음 단계

| # | 작업 | 상태 | 누가 | 다음 행동 |
|---|---|---|---|---|
| T1 | Gemini `model` 확정 | Council 2가 실측 중 (아래 참고) | Council 2 + 대표님 | 안정적인 Flash 모델을 대표님과 정해 `members.json`의 `gemini.model`에 기록 |
| T2 | **429·503 재시도(지수 백오프)** | 없음 — `call_openai_compatible`이 한 번 실패하면 끝. 의장 고정이라 503 한 번에 3단계 정지 | Council 2 (예정이라고 보고) | 구글 권고대로 지수 백오프 재시도 추가 ([Gemini API 문제 해결](https://ai.google.dev/gemini-api/docs/troubleshooting)) + 테스트 |
| T3 | 테스트 정리 | `OpenAICompatibleTest.tearDown`에 `server.shutdown()`만 있고 `server_close()` 없음 → ResourceWarning 4건 (Council 2 보고, 시험 코드만) | Council 2 | `server_close()` 추가 |
| T4 | 회의 보류 해제 | 의장 Gemini 준비 전까지 보류 (D21) | Council 2 | T1 후 `check --ping`에서 `의장: gemini — 설정 확인됨` + 성공 확인 |
| T5 | 04 체크리스트 6~8단계 | 미실행 (Chrome 연결, CLI 위원만 연습 회의, 브라우저 포함 연습 회의) | Council 2 + 대표님 | 순서대로 실행, 결과를 Decision Log·문서에 기록 |
| T6 | Windows 병렬 실행 확인 | 단위 테스트는 통과(Council 2), 실제 위원 병렬은 미확인 | Council 2 | 연습 회의 출력의 위원별 `(N초)` 비교 |
| T7 | `ai-terms/*.md` PC 폴더 복사 | 미완 | Council 2 | ②의 2-1 참고 |
| T8 | 매일 트렌드 루틴 (D9) | 설계만 (01 문서 5장), 미구현 | Council 2 + 대표님 결정 | 무인 실행이면 브라우저 위원은 자동 생략(SKILL.md). Windows 작업 스케줄러 + `claude -p "/llm-council …"` 같은 바깥 실행은 중첩 문제 없음 [추론] |
| T9 | Phase B 데이터 레이어 | 미착수 | Council 2 + 대표님 | YouTube Data API 키 발급(대표님), 채널·영상 스냅샷 스크립트, Playboard 산식·약관 확인 |
| T10 | 채점 기준 개선 | 초안 v0.1 | 회의 후 | 첫 회의 결과와 실제 성과를 비교해 `rubrics/` 수정 |
| T11 | main 병합 PR | 요청 없음 | 대표님 결정 | 요청 시 PR 생성 |
| T12 | 유료 위원 결정 | 보류 (D14) | 대표님 | Grok(API 종량제 vs SuperGrok+Grok Build CLI), Perplexity API, OpenRouter $10, Meta Model API — 요청 시 재검토 |
| T13 | Meta Model API 한국 가입 가능 여부 | Council 1이 대표님께 확인 요청했으나 답 없음 | 대표님 | 유료 보류와 함께 대기 |
| T14 | Codex 무료 계정 한도 | 미확인 | Council 2 | 연습 회의를 반복하며 한도 오류 여부 관찰 |

**Council 2가 이미 한 것 (Council 2 보고 그대로, 중복 불필요)**
- `0216f6e` pull, 단위 테스트 16개 OK.
- `GEMINI_API_KEY` 등록, AI Studio 결제 등급 «무료 등급», `models gemini --filter flash` → 26개.
- 실호출 8회: 3.8-flash 1/3 성공(나머지 HTTP 503 혼잡), 3.7-flash 1/2, 3.5-flash 2/2, flash-latest 1/1(70초). 같은 모델이 몇 초 사이 성공→503 → 일시 혼잡.
- Codex: ChatGPT 로그인 완료, ping ✓ 7.6초.

---

## ④ 알려진 결함·의심 지점·시험 안 한 경로

### 4-1. 코드 결함·약점
- **재시도 없음** (T2). 503이 잦은 무료 등급 + 의장 고정 조합에서 가장 큰 위험.
- **`new`의 회의 보류 확인은 정적 점검**: 환경변수·model 값만 보고 실제 호출은 안 함 → 통과해도 회의 중 의장 호출이 실패할 수 있음. 회의 전 `check --ping` 권장.
- **반론자(Devil's Advocate) 순환**: `devil_advocate_rotation`이 `codex → gemini → claude` 순. 그 회의의 반론자가 2단계에서 실패하면 그 회의엔 반론이 없음 (대체 지정 로직 없음).
- **자기소개 가리기 정규식**: "I am Claude", "저는 Gemini", "As ChatGPT," 형태만 가림. 다른 표현(예: "Google이 만든 모델로서")은 통과할 수 있고, 반대로 "나는 Meta …" 같은 일반 문장을 잘못 가릴 수도 있음. 실제 출력으로 시험 안 함.
- **`FINAL RANKING` 파싱**: 마지막 `FINAL RANKING` 줄의 대문자 한 글자만 읽음. 모델이 "최종 순위:"처럼 바꿔 쓰면 읽기 실패 → `aggregate`가 실패 수를 알려줌. 실제 모델 출력으로 시험 안 함.
- **의장 Gemini의 자기 선호 가능성**: Gemini도 1단계 답을 내므로 익명이어도 자기 답을 알아볼 수 있음 ([Panickssery et al., 2024](https://arxiv.org/abs/2404.13076)). 기록이 쌓이면 Gemini 답의 채택 빈도 점검 권장.
- **병렬 테스트의 시간 조건**(`< 4.0초`)은 느린 PC에서 흔들릴 수 있음.
- **`--prepare` 후 재실행 시 질문 파일 보존**은 "내용이 같으면 다시 쓰지 않음"으로 해결했지만, 회의 도중 자료표(fact-sheet)를 고치면 질문 파일이 바뀌어 위원마다 다른 질문을 받을 수 있음 → 회의 시작 후 자료표 수정 금지 [추론].

### 4-2. 시험 안 한 경로 (클라우드에서 불가했던 것)
- Claude in Chrome으로 meta.ai·perplexity.ai·grok.com 질문 전송·답변 복사 (화면 구조, 긴 답변·출처 링크 복사 정확도, 사이트별 첫 권한 화면) — 전부 미시험.
- Claude Code의 Agent(서브에이전트)·Bash 백그라운드 동시 실행 — 로컬 버전에서 미시험. 안 되면 차례 실행으로 대체(SKILL.md 2-4).
- Codex에 **긴 한국어 프롬프트**를 표준입력으로 넣는 실제 회의 호출 — ping(짧은 영어)만 성공.
- Gemini API 의장 프롬프트(답변 전부 + 평가 전부가 들어가는 긴 입력)의 길이·시간 — 미시험. 무료 등급 토큰 한도에 걸릴 수 있음 [추론].
- 1~5단계 전체 실제 회의 — 한 번도 실행 안 됨 (가짜 위원 테스트만 통과).
- Windows 레거시 콘솔에서 한글 출력 — 미시험 (스크립트는 UTF-8로 출력 재설정).

---

## ⑤ 검증 안 된 주장 목록

검증 단계: **[미확인]** 출처 없음·찾지 못함 / **[2차]** 서드파티·검색 요약만 확인, 1차 원문 미확인 / **[상충]** 출처끼리 다름 / **[추론]** Claude 판단

| # | 주장 | 단계 | 근거·출처 | 현재 상태 |
|---|---|---|---|---|
| U1 | OpenRouter `:free` 모델: 분당 20회, 하루 50회(구매 $10 미만)·1,000회($10 이상) | [2차] | [OpenRouter Limits](https://openrouter.ai/docs/api-reference/limits) (검색 요약, 페이지 직접 열람 실패) | 유료 보류라 미사용 |
| U2 | ChatGPT 무료 플랜에도 Codex 포함 | [2차] | [OpenAI Help](https://help.openai.com/en/articles/11369540-codex-usage-limits) | PC에서 로그인·ping 성공 → **사용 가능은 실측됨**, 무료 한도는 [미확인] |
| U3 | Gemini 무료 등급은 Flash 위주, Pro 제외 | [상충] | [Klymentiev](https://klymentiev.com/blog/gemini-api-free-tier), [GeoToolbox](https://geotoolbox.ai/blog/gemini-api-pricing) | Council 2 실측: 무료 키로 Flash 계열 응답 성공 |
| U4 | Gemini 무료 등급 입력은 구글 제품 개선에 사용 | [2차] | 위 두 자료가 공식 요금표 문구 인용 | 공식 요금 페이지 직접 열람 실패 |
| U5 | 무료 API 키도 "API 키 인증 영향 없음"에 포함 | [미확인]→**실측으로 부분 해소** | 공지는 "API key authentication"만 언급 ([#28017](https://github.com/google-gemini/gemini-cli/discussions/28017)) | Council 2 실측: 무료 키로 API 직접 호출 성공 (CLI 경유는 미사용) |
| U6 | Groq가 2026-08-16 Llama 무료 등급 종료 | [2차] | [Groq Deprecations](https://console.groq.com/docs/deprecations) (검색 경유), [ECorpIT](https://ecorpit.com/groq-llama-3-3-70b-shutdown-qwen3-6-27b-preview-replacement-2026/) | 미사용 |
| U7 | Meta Model API: 2026-07-09 공개, 신규 $20 크레딧, 미국 개발자 대상, Muse Spark 1.3 $1.25/$4.25 | [2차] | [AIChatDaily](https://www.aichatdaily.com/ai-models/meta-opens-muse-spark-1-1-developers-via), [FourWeekMBA](https://fourweekmba.com/ai-meta-muse-spark-1-1-meta-model-api-closed-pivot/), [eesel](https://www.eesel.ai/blog/muse-spark-1-3-pricing) | 한국 가입 여부 [미확인] |
| U8 | Perplexity Pro 구독자 월 $5 API 크레딧 | [상충] | [Perplexity Help](https://hub-prod.perplexity.ai/hub/faq/pplx-api) vs [Community](https://community.perplexity.ai/t/perplexity-pro-bonus-for-the-api-is-set-to-zero/51) | 구독 안 함(D15) |
| U9 | Perplexity Sonar Chat Completions 2026-09-27 종료 → Agent API | [2차] | [CloudZero](https://www.cloudzero.com/blog/perplexity-api-pricing/) | 유료 보류 |
| U10 | Meta·Perplexity 약관의 자동화 관련 조항 | [2차] | ConductAtlas 정리 자료만 ([Meta](https://conductatlas.com/platform/meta/meta-terms-of-service/provision/CA-P-017687/no-automated-data-collection-without-permission/), [Perplexity](https://conductatlas.com/platform/perplexity-ai/perplexity-terms-of-service/provision/CA-P-049606/prohibition-on-scraping-or-automated-data-extraction/)) — 원문 페이지 열람 실패 | 대표님이 사이트 하단 Terms로 직접 확인 권장 |
| U11 | Grok Build CLI 이용 등급(SuperGrok Heavy 전용 vs SuperGrok·X Premium+) | [상충] | [The Decoder](https://the-decoder.com/x-ai-plays-catch-up-with-grok-build-its-first-terminal-based-coding-agent/), [CodeAgentSwarm](https://www.codeagentswarm.com/en/guides/how-to-use-grok-build) | 유료 보류 |
| U12 | Grok 4.7 $2/$6, X 검색 게시물 1,000개당 $5(2026-09-21~), 데이터 공유 크레딧 월 $150(되돌릴 수 없음) | [2차] | [MorphLLM](https://www.morphllm.com/grok-api-pricing), [RuntimeWire](https://runtimewire.com/article/xai-is-changing-the-economics-of-x-search-runtimewire-was-built-for-a-narrower-r), [agentdeals](https://agentdeals.dev/vendor/xai) | 유료 보류 |
| U13 | 무료 Colab 금지 항목(웹 서비스·프록시·SSH 등) | [2차] | [Prodigy 포럼 인용](https://support.prodi.gy/t/is-it-possible-to-install-prodigy-on-google-colab-pro/5416/4), [ColabGeek](https://pypi.org/project/ColabGeek) | 공식 FAQ 열람 실패 |
| U14 | Kaggle 주당 약 30 GPU시간, 세션 12시간(9시간 설도) | [상충] | [gpuperhour](https://gpuperhour.com/blog/free-cloud-gpus-and-credits), [PyPI kgz](https://pypi.org/p/kgz) | — |
| U15 | 780M에서 8B 모델 약 15 tok/s | [추론] | 32B 실측 4 tok/s를 크기 비율로 외삽 | 실측 필요 |
| U16 | YouTube `videos.list` 요청당 최대 50개 ID | [2차] | [OutlierKit](https://outlierkit.com/resources/youtube-api-quota/) | 호출당 1 unit은 [Google 공식](https://developers.google.com/youtube/v3/docs/videos/list) |
| U17 | Playboard 성장(growth) 순위의 산식과 자동 수집 허용 여부 | [미확인] | [Apify 스크래퍼 설명](https://apify.com/maximedupre/playboard)에 growth 지표가 있다는 것만 확인 | Phase B 전 확인 |
| U18 | 회의 1회 비용 추정($0.01~0.19, 확장 시 $0.02~0.05) | [추론] | 01·02 문서 계산 | 유료 미사용 |
| U19 | Claude in Chrome의 사이트별 첫 권한 화면, 각 사이트 로그인 유지 기간 | [미확인] | [Claude Code Chrome 문서](https://code.claude.com/docs/en/chrome)는 권한 관리만 언급 | T5에서 확인 |
| U20 | Karpathy llm-council 공개일 2025-11-22 | [2차] | [Blockchain News](https://blockchain.news/ainews/llm-council-web-app-multi-model-ai-response-evaluation-using-openrouter-for-enhanced-model-comparison) | 용어 문서에만 사용 |
| U21 | 중첩 `claude -p` 차단·멈춤 | [2차] | GitHub 이슈 미러 ([#26190](https://claudeissues.com/issue/26190-nested-claude-p-instances-hang-when-claudecode-env-var-is-inherited), [#29543](https://claudeissues.com/issue/29543-bug-claude-print-produces-no-output-when-claudecode-env-var-is-unset-inside-a-se)) | 서브에이전트로 회피 |
| U22 | 안내서 소요 시간(단계별 분) | [추론] | 03 가이드 3장 | 첫 회의로 실측 |

**과거에 틀렸던 것 (재발 방지)**: "Google AI Pro + Gemini CLI 하루 1,500회", "Gemini는 Google 로그인하면 된다", "Groq 무료로 Llama" — 모두 Council 1이 종료·변경 공지를 확인하지 않고 썼다가 정정함. **유료·무료 정책은 회의 전 최신 공지로 다시 확인.**

---

## ⑥ 첫 안건 «최근 6~12개월 글로벌 급성장 채널 분석»에 대해 모은 것

**자료표(fact-sheet)는 아직 만들지 않았습니다.** 아래는 자료를 모을 때 쓸 출처와 생각입니다.

### 6-1. 확인된 데이터 출처와 제약
- **Playboard**: 국가·카테고리별 순위와 성장(growth) 순위 제공. 인기 순위는 최근 등록 영상의 조회수·좋아요 기반이며 점수 = 조회수 + 좋아요×10, 구독자 수는 하루 1번 갱신, 구독자 1,000명·누적 조회수 100만 이상 채널만 순위에 듦 ([Playboard About](https://playboard.co/en/about), 검색 요약) [2차]. 성장 산식은 [미확인].
- **YouTube Data API**: 하루 10,000 unit, `search.list` 100 unit, `videos.list`·`channels.list` 1 unit ([Google 공식](https://developers.google.com/youtube/v3/determine_quota_cost)). 구독자 수는 앞 3자리 반올림, **과거 이력 없음** → 직접 스냅샷 필요 ([Rival IQ](https://help.rivaliq.com/en/articles/9788197-why-youtube-subscriber-counts-are-rounded), [ChannelCrawler](https://channelcrawler.com/insights/beyond-the-youtube-data-api-access-historical-channel-data-trends-channelcrawler)). 지역별 인기 영상은 `videos.list`의 `chart=mostPopular` ([Google 공식](https://developers.google.com/youtube/v3/docs/videos/list)).
- **vidIQ**: 국가별 최다 구독 채널 목록을 매일 갱신 (교차 확인용, 성장률 아님) ([vidIQ](https://vidiq.com/youtube-stats/top/country/kr/)) [2차].
- **채점 기준**: `council/rubrics/youtube-growth.md` (데이터 근거 30%, 재현 가능성 20%, 수익화 연결 20%, 생존자 편향 점검 15%, 실행 계획 15%).

### 6-2. 생각 [추론]
1. **"급성장"부터 정의**: 개설·첫 업로드 12개월 이내 + 최근 90일 **조회수** 증가율 상위 + 영상당 평균 조회수. 구독자는 반올림 값이라 보조 지표로만 (01 문서 4.2).
2. **영어권 국가부터**: Playboard 미국·영국·캐나다·호주 등 성장 순위에서 후보 20~50개 → API로 채널·최근 영상 지표 수집 → 2~4주 매일 스냅샷 후 판단하면 일시 급등을 거를 수 있음.
3. **비교군 필수**: 같은 주제·같은 시기에 시작했지만 크지 못한 채널 일부를 넣어 생존자 편향을 줄임 ([Survivorship bias](https://en.wikipedia.org/wiki/Survivorship_bias)).
4. **수익화 단서 기록**: 스폰서 표기, 제휴 링크, 자체 상품, 멤버십 여부를 채널별로 표에 기록 → 채점 기준 "수익화 연결" 항목의 근거.
5. **대표님 자산과 연결**: B2B 영업·AI 연구 경력이 강점이 되는 주제(예: AI 도구 실무, 커리어 전환)가 후보에 있으면 재현 가능성 점수에 반영하되, 이는 자료가 아니라 가설로 표시.
6. 자료표 행마다 출처·수집일 필수, 무료 Gemini에 넘어가므로 비공개 정보 금지 (SKILL.md 규칙 8).

---

## 이어받는 방법 (Council 2용 요약)

1. 이 문서 → `council/README.md` → `.claude/skills/llm-council/SKILL.md` → `council/members.json` 순으로 읽기.
2. 설계 배경은 `docs/llm-council/01~02`, 사용법은 `03`, Windows 시험 절차는 `04`.
3. 첫 작업 추천 순서 [추론]: T2(재시도) → T3 → T1(모델 확정) → T4(보류 해제) → T5~T6(연습 회의) → 첫 안건.
4. Council 1은 이 커밋 이후 이 브랜치를 수정하지 않습니다.
