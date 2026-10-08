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
7. **회의 보류**: 의장(`gemini`)이 준비되지 않으면 회의를 열지 않는다(사용자 결정). `new`가 막으면 `--ignore-chair`로 우회하지 말고, `check`가 알려 주는 이유와 해결 절차(`council/README.md`의 "Gemini 연결")를 사용자에게 안내한다.
8. **API 키는 다루지 않는다**: 사용자가 키를 채팅에 붙여넣으려 하면 막고, Windows 환경변수에 직접 넣도록 안내한다. Gemini 무료 등급은 입력이 구글 제품 개선에 쓰일 수 있으므로 자료표에 비공개 정보를 넣지 않는다.

## 절차

### 0. 점검
`python council/scripts/council.py check` — 꺼져 있거나 설치되지 않은 위원을 사용자에게 알린다. 처음 쓰는 날이나 위원이 실패한 뒤에는 `check --ping`으로 실제 응답까지 확인한다.

### 1. 안건과 자료
1. `python council/scripts/council.py new "<안건>" [--rubric youtube-growth]` → 출력된 경로가 `$RUN`.
2. `$RUN/fact-sheet.md`를 채운다. 웹 검색·사용자가 준 데이터로 표를 만들고, 행마다 출처 링크와 수집일을 적는다.
3. 자료 요약을 사용자에게 보여주고, 빠진 데이터가 있는지 확인받는다.

### 2. Stage 1 — 독립 의견 (모든 위원 동시 진행)
1. `python council/scripts/council.py stage1 $RUN --prepare` — 모든 위원의 프롬프트 파일을 먼저 만든다(호출 없음, 수초).
2. 아래 세 갈래를 **같은 응답 안에서 동시에** 시작한다. 하나가 끝나기를 기다렸다가 다음을 시작하지 않는다.
   - **자동 위원**: `python council/scripts/council.py stage1 $RUN`을 Bash의 백그라운드 실행으로 띄운다. Gemini(API)·Codex(CLI)가 스크립트 안에서 병렬로 호출된다.
   - **Claude**: Agent 도구를 백그라운드로 실행해 규칙 3의 문구로 `$RUN/stage1/prompts/claude.md`를 넘긴다. 결과가 오면 `$RUN/stage1/responses/claude.md`에 저장한다.
   - **브라우저 위원** (`meta-ai`·`perplexity`·`grok-web`): `settings.browser_mode`를 따른다. 사용자가 이번 회의에서 다른 방식을 말하면 그것을 따른다.
     - `assist`(기본) → A. 단, Claude in Chrome 도구가 없거나 사용자가 없는 무인 실행(`claude -p` 등)이면 C로 바꾸고 그 사실을 보고한다.
     - `paste` → B, `skip` → C, `ask` → 회의마다 사용자에게 묻는다.
     - **A. 브라우저 보조 (사용자가 지켜봄)**
       1. 세 사이트를 각각 새 탭으로 열고(`browser_url`), 새 대화에 `$RUN/stage1/prompts/<id>.md` 전문을 붙여넣어 **세 곳 모두 먼저 보낸다**. 세 사이트가 동시에 답을 만들게 하기 위해서다.
       2. 그다음 탭을 하나씩 돌며 답변 생성이 끝났는지 확인하고, 끝난 답변 본문 전체를 `$RUN/stage1/responses/<id>.md`에 원문 그대로 저장한다.
       3. 로그인 요구, CAPTCHA, 약관·쿠키 동의, 유료 업그레이드 안내가 나오면 그 탭에서 멈추고 사용자에게 넘긴다. 직접 우회하지 않는다. 다른 탭 작업은 계속한다.
     - **B. 직접 붙여넣기** — 사용자가 프롬프트를 사이트에 넣고, 받은 답변을 채팅에 붙여넣으면 진행자가 원문 그대로 저장한다.
     - **C. 이번엔 생략** — 기다리지 않는다.
3. 세 갈래가 모두 끝나면 `python council/scripts/council.py status $RUN`으로 빠진 응답을 확인한다.
4. 이 환경에서 Bash나 Agent를 백그라운드로 실행할 수 없으면 차례로 실행해도 된다. 각 위원은 자기 프롬프트 파일만 보고 자기 응답 파일에만 쓰므로 결과는 같고 시간만 더 걸린다.

### 3. Stage 2 — 익명 상호평가 (동시 진행)
1. `python council/scripts/council.py stage2 $RUN --prepare` — 라벨(Response A, B…)을 무작위로 붙이고 평가자마다 순서를 섞은 프롬프트를 만든다. 반론자(Devil's Advocate)는 회의마다 돌아가며 정해진다.
2. 동시에 시작한다: `python council/scripts/council.py stage2 $RUN`(백그라운드, Gemini API·Codex 병렬 평가) + `claude` 평가 서브에이전트(`$RUN/stage2/prompts/claude.md` → `$RUN/stage2/responses/claude.md`).
3. 둘 다 끝나면 `python council/scripts/council.py aggregate $RUN` — 평가 마지막 줄의 `FINAL RANKING`을 읽어 평균 순위를 낸다. 읽기 실패한 평가가 있으면 사용자에게 알린다.

### 4. Stage 3 — 의장 종합 (의장: Gemini 고정)
1. `python council/scripts/council.py stage3 $RUN` — 사용자 결정에 따라 의장은 항상 `gemini`다(`settings.chair_rotation: ["gemini"]`). 스크립트가 Gemini API(키 방식)로 자동 실행한다.
2. 의장 호출이 실패하면 다른 위원으로 바꾸지 말고 오류를 사용자에게 보고한 뒤 `stage3 $RUN`을 다시 시도한다. 사용자가 이번 회의만 바꾸라고 하면 `--chair <id>`를 쓴다.

### 5. 기록과 보고
1. `python council/scripts/council.py finalize $RUN` → `$RUN/decision-log.md` (익명 해제 표 포함).
2. 사용자에게 보고한다: 최종 결론, 근거, 소수 의견, 확신도, 순위 집계, 익명 해제 결과, 다음 행동. 사실은 출처와 함께, 추론은 `[추론]`으로 표시한다.
3. run 폴더를 커밋할지 사용자에게 묻는다(포트폴리오 기록용).
