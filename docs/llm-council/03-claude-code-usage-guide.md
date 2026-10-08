# Claude Code에서 LLM Council 사용 가이드 (v1.0)

> 작성일: 2026-10-08 · 대상: 박정훈 (Windows 11, Claude Max·Google AI Pro, ChatGPT·Meta AI·Perplexity·Grok 무료 계정)
>
> **표기 규칙** — 링크 = 출처로 확인한 사실 / 🧪 = 이 작업 환경에서 직접 실행해 확인 / 🔎 **[Claude 추론]** = 출처 없는 판단 / ⚠️ = 확인 필요

---

## 0. 한 장 요약

```
/llm-council <안건>
   │
   ├─ 1. 자료 정리   Claude Code가 출처 있는 자료표(fact-sheet) 작성 → 내가 확인
   ├─ 2. 독립 의견   Gemini·GPT(자동) + Claude(서브에이전트) + Meta AI·Perplexity·Grok(브라우저) — 모두 동시에
   ├─ 3. 익명 평가   이름 가린 답변을 Gemini·GPT·Claude가 채점·순위 (반론자 1명)
   ├─ 4. 의장 종합   Gemini 의장(고정) → 결론·소수 의견·확신도
   └─ 5. 기록        decision-log.md → 나중에 "실행 결과" 기입
```

**내가 할 일**은 ① 안건 입력 ② 자료 확인 ③ 브라우저 작업 지켜보기(로그인·CAPTCHA가 나오면 처리) ④ 결과 읽고 실행 — 네 가지입니다. 나머지는 Claude Code가 자동으로 진행합니다.

---

## 1. 처음 한 번만: 준비 (Windows PowerShell)

### 1.1 설치 확인
```powershell
node -v          # Node.js가 없으면 https://nodejs.org 에서 LTS 설치
python --version # 3.10 이상. 없으면 https://www.python.org/downloads/
```

