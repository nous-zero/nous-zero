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
   ├─ 2. 독립 의견   Gemini·GPT(자동) + Claude(서브에이전트) + Meta AI·Perplexity·Grok(브라우저)
   ├─ 3. 익명 평가   이름 가린 답변을 Gemini·GPT·Claude가 채점·순위 (반론자 1명)
   ├─ 4. 의장 종합   Claude ↔ Gemini 번갈아 의장 → 결론·소수 의견·확신도
   └─ 5. 기록        decision-log.md → 나중에 "실행 결과" 기입
```

**내가 할 일**은 ① 안건 입력 ② 자료 확인 ③ 브라우저 위원 방식 선택(지켜보기 / 직접 붙여넣기 / 생략) ④ 결과 읽고 실행 — 네 가지입니다.

---

## 1. 처음 한 번만: 준비 (Windows PowerShell)

### 1.1 설치 확인
```powershell
node -v          # Node.js가 없으면 https://nodejs.org 에서 LTS 설치
python --version # 3.10 이상. 없으면 https://www.python.org/downloads/
```

### 1.2 위원 CLI 설치와 로그인
```powershell
npm install -g @google/gemini-cli @openai/codex
gemini           # 처음 실행 시 "Login with Google" 선택 → Google AI Pro 계정 로그인 → /quit 으로 종료
codex login      # 브라우저가 열리면 ChatGPT 계정으로 로그인
```
- 🧪 2026-10-08 기준 설치된 버전: Gemini CLI `0.63.0`, Codex CLI `0.161.0`.
- 🧪 Gemini CLI는 로그인 전에 실행하면 `Please set an Auth method ...` 메시지를 냅니다. 이 메시지가 나오면 `gemini`를 한 번 실행해 로그인하면 됩니다.
- Codex 로그인 방식: [Codex Auth](https://developers.openai.com/codex/auth)

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
- gemini           [사용] command            명령 gemini: 있음 (...)
- codex            [사용] command            명령 codex: 있음 (...)
- meta-ai          [사용] manual             사용자가 브라우저 답변을 붙여넣음
- perplexity       [사용] manual             ...
- grok-web         [사용] manual             ...
```
`없음`이 나오면 8장 문제 해결을 보세요.

### 1.5 (선택) 브라우저 보조를 쓰려면: Claude in Chrome 연결
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
| 2. 독립 의견 | Gemini·Codex 자동 호출, Claude는 서브에이전트로 답변 | 브라우저 위원 방식 선택 (4장) | 5~15분 |
| 3. 익명 평가 | 답변에 무작위 라벨(Response A, B…) 부여, 평가자마다 순서 섞기, 반론자 지정, 순위 집계 | — | 5~10분 |
| 4. 의장 종합 | 회의마다 Claude ↔ Gemini 의장 교대, 결론 작성 | — | 2~5분 |
| 5. 기록 | `decision-log.md` 생성, 결과 보고, 커밋 여부 질문 | 결과 읽기, 커밋 여부 답하기 | — |

- 진행자는 **의견을 내지 않고**, 위원 답변을 고치거나 요약해서 넘기지 않습니다. Claude의 의견은 진행자와 분리된 서브에이전트가 냅니다 ([SKILL.md](../../.claude/skills/llm-council/SKILL.md) 규칙).
- Claude Code 안에서 `claude -p`를 다시 부르면 중첩 세션 차단에 걸리거나 멈추는 사례가 보고되어 서브에이전트 방식을 씁니다 ([claudeissues #26190](https://claudeissues.com/issue/26190-nested-claude-p-instances-hang-when-claudecode-env-var-is-inherited)).

---

## 4. 브라우저 위원(Meta AI·Perplexity·Grok) 참여 방식

독립 의견 단계(스크립트의 Stage 1)에서 Claude가 매번 묻습니다. 셋 중 하나를 고르세요.

| 방식 | 언제 | 진행 |
|---|---|---|
| **A. 브라우저 보조** | Claude in Chrome이 연결되어 있고, 화면을 지켜볼 수 있을 때 | Claude가 새 탭에서 각 사이트를 열고 → 질문 전문을 붙여넣고 → 답변이 끝나면 전체를 복사해 저장. 로그인·CAPTCHA·동의 화면·유료 안내가 나오면 멈추고 나에게 넘김 |
| **B. 직접 붙여넣기** | 확장 프로그램이 없거나 직접 하고 싶을 때 | `council/runs/<회의>/stage1/prompts/meta-ai.md` 등을 열어 전체 복사 → 사이트에 붙여넣기 → 받은 답변을 Claude Code 채팅에 붙여넣으며 "meta-ai 답변"이라고 알려주기 → Claude가 원문 그대로 저장 |
| **C. 생략** | 바쁠 때 | Claude·Gemini·GPT 3개 답변만으로 진행 (최소 2개 필요) |

- 브라우저 위원은 복사·붙여넣기 부담을 줄이려고 **Stage 1(독립 의견)에만** 참여합니다. 평가는 Gemini·GPT·Claude가 합니다.
- 🔎 [Claude 추론] 사이트마다 **새 대화**에서 시작해야 이전 대화의 맥락이 섞이지 않습니다.
- ⚠️ 각 사이트 약관의 자동화 관련 조항은 원문으로 확인하지 못했습니다. A 방식을 쓰기 전에 각 사이트 하단의 Terms 링크를 한 번 확인하세요.

---

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
| 의장 지정 | "이번 회의 의장은 gemini로" |
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
| `check`에서 `명령 gemini: 없음` | Node.js 설치 후 새 PowerShell 창에서 `npm install -g @google/gemini-cli` 다시 실행 |
| Gemini 실패: `Please set an Auth method ...` | 🧪 로그인 전 상태의 메시지. `gemini` 실행 → Google 로그인 |
| Codex 실패 (로그인 관련) | `codex login` 다시 실행 |
| 위원이 `시간 초과` | `council/members.json`에서 해당 위원의 `timeout`(초)을 늘림 |
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
- 🧪 직접 확인: `gemini --help`(0.63.0), `codex exec --help`(codex-cli 0.161.0), `python council/scripts/council.py check`, 테스트 `python -m unittest discover -s council/tests` (7개 통과)
