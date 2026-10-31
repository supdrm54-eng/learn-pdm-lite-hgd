# 예지보전 10분 실습 — learn-pdm-lite-hgd

프레스 메인모터·용접로봇 감속기의 진동에서 노이즈와 추세를 가려 정비 필요 시점을 잡고, 그래프 한 장을 공개하는 10분 수업이다. 수업은 Claude Code 스킬 `/learn-pdm-lite-hgd`가 진행한다 (Skills as Curriculum). supdrm54-eng가 course-forge로 KMA 자동차특화 AI 융합 전문가 과정 5일차를 바탕으로 만들었다. 3시간 전체판은 [learn-auto-pdm](https://github.com/supdrm54-eng/learn-auto-pdm).

- **결과 그래프**: https://supdrm54-eng.github.io/learn-pdm-lite-hgd/
- 처음이면 [GUIDE.md](GUIDE.md)부터

## 설치 — 한 줄

```
npx skills add supdrm54-eng/learn-pdm-lite-hgd --agent claude-code --global --yes 를 실행해 줘
```

새 세션에서 `/learn-pdm-lite-hgd`를 입력하면 시작된다. Node.js가 없으면 GUIDE.md 1단계대로 설치한다.

## 블록

| Block | 주제 | 끝나면 생기는 것 |
|---|---|---|
| 0 | 준비 | `~/pdm-lite` 폴더와 센서 데이터 |
| 1 | 노이즈 vs 추세 | 판정표, 진동 그래프 한 장, 퀴즈 1문항 |
| 2 | 공개 | 그래프 공개 주소 |

## 수업 방식

| 구분 | 내용 |
|---|---|
| 목표 — AI Native | 계산·그래프는 Claude, 정비 신호 판단은 나 |
| 방법 — Skills as Curriculum | 스킬이 설명 → 실습 → STOP → 확인·퀴즈를 진행한다 |
| 형식 — 자율학습 | 10분, 퀴즈 1문항 |

## 원본 강의와 데이터 출처

| 자료 | 출처 | 구분 |
|---|---|---|
| 원본 강의 | [keerhee/kma-auto-genai-3-1](https://github.com/keerhee/kma-auto-genai-3-1) `Day5_예지보전/Day5_3_Main_자동차예지보전AI활용.pdf` — ③ 전처리, ④ 분석 1, 실습과제 2 | 개념·과제·모범답안을 따름 |
| `Day5_설비센서_50건_가상.csv` | 원본 저장소 `data/Day5/` | 실습용 가상 데이터 |

## 개정 이력

| 날짜 | 바뀐 점 |
|---|---|
| 2026-10-31 | 첫 판 — 블록 3개(10분), 퀴즈 1문항, 정답 수치 13개 검증 |

## 만든 방법

- `/course-forge`로 만들었다. 제작 기록은 [`forge/`](forge/)에 있다.
- 출처: 원본 강의 저장소 https://github.com/keerhee/kma-auto-genai-3-1
