# AI 용어: Llama (라마)

> 작성일: 2026-10-08 · 작성: Claude Code
> 저장 권장 위치: `C:\Users\745ra\OneDrive\바탕 화면\Ai 용어 트랜드\Llama.md`
>
> **표기 규칙** — 링크 = 출처로 확인한 사실 / 🔎 **[Claude 추론]** = 출처 없는 추론·제안 / ⚠️ = 출처 간 불일치·미확인

---

## 1. 한눈에 보기

| 항목 | 내용 |
|---|---|
| 한 줄 정의 | Meta가 만든 대규모 언어 모델(LLM) 계열. 모델 가중치를 내려받아 직접 실행·미세조정할 수 있는 **공개 가중치(open-weight)** 모델 |
| 라이선스 | Llama Community License + 이용 정책. 완전한 오픈소스가 아니라 **소스 공개(source-available)** 로 분류됨. 월간 활성 사용자 7억 명 이상 서비스는 Meta의 별도 허가 필요 ([Wikipedia](https://en.wikipedia.org/wiki/Llama_(language_model)), [DataCamp](https://www.datacamp.com/blog/llama-4)) |
| 2026년 위치 | Meta의 최신 주력은 비공개 모델 **Muse Spark**로 이동했고, Llama는 직접 설치·미세조정하려는 개발자용으로 남는 이원화 구조로 분석됨 ([FourWeekMBA](https://fourweekmba.com/ai-meta-muse-spark-1-1-meta-model-api-closed-pivot/), [Implicator](https://www.implicator.ai/meta-debuts-muse-spark-first-ai-model-from-its-14-3-billion-superintelligence-lab.md)) |

---

## 2. 어원

- 첫 버전의 이름 **LLaMA**는 **L**arge **La**nguage **M**odel **M**eta **A**I의 약자입니다 ([Wikipedia](https://en.wikipedia.org/wiki/Llama_(language_model))).
- 🔎 **[Claude 추론]** 약자가 동물 '라마(llama)'와 철자가 같아 기억하기 쉬운 이름이 되었고, 이후 버전부터는 대소문자를 섞지 않은 **Llama**로 표기합니다.

---

## 3. 6하원칙 (5W1H)

| 원칙 | 내용 | 출처 |
|---|---|---|
| **누가 (Who)** | Meta (AI 연구 조직) | [Wikipedia](https://en.wikipedia.org/wiki/Llama_(language_model)) |
| **언제 (When)** | 2023-02 LLaMA(7·13·33·65B) → 2023-07 Llama 2(7·13·70B, Microsoft와 협력) → 2024-04 Llama 3 → 2024-12-06 Llama 3.3 70B → 2025-04-05 Llama 4 Scout·Maverick | [Wikipedia](https://en.wikipedia.org/wiki/Llama_(language_model)), [Gigazine](https://gigazine.net/gsc_news/en/20241209-meta-llama-3-3), [DataCamp](https://www.datacamp.com/blog/llama-4) |
| **어디서 (Where)** | Meta 공식 사이트와 Hugging Face에서 가중치 배포 | [Telnyx](https://telnyx.com/llm-library/llama-3.3-70b-instruct) |
| **무엇을 (What)** | 텍스트 생성 LLM. Llama 3.3 70B는 128K 토큰 문맥, 8개 언어 공식 지원 | [Telnyx](https://telnyx.com/llm-library/llama-3.3-70b-instruct) |
| **어떻게 (How)** | Llama 3까지는 모든 파라미터가 매번 계산되는 dense 구조. Llama 4는 토큰마다 일부 전문가(expert)만 쓰는 **MoE(Mixture-of-Experts)** 구조로 전환: Scout 총 109B·활성 17B·전문가 16개·문맥 10M, Maverick 총 400B·활성 17B·전문가 128개·문맥 1M | [DataCamp](https://www.datacamp.com/blog/llama-4) |
| **왜 (Why)** | 처음엔 연구자에게 사례별로 승인해 공개(비상업 라이선스), Llama 2부터 대화용 지시 학습(instruction-tuned) 버전을 함께 공개해 개발자 생태계 확대 | [Wikipedia](https://en.wikipedia.org/wiki/Llama_(language_model)) |

### 3.1 2026년에 달라진 점
- **Groq 무료 등급 종료**: Groq는 2026-08-16 `llama-3.3-70b-versatile`·`llama-3.1-8b-instant`, 2026-07-17 `llama-4-scout`를 무료·개발자 등급에서 종료했습니다 ([Groq Deprecations](https://console.groq.com/docs/deprecations)).
- **Meta의 비공개 전환**: Muse Spark는 Meta가 처음으로 가중치를 공개하지 않은 모델이며, 2026-07-09 Meta Model API로 개발자에게 공개 프리뷰가 시작되었습니다 ([FourWeekMBA](https://fourweekmba.com/ai-meta-muse-spark-1-1-meta-model-api-closed-pivot/), [AIChatDaily](https://www.aichatdaily.com/ai-models/meta-opens-muse-spark-1-1-developers-via)).

---

## 4. 박정훈 님과의 시너지 분석

> 경력 정보는 [README.md](../README.md) 기준이며, 분석은 모두 🔎 **[Claude 추론]** 입니다.

| 자산 | Llama와의 연결 | 실행 아이디어 |
|---|---|---|
| **AIGEN — 3B Biomedical Agent (GDPO·SFT·Uncertainty Head)** | 가중치가 공개된 모델이라 **직접 미세조정(SFT)·선호 학습**을 실습할 수 있음 | Colab·Kaggle 무료 GPU에서 소형 Llama로 SFT·DPO 실습 → AIGEN 경험을 공개 포트폴리오로 재현 |
| **LLM Council 프로젝트** | 로컬에서 돌릴 수 있는 유일한 Meta 계열 무료 위원 | `council/members.json`의 `llama-local`(Ollama `llama3.1:8b`)을 켜서 오프라인 위원으로 사용. 단, 현재 PC(내장 GPU)에서는 느림 |
| **Phase 1 학습 (PyTorch·HuggingFace)** | Hugging Face에서 가장 많이 쓰이는 공개 모델 계열 중 하나라 학습 자료가 풍부 | GDPO.py 주석 학습과 병행해 Llama 아키텍처(dense vs MoE) 비교 노트 작성 |
| **글로벌 YouTube 채널** | "오픈 모델 vs 비공개 모델" 흐름 자체가 콘텐츠 주제 | Meta의 Llama → Muse Spark 전환을 다루는 해설 영상·LinkedIn 글 |

---

## 5. 관련 용어

| 용어 | 한 줄 설명 | 출처 |
|---|---|---|
| Open-weight (공개 가중치) | 학습된 모델 가중치를 내려받아 직접 실행할 수 있게 공개한 모델 | [Wikipedia](https://en.wikipedia.org/wiki/Llama_(language_model)) |
| MoE (Mixture-of-Experts) | 여러 전문가 하위 네트워크 중 일부만 토큰마다 활성화하는 구조 | [DataCamp](https://www.datacamp.com/blog/llama-4) |
| Muse Spark | Meta Superintelligence Labs의 비공개 모델, Meta Model API로 제공 | [FourWeekMBA](https://fourweekmba.com/ai-meta-muse-spark-1-1-meta-model-api-closed-pivot/) |
| Ollama | 공개 가중치 모델을 내 PC에서 실행하는 도구, OpenAI 호환 API 제공 | [Ollama 문서](https://docs.ollama.com/api/openai-compatibility.md) |
