# Side A 팟캐스트: The Replay, Seoul, Actually, Behind the Brand

목차는 [2026-11-07-story-audio-english-design.md](2026-11-07-story-audio-english-design.md). 공통 규칙 [side-a-rules.md](side-a-rules.md)은 이 문서가 따로 정하지 않는 한 그대로 따른다. 옛 팟캐스트 기획서 전문(4부 나누기, 앨범별 앱 반영 기록, 제작 로그)은 [archive/2026-11-09-podcast-album-design.md](archive/2026-11-09-podcast-album-design.md).

## 1. 영어 팟캐스트 공통 (The Replay, Seoul, Actually)

**의도:** 코스가 교재라면 팟캐스트는 **틀어 두는 영어**다. 운동하거나 일할 때 흘려들으며 귀를 트이게 한다. 대부분을 알아들어야 하므로 성범이 잘 아는 주제와 이름(래퍼, 곡, 아이돌, 한국 음식)을 넣어, 아는 말이 들리면 나머지도 따라 들리게 한다.

- 목표: 미국 사람들의 방송을 엿듣는 느낌. 흘려들어도 흐름을 놓치지 않는다.
- 하지 않는 것: 한국어 해설, 도입, 따라 말하기, 다시 듣기. 음성은 처음부터 끝까지 영어다. 성범은 나오지 않는다. 실제 래퍼나 아이돌이 직접 나와 말하는 설정도 없다.
- 실패: 듣기평가처럼 끊어 읽음 / 너무 어려움 / 한마디씩 탁구처럼 주고받아 문장 하나를 끝까지 못 들음 / 실존 인물에 대해 사실이 아닌 말.

**진행자와 리듬**
- 사회자와 게스트 두 사람. 사회자 Mike(미국 남자, E)는 모든 앨범에서 같은 사람이고, 게스트(가상 인물, 여자)는 앨범마다 바뀐다.
- 한 명이 끌고 가고 다른 한 명이 가끔 받아친다. 2~4문장씩 이어 말하고 받는 쪽은 짧게 반응한다. 게스트가 혼자 길게 말하지 않게 2~4문장마다 사회자가 끊는다.
- 사회자 질문은 초급 패턴(`Do you like ~?`, `What's ~?`, `How was ~?`, `Did you ~?`)으로 쓴다.

**난이도:** 속도는 원어민 그대로(멈칫, 웃음, 맞장구 포함), 쉽게 만드는 일은 대본에서 한다. 문장은 대부분 3~8단어, 단어는 초급~심화(장르 말 beat, drop, verse, feature는 이름과 함께면 됨), 아는 이름을 자주 넣고, 핵심 말은 한 번 더 말한다(`It has twenty-three songs. Twenty-three!`). 음성 자체를 느리게 만들지 않는다. 앨범이 늘수록 대본을 조금씩 어렵게 한다.

**실존 인물과 사실**
- 하지 않은 말이나 일을 지어내지 않는다. 썰은 널리 보도된 것만 쓰고, 곡 속 폭로나 비난은 "켄드릭이 곡에서 이렇게 말했다", "드레이크는 부인했다"처럼 누가 어디서 한 말인지로 전한다. 소송은 보도된 결과까지만.
- 진행자가 편을 들거나 놀리는 것은 가상 인물의 의견이라 괜찮다. 실존 인물의 사생활을 새로 꾸미지 않는다.
- 발매일, 곡 수, 순위는 출처로 확인해 대본 파일에 적는다. 가사는 인용하지 않는다.

**욕:** The Replay는 디스전 이야기라 욕(fuck, shit, damn)과 성적인 단어를 가리지 않고 쓴다. 혐오 표현(n-word 등)은 쓰지 않는다. 일레븐랩스는 욕을 삐 소리 없이 읽는다(2026-11-09 시험, `audio/unused/uiux-study-tests/podcast-profanity-test-mike.mp3`).

**한국어 말:** 한국 이름, 음식, 장소는 한국말 그대로 나와도 된다. 한국어 문장과 요즘말은 섞지 않는다. 미국인 진행자는 한국 이름을 살짝 서툴게 발음할 수 있다. 가사 표기는 공통 규칙대로.

