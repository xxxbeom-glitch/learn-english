# Side A 음성: 엔진, 목소리, 효과음, 비용

목차는 [2026-11-07-story-audio-english-design.md](2026-11-07-story-audio-english-design.md). 모든 콘텐츠의 음성 공통 규칙이다. 콘텐츠별 목소리 배치와 제작 기록은 각 분야 문서에 있다.

## 1. 엔진 (지금 기준)

- 한국어(해설)와 영어 모두 **일레븐랩스 Eleven v4**로 만든다. (2026-11-09 저녁 "그냥 일레븐랩스로 하자". Words도 2026-11-10 "그냥 전부 일레븐랩스")
- 구글 Gemini TTS로 영어를 만드는 안은 2026-11-09에 시험하고 취소했다. 시험 기록(배역, 키, 비교 파일)은 [archive 스냅숏](archive/2026-11-07-story-audio-english-design-snapshot-2026-11-10.md) 6장에 있다. `.env`의 `GEMINI_API_KEY`와 `spikes/episode-01/google_tts_test.py`, `voice_audition.py`, `audio/unused/google-test/`, `audio/unused/beginner2-variants/`는 시험 기록으로만 남는다.
- 계정: 2026-11-10부터 성범이 유료로 올린 lumianthecompany 계정 연결(`67a9ac48`)로 만든다. 예전 xxx.beom 연결(`761d98d3`)과 크리에이터 워크스페이스(`73061a6b…`)도 썼다. 유료 API는 쓰기 전에 실제 비용을 확인하고, 돈이 나가면 미리 말하고 동의를 받는다.
- 음성은 앱에서 실시간으로 읽지 않고 미리 만든 파일을 재생한다.

## 2. 목소리

| 역할 | 목소리 | 쓰는 곳 |
|---|---|---|
| 해설자 Mina | 한국 여성, `aiUUgjHa4mpHf6UenZuf` | 코스, Words |
| 남1 | Jack John | 코스 예문, Words 단어, 쉐도잉 나(A) |
| 여1 | Hope (`OYTbf65OHHFELVut7v2H`) | 코스 예문, Words 예문, 쉐도잉 상대(B) |
| 남2 | Will | 코스 예문, Words 예문 |
| 여2 | Clara (`ZIlrSGI4jZqobxRKprJz`) | 코스 예문, Words 단어, 쉐도잉 안내 두 마디 |

- 코스 목소리 설정은 `spikes/episode-01/beginner_v2.py`의 `VOICE`에 있다. 팟캐스트 목소리(Mike, Mia, Hayley 등)는 [팟캐스트](side-a-podcasts.md).
- 옛 초급 v1 인물 목소리(성범 Jack John, 테일러 Jessica, 해리 Will, 올리비아 Shannon W, 지수 Yeonhee, Eric, Josh, Tanya)는 쓰지 않는다. 겹치는 영어 문장은 재사용할 수 있다.

## 3. 만드는 규칙

- 감정은 `[nervous]`, `[teasing]`, `[laughs]`, `[annoyed]`, `[firm]` 같은 표시로 넣는다. 초반 화는 또렷하게, 감정은 살짝만.
- 줄마다 따로 만들면 앞줄의 말투를 이어받지 못한다. 혼자 하는 방송에서 `[softly]`는 속삭임처럼 읽히므로 `[warmly]`, `[nostalgic]`처럼 말투만 누그러뜨리는 표시를 쓴다. `[smirks]`는 소리로 나지 않아 `[sarcastic]`을 쓴다.
- 말해보기·따라 하기 멈춤은 대본의 `[long pause]`에 맡기지 않고 조용한 구간을 파일에 직접 넣는다.
- 반복과 다시 듣기는 만든 음성을 재사용해 크레딧을 아낀다. 같은 목소리, 같은 문장이 이미 있으면(끝인사 등) 새로 만들지 않고 복사한다.
- 대본이 바뀌면 바뀐 줄만 다시 만든다. 조각 id가 같으므로 `clips N`으로 목록을 다시 쓰고, 바뀐 조각만 덮어쓴 뒤 `build N`으로 다시 잇는다. 옛 소리는 지우지 않고 따로 보관한다.
- 조각 앞뒤 무음을 자른 자리에서 소리가 갑자기 시작·끝나면 '삑' 잡음이 난다. 조각마다 앞 0.01초, 뒤 0.02초 페이드를 넣는다. 일레븐랩스가 조각 맨 앞에 곧은 높은 음을 넣을 때가 있어, 들리는 곳은 그 조각 앞을 잘라 낸다(Words `build_words.py`의 SKIP).
- **소리용 글과 화면 글 나누기:**
  - 해설 줄에서 사람 이름을 띄어 쓰면 해설자가 한숨처럼 끊긴다. 소리용 글(clips.json)에서는 붙여 쓴다(카디비, 젠슨황, 샘올트먼, 아리아나그란데, 일론머스크, 저스틴비버, 켄드릭라마, 칸예웨스트). 화면 글은 띄어 쓴다. (2026-11-10)
  - 한국어 해설 속 영어 단어(or, for)를 한국식으로 읽는 것은 고치지 않는다(성범 결정).
  - R&B는 "R and B"로 읽게 한다(`beginner_v2.py`의 `SAY`). SZA는 `/ˈsɪzə/`, TWS는 `two-us`, `&`는 `and`로 넣는다. 화면 글은 그대로다.