### 1.2 위원 연결: Codex 로그인 + Gemini API 키
```powershell
npm install -g @openai/codex
codex login      # 브라우저가 열리면 ChatGPT 계정으로 로그인
```
- 🧪 2026-10-08 기준 Codex CLI `0.161.0`. 로그인 방식: [Codex Auth](https://developers.openai.com/codex/auth)
- ✅ PC 실측(다른 세션 보고): `check --ping`에서 `✓ codex: 성공 (7.6초)`.

**Gemini (API 키 방식)** — ⚠️ **정정(2026-10-08)**: 이전 판에서 "Gemini CLI에 Google 로그인"을 안내했으나, 2026-06-18부터 개인 계정의 Gemini CLI가 중단되어 PC에서 `IneligibleTierError: This client is no longer supported for Gemini Code Assist for individuals`로 거절되었습니다. 제가 종료 공지를 확인하지 않고 쓴 오류입니다.

1. [Google AI Studio](https://aistudio.google.com)에 Google 계정으로 로그인해 **API 키**를 만듭니다 ([Gemini API 키 문서](https://ai.google.dev/gemini-api/docs/api-key)).
2. 키를 Windows 환경변수 `GEMINI_API_KEY`에 넣습니다: Windows 검색에서 "계정의 환경 변수 편집" → 새로 만들기 → 이름 `GEMINI_API_KEY`, 값에 키. (명령어로 넣으면 PowerShell 기록에 남으므로 이 화면을 권장. **키를 Claude Code 채팅에 붙여넣지 마세요.**)
3. PowerShell과 Claude Code를 **새로 엽니다** (환경변수는 새로 연 창부터 적용).
4. 쓸 수 있는 모델 확인: `python council/scripts/council.py models gemini --filter flash`
5. 목록에서 Flash 모델 ID 하나를 골라 `council/members.json`의 `gemini` → `model`에 적습니다 (또는 Claude Code에 "members.json의 gemini 모델을 <ID>로 바꿔줘").
6. `python council/scripts/council.py check --ping` → `✓ gemini: 성공`과 `의장: gemini — 설정 확인됨`이 나오면 회의를 열 수 있습니다.

- 2026-06-18부터 무료·Google AI Pro·Ultra 개인 계정의 Gemini CLI 사용이 중단되었고, API 키 인증은 영향이 없습니다 ([Gemini CLI 공식 공지 #28017](https://github.com/google-gemini/gemini-cli/discussions/28017)). 그래서 Gemini는 CLI 대신 **API 키로 스크립트가 직접** 부릅니다 ([Gemini OpenAI 호환 문서](https://ai.google.dev/gemini-api/docs/openai)).
- 무료 등급은 Flash 계열 위주이고, 무료 등급 입력은 구글 제품 개선에 쓰일 수 있습니다 ⚠️ 출처 간 세부 차이 있음 ([Klymentiev](https://klymentiev.com/blog/gemini-api-free-tier), [GeoToolbox](https://geotoolbox.ai/blog/gemini-api-pricing)). 자료표에 비공개 정보를 넣지 마세요.
- **의장(gemini)이 준비되기 전에는 `new`가 회의를 시작하지 않습니다(회의 보류, 사용자 결정).**

### 1.3 저장소 받기
Council 파일은 현재 브랜치 `claude/llm-concile-usage-interview-pnttr8`에 있습니다.
```powershell
git clone https://github.com/nous-zero/nous-zero.git
cd nous-zero
git checkout claude/llm-concile-usage-interview-pnttr8
```
🔎 [Claude 추론] 써 보고 만족스러우면 이 브랜치를 main에 합치는 PR을 만들면, 이후에는 `git checkout` 없이 main에서 바로 쓸 수 있습니다.

### 1.4 연결 점검
```powershell
python council/scripts/council.py check
```
정상이라면 다음처럼 보입니다 (🧪 이 환경의 출력 형식):
```
- claude           [사용] subagent           Claude Code 서브에이전트가 응답을 채움
- gemini           [사용] openai_compatible  환경변수 GEMINI_API_KEY: 설정됨
- codex            [사용] command            명령 codex: 있음 (...)
- meta-ai          [사용] manual             사용자가 브라우저 답변을 붙여넣음
- perplexity       [사용] manual             ...
- grok-web         [사용] manual             ...
```
`없음`이 나오면 8장 문제 해결을 보세요.

### 1.5 첫 실험: 실제 응답 확인

> 단계별 통과 기준이 있는 전체 체크리스트는 [04-windows-local-test.md](./04-windows-local-test.md)에 있습니다.

로그인까지 마쳤다면 회의 전에 위원들이 실제로 답하는지 시험합니다.

```powershell
python council/scripts/council.py check --ping
```
- 켜져 있는 자동 위원(Gemini·Codex)에게 `Reply with exactly one word: OK`를 보내고 위원별 성공·실패와 걸린 시간을 보여줍니다. 위원마다 최대 180초 기다립니다(`--ping-timeout`으로 조절).
- 성공하면 `✓ gemini: 성공 (… 초) - OK`처럼, 실패하면 `! gemini: 실패 … - <오류>`처럼 나옵니다. 마지막 줄의 `의장: gemini — 설정 확인됨`을 꼭 확인하세요.
- 둘 다 성공하면 **연습 회의**를 한 번 엽니다. 가벼운 안건으로 전체 흐름을 확인하는 용도입니다.
  ```
  /llm-council 연습: 아침 루틴에서 LeetCode와 GDPO 주석 중 무엇을 먼저 할까
  ```
  처음에는 "이번엔 브라우저 위원 생략"이라고 해서 CLI 위원만으로 끝까지 가 보고, 그다음 회의에서 브라우저 보조를 켜는 순서를 권합니다(🔎 [Claude 추론] 문제가 생겼을 때 원인을 나눠 찾기 쉬움).
- 실패하면 오류 문구를 Claude Code에 그대로 붙여넣어 주세요.

### 1.6 (선택) 브라우저 보조를 쓰려면: Claude in Chrome 연결
- Chrome(또는 Edge)에 Claude 확장 프로그램을 설치하고, Claude Code를 `claude --chrome`으로 시작하거나 세션 중에 `/chrome`을 실행합니다. `/chrome`에서 "Enabled by default"를 고르면 매번 플래그를 붙이지 않아도 됩니다 ([Claude Code Chrome 문서](https://code.claude.com/docs/en/chrome)).
- 브라우저 작업은 새 탭에서, 내가 볼 수 있는 Chrome 창에서 실시간으로 진행되고, 이미 로그인된 상태를 그대로 씁니다. 로그인 화면이나 CAPTCHA가 나오면 멈추고 나에게 넘깁니다 ([Claude Code Chrome 문서](https://code.claude.com/docs/en/chrome)).
- 지원 브라우저는 Google Chrome과 Microsoft Edge(베타)이며 WSL에서는 지원되지 않습니다 ([Claude Code Chrome 문서](https://code.claude.com/docs/en/chrome)).
- 사전에 meta.ai, perplexity.ai, grok.com에 로그인해 두세요.

---

## 2. 회의 열기

`nous-zero` 폴더에서 Claude Code를 실행하고 입력합니다.
```
/llm-council 최근 6~12개월 글로벌 급성장 채널 분석
```
- 프로젝트의 `.claude/skills/` 폴더에 있는 스킬은 그 저장소에서 Claude Code를 실행하면 불러와지고, 스킬의 `name`이 `/명령어`가 됩니다 ([Claude Code Skills 문서](https://code.claude.com/docs/en/skills)).
- `/llm-council`을 쓰지 않고 "이 안건으로 카운슬 열어줘"라고 말해도 스킬 설명과 맞으면 Claude가 불러올 수 있습니다 ([Claude Code Skills 문서](https://code.claude.com/docs/en/skills)).

---

## 3. 단계별로 무슨 일이 일어나나

| 단계 | Claude Code(진행자)가 하는 일 | 내가 할 일 | 소요 시간 (🔎 추정) |
|---|---|---|---|
| 0. 점검 | `check` 실행, 꺼진 위원 알림 | — | 수초 |
| 1. 자료 | run 폴더 생성, 웹 검색 등으로 **출처 있는 자료표** 작성 | 자료 요약을 보고 빠진 데이터 알려주기 | 5~15분 |
| 2. 독립 의견 | 프롬프트를 먼저 모두 만든 뒤 **동시에** 진행: Gemini·Codex 병렬 호출(백그라운드) + Claude 서브에이전트 + 브라우저 탭 3개에 질문 전송 → 답이 끝나는 대로 저장 | 브라우저 작업 지켜보기 (4장) | 가장 느린 위원 기준 (🔎 5~10분) |
| 3. 익명 평가 | 답변에 무작위 라벨(Response A, B…) 부여, 평가자마다 순서 섞기, 반론자 지정 → Gemini·Codex·Claude 평가 **동시 진행** → 순위 집계 | — | 3~8분 |
| 4. 의장 종합 | **Gemini 의장(고정)** 이 익명 답변·평가·순위를 보고 결론 작성 | — | 2~5분 |
| 5. 기록 | `decision-log.md` 생성, 결과 보고, 커밋 여부 질문 | 결과 읽기, 커밋 여부 답하기 | — |

- 진행자는 **의견을 내지 않고**, 위원 답변을 고치거나 요약해서 넘기지 않습니다. Claude의 의견은 진행자와 분리된 서브에이전트가 냅니다 ([SKILL.md](../../.claude/skills/llm-council/SKILL.md) 규칙).
- Claude Code 안에서 `claude -p`를 다시 부르면 중첩 세션 차단에 걸리거나 멈추는 사례가 보고되어 서브에이전트 방식을 씁니다 ([claudeissues #26190](https://claudeissues.com/issue/26190-nested-claude-p-instances-hang-when-claudecode-env-var-is-inherited)).

---

## 4. 브라우저 위원(Meta AI·Perplexity·Grok) 참여 방식

기본값은 **A. 브라우저 보조(자동)** 입니다(`council/members.json`의 `settings.browser_mode`: `assist`). Chrome이 연결되지 않았거나 사람이 없는 무인 실행이면 Claude가 C(생략)로 바꾸고 알려줍니다. 회의 중에 "이번엔 직접 붙여넣을게"처럼 말하면 그 회의만 바뀝니다. 기본값을 바꾸려면 `browser_mode`를 `paste`·`skip`·`ask`(매번 묻기) 중 하나로 고칩니다.

| 방식 | 언제 | 진행 |
|---|---|---|
| **A. 브라우저 보조** | Claude in Chrome이 연결되어 있고, 화면을 지켜볼 수 있을 때 | Gemini·GPT 호출과 **동시에** Claude가 세 사이트를 새 탭으로 열어 질문을 모두 먼저 보내고 → 탭을 돌며 끝난 답변을 전체 복사해 저장. 로그인·CAPTCHA·동의 화면·유료 안내가 나오면 그 탭만 멈추고 나에게 넘김 |
| **B. 직접 붙여넣기** | 확장 프로그램이 없거나 직접 하고 싶을 때 | `council/runs/<회의>/stage1/prompts/meta-ai.md` 등을 열어 전체 복사 → 사이트에 붙여넣기 → 받은 답변을 Claude Code 채팅에 붙여넣으며 "meta-ai 답변"이라고 알려주기 → Claude가 원문 그대로 저장 |
| **C. 생략** | 바쁠 때 | Claude·Gemini·GPT 3개 답변만으로 진행 (최소 2개 필요) |

- 브라우저 위원은 복사·붙여넣기 부담을 줄이려고 **Stage 1(독립 의견)에만** 참여합니다. 평가는 Gemini·GPT·Claude가 합니다.
- 🔎 [Claude 추론] 사이트마다 **새 대화**에서 시작해야 이전 대화의 맥락이 섞이지 않습니다.
- ⚠️ 각 사이트 약관의 자동화 관련 조항은 원문으로 확인하지 못했습니다. A 방식을 쓰기 전에 각 사이트 하단의 Terms 링크를 한 번 확인하세요.

---

### 4.1 의장: Gemini 고정 (2026-10-08 사용자 결정)

- 의장은 항상 Gemini입니다(`council/members.json`의 `settings.chair_rotation: ["gemini"]`). 스크립트가 Gemini API(키 방식)로 자동 실행하므로 의장 단계에서 내가 할 일은 없습니다. **Gemini가 연결되기 전에는 회의를 열지 않습니다(회의 보류, 사용자 결정)** — `new`가 의장 준비를 확인하고 막습니다.
- 원본 llm-council의 기본 의장도 Gemini 3 Pro입니다 ([karpathy/llm-council](https://github.com/karpathy/llm-council)).
- 의장 호출이 실패하면 Claude가 다른 위원으로 바꾸지 않고 오류를 보고한 뒤 다시 시도합니다. 한 회의만 바꾸고 싶으면 "이번 회의 의장은 claude로"라고 말합니다.
- 참고: LLM 평가자는 자기가 쓴 글을 알아보고 더 높게 평가하는 경향이 있습니다 ([Panickssery et al., NeurIPS 2024](https://arxiv.org/abs/2404.13076)). Gemini도 위원으로 답을 내므로, 🔎 [Claude 추론] 익명화·채점 기준·소수 의견 기록이 이 영향을 줄이는 장치입니다. 기록이 쌓이면 Gemini 답변(익명 해제 표로 확인)이 최종 결론에 지나치게 자주 채택되는지 점검해 볼 수 있습니다.

## 5. 결과 읽는 법 (`decision-log.md`)

| 섹션 | 볼 것 |
|---|---|
| 의장 종합 | 최종 결론, 근거(어느 Response에서 왔는지), 평가 기준별 판단 |
| 소수 의견 | 채택되지 않은 주장과 이유 → **나중에 맞았는지 꼭 확인** |
| 확신도 | 상·중·하. "하"면 "추가로 필요한 데이터"를 모아 재회의 |
| 순위 집계 | 평균 순위(낮을수록 좋음). 참고용이며 결론은 다수결이 아님 |
| 익명 해제 | 어떤 위원이 어떤 Response를 썼는지 — 회의가 끝난 뒤에만 공개 |
| 실행 결과 (추후 기입) | 실행한 행동, 결과 지표, 결론이 맞았는지 → 다음 회의의 채점 기준 개선 재료 |

---

## 6. 자주 쓰는 요청 예시

| 상황 | Claude Code에 이렇게 말하기 |
|---|---|
| 첫 안건 | `/llm-council 최근 6~12개월 글로벌 급성장 채널 분석` (Claude가 YouTube 채점 기준 `youtube-growth`를 제안) |
| 자료를 먼저 같이 모으기 | "카운슬 열기 전에 자료표부터 같이 만들자. 이 데이터도 넣어줘: …" |
| 의장 바꾸기 (한 회의만) | "이번 회의 의장은 claude로" (기본은 Gemini 고정) |
| 브라우저 위원 빼기 | "이번엔 브라우저 위원 생략하고 진행" |
| 중단된 회의 이어가기 | "council/runs/<회의 폴더> 이어서 진행해줘" (Claude가 `status`로 빠진 단계 확인) |
| 결과 기록 | "<회의 폴더> decision-log에 실행 결과 기록: 조회수 …" |
| 채점 기준 고치기 | "youtube-growth 루브릭에 '제작 비용' 항목 추가하자" |
| 기존 채널 진단 (요청 시에만) | "/llm-council 기존 채널 부진 원인 진단" |

---

## 7. 지키는 규칙

1. **유료 위원 보류**: Grok API·Perplexity API 등 `"paid": true` 위원은 내가 요청하기 전까지 실행하지 않습니다.
2. **사실과 추론 구분**: 자료표의 모든 행에 출처를 적고, 출처가 없으면 `[추론]`으로 표시합니다. 결과 보고도 같습니다.
3. **원문 보존**: 위원 답변은 한 글자도 바꾸지 않고 저장합니다.
4. **최소 2개**: 독립 의견이 2개 미만이면 평가 단계로 가지 않습니다.
5. **기존 채널 진단은 요청 시에만** (인터뷰 결정).

🔎 [Claude 추론] **좋은 안건 쓰는 법**: "유튜브 어떻게 키우지?"처럼 넓은 질문보다 "최근 12개월 영어권 신규 채널 중 조회수 증가율 상위 20개의 공통 포맷 3가지와, 1인 제작자가 재현 가능한 것"처럼 **대상·기간·판단 기준**이 들어간 질문이 자료와 채점 기준을 쓰기 쉽습니다.

---

## 8. 문제 해결

| 증상 | 원인과 해결 |
|---|---|
| `의장: gemini — 준비 안 됨 (...) → 회의 보류` | 1.2의 Gemini API 키 절차를 마치지 않은 상태. 괄호 안 이유(환경변수 없음 / model 값 미정)를 해결 |
| Gemini 실패: `HTTP 400`·`404` | `model` ID가 틀림. `models gemini --filter flash`로 다시 확인 |
| Gemini 실패: `HTTP 429` | 무료 등급 한도 초과. 잠시 후 다시 시도 (한도는 AI Studio에서 확인) |
| Gemini CLI에서 `IneligibleTierError` | 2026-06-18 개인 계정 중단 때문 ([공지 #28017](https://github.com/google-gemini/gemini-cli/discussions/28017)). Council은 CLI를 쓰지 않으므로 무시 |
| Codex 실패 (로그인 관련) | `codex login` 다시 실행 |
| 위원이 `시간 초과` | 네트워크·로그인 문제로 CLI가 재연결을 반복하는 경우가 있음(🧪 이 작업 환경에서 Codex가 네트워크 차단 때문에 계속 재연결). 먼저 `check --ping`으로 확인하고, 응답이 느린 것뿐이면 `council/members.json`의 `timeout`(초)을 늘림 |
| `응답이 1개뿐입니다. 최소 2개가 필요합니다` | 실패한 위원 오류는 `council/runs/<회의>/logs/`에 있음. 해결 후 `stage1` 다시 실행 (이미 받은 답은 건너뜀) |
| `순위를 읽지 못한 평가` | 평가 마지막 줄에 `FINAL RANKING:`이 없음. Claude에게 "그 평가만 다시 받아줘" (`stage2 --force`는 모든 자동 평가를 다시 받음) |
| 브라우저 보조가 멈춤 | 로그인·CAPTCHA·동의 화면 → 직접 처리 후 "계속"이라고 말하기. 확장 연결은 `/chrome`에서 확인 |
| 한글이 깨짐 | 스크립트는 UTF-8로 읽고 씀. 결과 파일은 VS Code 등 UTF-8 편집기로 열기 |

---

## 9. 다음 단계

- **Phase B — 데이터 레이어**: YouTube Data API로 채널·영상 지표를 매일 저장해 자료표를 자동으로 채우기 ([01 문서 4장](./01-interview-and-plan.md))
- **Phase C — Python 재구현·포트폴리오**: 회의 기록이 쌓이면 결정과 성과를 비교한 글을 LinkedIn·블로그에 공유

---

## 출처

- Claude Code Chrome 연동 — https://code.claude.com/docs/en/chrome
- Claude Code Skills — https://code.claude.com/docs/en/skills
- Codex Auth — https://developers.openai.com/codex/auth
- 중첩 세션 이슈 — https://claudeissues.com/issue/26190-nested-claude-p-instances-hang-when-claudecode-env-var-is-inherited
- Panickssery et al. 2024 — https://arxiv.org/abs/2404.13076 , karpathy/llm-council — https://github.com/karpathy/llm-council
- 🧪 직접 확인: `gemini --help`(0.63.0), `codex exec --help`(codex-cli 0.161.0), `council.py check --ping`(클라우드에서 실패 원인 표시 확인), PC 실측 보고 `✓ codex: 성공 (7.6초)`·`✗ gemini: IneligibleTierError`, 테스트 `python -m unittest discover -s council/tests` (9개 통과)