**앱 표시:** 가사는 영어 줄마다 한글 뜻을 붙이고, 더보기 시트의 Korean translation 스위치로 끄고 켠다. 한글 뜻은 대본을 쓸 때 줄마다 함께 쓴다(번역투 금지). 가사 구간 이름은 talk(코스의 dialogue와 구분).

**화자 표시 (2026-11-10 성범 요청):** 둘 이상이 대화하는 화(The Replay: Mike와 Dana, Mike와 Tasha)는 가사 줄 앞에 `Mike:`처럼 화자 이름을 단다. 쉐도잉 가사와 같은 모양(`.who`, 흐리게)이다. 이름은 대본의 `**Mike:**` 표시가 시간표(`audio/podcast/*.json`의 speaker)에 이미 들어 있어 그대로 쓴다. 음성은 다시 만들지 않았다. 혼자 말하는 Seoul, Actually(매디)에는 달지 않는다. 기준은 화의 출연자(cast)가 둘 이상인지다(`template.html` lineHtml).

**대본과 검수:** Claude가 새로 쓰고, 한 앨범씩 글로 먼저 보여 준다. 별도 AI가 ① 영어 ② 상황 ③ 사실(출처 대조) ④ 난이도 ⑤ 듣기 ⑥ 한글 뜻을 본다.

**음성:** 일레븐랩스 Eleven v4. 두 목소리를 한 번에 섞을 수 없어 말하는 차례마다(혼자 하는 방송은 줄마다) 한 번씩 만들고(다시 만들기 없음) ffmpeg로 잇는다. 차례 사이 0.35초, 전체 -16 LUFS, 속도 1.0. 만들기: `python build_podcast.py <조각 폴더> <트랙 MP3 폴더(audio/podcast/masters)> <앨범 번호>` → `merge_replay.py`(The Replay) → `build_page.py` → `build_pwa.py`. `build_podcast.py`는 대본 파일이 있는 만큼 부를 읽고, 조각 수가 줄 수와 같으면 줄마다 한 조각으로 본다.

## 2. The Replay (채널 앨범 하나)

- 홈에 채널 앨범 하나: 이름 The Replay(앱 안 한글 이름 '더 리플레이'), 소개 "Rap's biggest stories, retold", 표지 replay1. 홈 카드는 'The Replay / 17 min'.
- **한 트랙으로 합침 (2026-11-10):** 처음엔 앨범마다 4부로 나눴으나, 지금은 앨범 하나가 트랙 하나다. 새로 녹음하지 않고 2~4부 첫머리의 "we're back, last time" 요약과 앞 부 끝과 겹치는 질문만 잘라 냈다(드레이크 3부 첫 줄은 "We're back."만 뺌). 부 사이 0.4초. `spikes/episode-01/merge_replay.py`, 부별 시간표는 `audio/podcast/parts/`. 대본 파일(`content/podcasts/album-0N-part-K.md`)은 부별 원본 그대로 둔다.
- 앱 기록 옮기기: 화 자리가 6칸 당겨져 폰의 들은 기록을 앱이 한 번 옮긴다(합친 트랙은 네 부를 다 들었을 때만 다 들음, 들던 위치는 처음, 받아 둔 표시는 지움). 옮긴 뒤 lay=1을 저장해 다시 옮기지 않는다.
- **인트로 음악 (2026-11-10):** 두 트랙 앞에 힙합 비트(MUSCSmpl-playing_old_samples_-Elevenlabs.mp3, 6.7초를 반복). 처음 2.5초는 음악만, 인사가 시작되면 0.2배로 줄였다가 11초부터 6초 동안 페이드아웃. 성범이 좋다고 했다.

| 트랙 | 한글 부제 | 게스트 | 길이 | 줄거리와 출처 |
|---|---|---|---|---|
| EP1: Drake vs Kendrick | 드레이크와 켄드릭의 디스전 | Dana(힙합 기자), "Brittney – Casual Podcaster" `iNwc1Lv2YQLywnCvjfn1` | 8:05 | `content/podcasts/album-01-drake-kendrick-outline.md` |
| EP2: Young Thug and the YSL Trial | 래퍼 영떡의 YSL 갱단 재판 | Tasha(애틀랜타 법원 기자, E), "Mia – Lively, Crisp, Expressive" `052jzHJceQiZr7ltnY0C` | 9:23 | `content/podcasts/album-02-young-thug-ysl-outline.md` |