- 일레븐랩스 제한: 한꺼번에 많이 보내면 '대기 작업이 너무 많다'(429)로 일부를 거절하는데, 만들어지지도 과금되지도 않아 다시 만들어도 된다. 하루 생성 한도(429 daily_generation_limit_reached)는 크레딧 부족과 다르며, 한도가 풀린 뒤 빠진 조각만 만든다. 그래서 앨범 하나씩 나눠 만든다.

## 4. 효과음

| 소리 | 파일 (`spikes/episode-01/audio/raw/`) | 쓰는 곳 |
|---|---|---|
| 초급 시작음 | `sfx-start.mp3`(3초) | 초급 |
| 심화 시작음 | `sfx-start-intermediate.mp3`(원본 TOONMisc-Professional_cartoon, 2초) | 심화 |
| 고급 시작음 | `sfx-start-advanced.mp3`(원본 MUSCInst-Create_a_short_5-sec, 2초). 평균 음량이 약 5dB 커서 초급 시작음 크기로 맞춘다 | 고급 |
| 끝음 | 초급 끝음을 같이 쓴다(과정별 끝음은 안 정함) | 코스, Words |
| 다음 문제 클릭음 | `sfx-next-soft.mp3`(효과음 라이브러리 "Create a very soft U...", 1초로 자르고 4dB 줄임) | 말해보기, Words 복습, 쉐도잉 따라 하기 |
| Words 시작음 | `sfx-start-words.mp3`(MUSCInst-Cinematic_documentar, 약 2초) | Words |
| Words 단어 클릭음 | `sfx-word-click.mp3`(UIClick-soft,_appealing,_cli, -12dB) | Words |
| 쉐도잉 시작음 | `sfx-start-shadowing.mp3`(원본 UIMisc-Create_a_short_1.5_s, 3초) | 쉐도잉 |
| 팟캐스트 인트로 | 사본 없이 `audio/downloads/MUSCSmpl-playing_old_samples_-Elevenlabs.mp3`를 바로 씀 | The Replay |

효과음은 일레븐랩스 효과음에서 성범이 골랐다. 시작음과 끝음은 한 번 만들어 모든 화에 재사용해 프로그램 시그널처럼 들리게 한다. 내려받은 원본은 `audio/downloads/`(같은 이름)에 두고, 고른 것을 이름을 붙여 `audio/raw/`에 복사해 쓴다.

## 5. 비용

- 생성 1회에 대본 글자 수만큼 크레딧이 들지만, 짧은 조각도 한 번에 10~20크레딧쯤 들어 글자 수보다 많이 나온다. 긴 줄은 짧은 줄의 두 배쯤.
- 실제 측정: 초급 새 짜임 25화 약 26,850, 심화 25화 약 42,700, 고급 25화 약 5만(여러 계정 합, 같은 날 초급 다시 만들기 일부 포함), 쉐도잉 앨범 하나 약 2,700~3,100, Words 1화 2,735, 팟캐스트 앨범 하나 약 5,900~8,100.
- 구독은 몰아서 만들 때만 쓰고, 반복해서 듣는 동안 쉬었다가 다음 분량이 필요할 때 다시 구독한다.
- 무료 요금제는 월 10,000크레딧, 개인·비상업용이고 라이브러리 목소리를 API로 쓸 수 없다.

## 6. 파일과 압축

- 앱용 음성은 Opus 24kbps(webm)다(32k, 24k 시험본을 듣고 24k를 골랐다. 초급 25화 92MB → 18MB, 한 화 0.7MB 안팎). 올리는 곳은 Cloudflare R2([앱 저장과 배포](side-a-app-delivery.md)).
- 만든 조각과 결과는 `spikes/episode-01/audio/` 아래에 둔다(코스·쉐도잉·Words 조각은 과정별 폴더, 팟캐스트 부별 원본은 `audio/podcast/masters/`, 내려받은 원본은 `audio/downloads/`, 안 쓰는 시험 소리는 `audio/unused/`). 2026-11-10부터 `D:\project\uiux-study\sounds`는 쓰지 않는다. 폴더별 목록은 `spikes/episode-01/SOUNDS.md`.
