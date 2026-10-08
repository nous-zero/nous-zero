# Windows 로컬 테스트 체크리스트 (v1.0)

> 작성일: 2026-10-08 · 대상: 박정훈 PC (Windows 11)
>
> **표기 규칙** — 링크 = 출처로 확인한 사실 / 🧪 = 클라우드 작업 환경에서 직접 실행해 확인 / 🔎 **[Claude 추론]** = 출처 없는 판단 / ⚠️ = 확인 필요
>
> 사용법: 위에서부터 차례로 실행하고, 각 단계의 **통과 기준**과 비교하세요. 실패하면 출력 전체를 Claude Code에 붙여넣으면 됩니다.

---

## 0. 로그인은 한 번만 하면 유지되나요?

| 대상 | 유지 방식 | 근거 |
|---|---|---|
| **브라우저 위원** (meta.ai·perplexity.ai·grok.com) | Claude in Chrome은 **내 Chrome의 로그인 상태를 그대로 사용**합니다. 평소 쓰는 Chrome 프로필에서 세 사이트에 한 번 로그인해 두면, 사이트가 로그아웃시키기 전까지 다시 로그인하지 않아도 됩니다 | [Claude Code Chrome 문서](https://code.claude.com/docs/en/chrome): "shares your browser's login state" |
| ↳ 주의 | 시크릿 창이 아닌 **확장 프로그램이 연결된 일반 프로필**에서 로그인하세요. 로그인 화면이나 CAPTCHA가 나오면 Claude는 멈추고 사용자에게 넘깁니다 | 같은 문서 |
| ↳ 유지 기간 | 각 사이트가 로그인을 얼마나 유지하는지는 확인하지 못했습니다 ⚠️ | — |
| **Codex CLI** | `codex login` 후 인증 정보가 `~/.codex/auth.json`에 저장되고, 이후 실행은 저장된 인증을 씁니다 | [Codex 인증 문서](https://developers.openai.com/codex/auth) (auth.json에 접근 토큰 저장), [Non-interactive 문서](https://developers.openai.com/codex/noninteractive) |
| **Gemini CLI** | 처음 실행 때 Google 로그인을 하면 인증 설정이 사용자 폴더의 `.gemini` 아래에 저장됩니다 | 🧪 로그인 전 실행 시 `~/.gemini/settings.json`에서 인증 방식을 찾는다는 메시지 확인. 토큰 유지 기간은 미확인 ⚠️ |

🔎 **[Claude 추론]** 그래서 아래 1~3단계를 한 번 해 두면 회의 때는 로그인 없이 진행됩니다. 로그인이 풀리면 회의 중 해당 위원만 실패하거나 멈추고, Claude가 알려줍니다.

---

## 1. 기본 도구 확인 (PowerShell)

```powershell
git --version
node -v
python --version
```
**통과 기준**: 세 줄 모두 버전이 나옴. Python은 3.10 이상.

- `python`을 치면 Microsoft Store가 열리면 Python이 설치되지 않은 것입니다. [python.org](https://www.python.org/downloads/)에서 설치하거나, 설치되어 있다면 `py --version`을 쓰고 아래 명령의 `python`을 `py`로 바꾸세요.

---

## 2. 코드 받기

처음이라면:
```powershell
cd $HOME
git clone https://github.com/nous-zero/nous-zero.git
cd nous-zero
git checkout claude/llm-concile-usage-interview-pnttr8
```
이미 받았다면:
```powershell
cd $HOME\nous-zero
git pull
```
**통과 기준**: `council` 폴더와 `.claude\skills\llm-council\SKILL.md`가 있음 (`dir council`, `dir .claude\skills\llm-council`).

---

## 3. 자동 테스트 (계정 불필요)

```powershell
python -m unittest discover -s council/tests -v
```
**통과 기준**: 마지막에 `Ran 12 tests` 와 `OK`.

- 이 테스트는 가짜 위원으로 회의 전체(독립 의견 → 익명 평가 → 의장 → 기록), 병렬 호출, 질문 파일 보존, 유료 위원 차단을 확인합니다. 🧪 클라우드(Linux)에서 12개 통과.
- `test_automated_members_are_called_in_parallel`이 실패하면 Windows에서 병렬 호출이 안 되는 것이니 출력을 보내 주세요.

---

## 4. 위원 CLI 설치와 로그인

```powershell
npm install -g @google/gemini-cli @openai/codex
```
설치 후 **PowerShell 창을 새로 열고**:
```powershell
gemini --version
codex --version
```
**통과 기준**: 버전 숫자가 나옴 (🧪 2026-10-08 기준 Gemini CLI 0.63.0, codex-cli 0.161.0).

- `이 시스템에서 스크립트를 실행할 수 없으므로...` 오류가 나면 PowerShell 실행 정책 때문입니다. `gemini.cmd --version`처럼 `.cmd`를 붙여 실행하거나, 실행 정책을 확인하세요 ([Microsoft: about_Execution_Policies](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_execution_policies)). 🔎 [Claude 추론] Council 스크립트는 `.cmd` 파일을 찾아 실행하므로 이 오류와 상관없이 동작할 가능성이 높습니다.

로그인:
```powershell
gemini            # "Login with Google" 선택 → 브라우저에서 Google AI Pro 계정 로그인 → /quit
codex login       # 브라우저에서 ChatGPT 계정 로그인
codex login status
```
**통과 기준**: `codex login status`가 로그인 상태를 보여줌 (🧪 `codex login --help`에서 `status: Show login status` 확인).

---

## 5. Council 연결 점검

```powershell
python council/scripts/council.py check
```
**통과 기준**: `gemini`, `codex` 줄에 `명령 ...: 있음`.

```powershell
python council/scripts/council.py check --ping
```
**통과 기준**:
```
  ✓ gemini: 성공 (…초) - OK
  ✓ codex: 성공 (…초) - OK
```
- 실패 예시(🧪 로그인 전): `! gemini: 실패 (2.2초) - 종료 코드 41: Please set an Auth method ...` → 4단계 로그인 다시.
- `시간 초과`가 나오면 네트워크·로그인 문제일 수 있습니다(🧪 클라우드에서는 OpenAI 연결이 막혀 Codex가 계속 재연결했음).

---

## 6. Chrome 연결 점검 (Claude Code 안에서)

1. Chrome에서 meta.ai, perplexity.ai, grok.com에 로그인해 둡니다.
2. `nous-zero` 폴더에서 Claude Code를 실행하고 `/chrome`을 입력해 연결 상태를 확인합니다 ([Claude Code Chrome 문서](https://code.claude.com/docs/en/chrome)). 처음이면 `claude --chrome`으로 시작합니다.
3. 아래 문구를 그대로 입력합니다.

```
Chrome에서 meta.ai, perplexity.ai, grok.com을 각각 새 탭으로 열고, 로그인된 상태인지만 확인해서 표로 알려줘. 아무것도 입력하거나 보내지 마.
```
**통과 기준**: 세 사이트 모두 "로그인됨".

4. 세 사이트에 동시에 보내는 시험:

```
Chrome에서 meta.ai, perplexity.ai, grok.com 각각 새 대화를 열고 "1+1은? 숫자만 답해."를 세 곳에 먼저 모두 보낸 다음, 탭을 돌면서 각 답변을 표로 알려줘.
```
**통과 기준**: 세 답변이 모두 표에 나오고, Claude가 세 곳에 먼저 보낸 뒤 답을 모았음.

- 사이트마다 처음 한 번 확장 프로그램이 해당 사이트에서 동작해도 되는지 물을 수 있습니다. 권한은 `/chrome`에서 관리합니다 ([Claude Code Chrome 문서](https://code.claude.com/docs/en/chrome)). ⚠️ 정확한 첫 실행 화면은 미확인.

---

## 7. 연습 회의 ① — CLI 위원만

Claude Code에 입력:
```
/llm-council 연습: 아침 루틴에서 LeetCode와 GDPO 주석 중 무엇을 먼저 할까
```
진행 중 Claude가 자료표를 보여주면:
```
자료 확인했어. 이번엔 브라우저 위원 생략하고 끝까지 진행해줘.
```
**통과 기준**:
- 독립 의견 단계 출력에 `> 동시 호출: gemini, codex`가 나오고, 두 위원의 `저장 ... (N초)` 시간이 **서로 비슷하게** 끝남 (순서대로라면 두 번째 위원 시간이 첫 번째의 약 두 배가 됨) → Windows에서 병렬 호출 확인.
- 마지막에 `council\runs\<날짜_연습...>\decision-log.md`가 생기고, 의장이 `Gemini (Gemini CLI)`로 적혀 있음.

확인 명령:
```powershell
python council/scripts/council.py status council/runs/<회의 폴더 이름>
```

---

## 8. 연습 회의 ② — 브라우저 위원 포함

```
/llm-council 연습2: 새 글로벌 채널 첫 영상 포맷으로 숏폼과 롱폼 중 무엇이 나을까
```
**통과 기준**:
- Gemini·GPT 호출과 **같은 시간에** Chrome 탭 3개가 열리고 질문이 들어감.
- `status` 결과에서 stage1의 `claude`, `gemini`, `codex`, `meta-ai`, `perplexity`, `grok-web` 6개가 모두 `완료`.
- `decision-log.md`의 익명 해제 표에 6개 위원이 모두 있음.

---

## 9. 결과 보내기

모두 통과하면 "테스트 통과"라고만 알려 주세요. 실패하면 아래를 Claude Code에 붙여넣어 주세요.
1. 실패한 단계 번호와 명령
2. 출력 전체 (특히 `!` 로 시작하는 줄)
3. 회의 중 실패라면 `council\runs\<회의>\logs\` 폴더의 파일 내용