- 사회자 Mike: "Mike – Podcast Host Voice" `vDchjyOZZytffNeZXfZK`.
- EP1: 2013 "Control" 벌스와 빅3, 2023 "First Person Shooter", 2024 "Like That" → 주고받은 곡들("Push Ups", "Taylor Made Freestyle", "Euphoria", "Family Matters"와 "Meet the Grahams", "Not Like Us") → J. Cole 사과, "The Story of Adidon", 폭로와 부인, 드레이크의 음반사 소송 → 차트, 그래미, 슈퍼볼.
- EP2는 실제 형사 사건이라 더 조심한다. 법원이 정한 것만 사실로 말하고, 피해자와 사건 세부는 말하지 않으며, 유출 통화 내용은 다시 퍼뜨리지 않는다. 거너가 밀고했는지는 판단하지 않고, 곡이 누구 얘기인지는 팬 해석이라고 분명히 한다. 욕은 EP1보다 줄였다.
- 옛 부제 '조지아 역사상 가장 긴 재판'은 이해가 잘 안 된다고 해서 바꿨다.

## 3. Seoul, Actually (매디의 서울 여행)

- 1인 방송. 진행자 Maddie(오하이오 출신 22살 대학생, 첫 혼자 여행, 밝고 솔직함, 세븐틴 팬 캐럿)가 5일 서울 여행을 1부(1일차)~5부(5일차)로 푼다. 성범은 나오지 않는다("나 개입시키지마").
- 목소리 "Hayley - Natural TikTok & UGC" `gpmRbxMkenLwiGmvYotk`. 욕은 넣지 않는다. 한국어는 음식, 장소 이름과 서툰 "Kamsahamnida"만.
- 단어는 미국인 시점(sheet masks, "basically Korean Sephora", mayak kimbap, love locks, buskers, Papago). 미국인 후기에 자주 나오는 놀람(쓰레기통 없음, 밤에도 안전, 네이버 지도, 조용한 지하철, 고깃집 2인분, 찜질방, 티머니 현금 충전)을 넣었다.
- 세븐틴 팬미팅과 음악방송 녹화는 지어낸 행사다. 2026년 10월 군 복무를 고려해 다섯 명(에스쿱스, 정한, 조슈아, 준, 디에잇)만 나온다고 한다(출처는 3부 메모).
- 대본 `content/podcasts/album-03-part-1.md`~`part-5.md`. 앱에서는 쇼 이름 Seoul, Actually, 소개 "Maddie's solo trip to Seoul, no cap", 표지 `app/cover-seoul.webp`(바탕 #8f8c7a). 홈 카드는 'Seoul, Actually / 11 min'. 트랙에는 EP 번호를 그대로 붙인다(Day One~Day Five). 앱 안 이름(course)은 `매디의 서울 여행`.
- 남은 것: 대본의 `[softly]` 네 줄(1부 19, 3부 16, 5부 1과 14)을 다시 만들지는 성범이 정한다.

## 4. Behind the Brand (가칭, 2026-11-10 기획, 보류)

- 새 카테고리. 한 화에 브랜드 하나의 재미있는 역사와 자기계발 이야기를 10~15분 한 트랙으로 푼다(구간을 나누지 않는다).
- 호스트 케이시(한국인 여자)는 한국어에 영어를 섞는 이태원식으로 묻고, 게스트 제이크(서울 10년차 미국인 테크 기자, 한국어는 알아듣는다)는 영어로 답한다. 영어를 다 못 알아들어도 따라갈 수 있다. (성범 결정, 게스트 설정은 `작성자 판단`)
- 가사는 줄마다 번역: 영어 줄 아래 한국어, 케이시 줄 아래 영어.
- 1화 Apple 대본 초안 `content/podcasts/brand-01-apple.md`. 저장만 하고 보류. 검수, 사실 14개 확인, 음성 모두 전.

## 5. 나중에 (사용자 구상, 지금 만들지 않음)

- 기본 커리큘럼 밖의 장문 콘텐츠: 성범이 책을 읽고 필사한 하이라이트 문장, 옛날 주요 사건을 혼자 길게 말하는 스피칭과 해설.
- 케이팝·케이컬처 주제의 The Replay 회차(한국계 미국인 유튜버 게스트 등).
