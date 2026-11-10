# 소리 파일 자리와 정리 기록

소리 파일(mp3·webm·wav)은 크기가 커서 깃에 넣지 않는다(`.gitignore`의 `spikes/episode-01/audio/`, `app/*.webm`, `app/*.mp3`). 앱이 실제로 받는 소리는 Cloudflare R2에 있고, 올린 목록은 `r2-uploaded.json`이다. 이 문서는 폴더마다 무엇이 있는지, 안 쓰게 된 소리는 왜 뺐는지 남긴다.

2026-11-10 정리: 성범이 learn-english 소리를 다른 프로젝트 폴더(`D:\project\uiux-study\sounds`)와 이중으로 관리하지 말고 learn-english 하나에서만 작업하자고 했다. 거기 있던 소리를 모두 이 프로젝트 안으로 옮기고, 지금 쓰는 것과 안 쓰는 것을 나눴다.

## 지금 쓰는 소리

| 자리 | 무엇 | 쓰는 곳 |
|---|---|---|
| `audio/downloads/` | 성범이 일레븐랩스 사이트에서 내려받은 효과음·음악 원본. **새로 내려받을 때도 여기** | 고른 것은 `audio/raw/`에 이름을 붙여 복사해 쓴다 |
| `audio/raw/` | 빌드에 쓰는 효과음 사본 | 각 빌드 스크립트 |
| `audio/podcast/masters/` | 팟캐스트 화마다 이어 붙인 원본 MP3 `album-0N-part-K.mp3` (앨범 1·2 각 4부, 앨범 3 5부) | `merge_replay.py`(The Replay 합치기), `build_podcast.py`의 트랙 MP3 폴더 |
| `audio/beginner2/`, `audio/intermediate/`, `audio/advanced/`, `audio/shadowing/`, `audio/words/` | 과정별 음성 조각과 시간표 | 각 과정 빌드 스크립트 |
| `app/*.webm` | 앱에 넣는 완성 트랙(R2에 올라감) | `build_page.py`, `template.html` |

`audio/downloads/` 원본과 `audio/raw/` 사본의 짝:

| downloads 원본 | raw 사본 | 쓰임 |
|---|---|---|
| `UIMisc-Create_a_short_1.5_s-Elevenlabs.mp3` | `sfx-start-shadowing.mp3` | 쉐도잉 시작음 |
| `UIClick-Create_a_very_soft_U-Elevenlabs.mp3` | `sfx-next-soft.mp3` | 말해보기·따라 하기 다음 줄 클릭음 |
| `UIClick-soft,_appealing,_cli-Elevenlabs.mp3` | `sfx-word-click.mp3` | 단어 시작 클릭음 |
| `MUSCInst-Cinematic_documentar-Elevenlabs.mp3` | `sfx-start-words.mp3` | 단어 시작음 |
| `TOONMisc-Professional_cartoon-Elevenlabs.mp3` | `sfx-start-intermediate.mp3` | 심화 시작음 |
| `MUSCInst-Create_a_short_5-sec-Elevenlabs.mp3` | `sfx-start-advanced.mp3` | 고급 시작음 |
| `MUSCSmpl-playing_old_samples_-Elevenlabs.mp3` | (사본 없음, 바로 씀) | The Replay 인트로 비트(`merge_replay.py`) |

## 안 쓰거나 번복된 소리 — `audio/unused/`

지우지 않고 따로 빼 두었다. 다시 쓸 일이 없다고 확정되면 지워도 된다.

| 자리 | 무엇 | 뺀 이유 |
|---|---|---|
| `unused/app-old/b1-NN.webm`, `b1-NN.mp3` | 옛 초급 1~25화 트랙 | 2026-11-09 초급을 새 짜임(표현과 예문 중심)으로 다시 써서 대본과 맞지 않는다. 앱은 `b1-NN-v2.webm`을 쓴다 |
| `unused/app-old/b1-NN-text.webm` | 음성 없을 때 대본만 보여 주던 소리 없는 파일 | 초급 25화 모두 새 음성(v2)이 생겼다. 다시 필요하면 `build_page.py`가 새로 만든다 |
| `unused/app-old/b1-01-v2g.webm`, `b1-01-v2gk.webm` | 초급 1화 구글·Gemini 음성 비교판 | 구글·Gemini 음성은 취소, 한국어·영어 모두 일레븐랩스로 정했다 |
| `unused/app-old/b1-01-voices.webm` | 해설자 목소리 오디션 트랙 | 목소리를 고른 뒤 끝난 시험 |
| `unused/app-old/episode-01.mp3` | 첫 시험 에피소드(지하철 이야기) | 이야기·대화 짜임을 버리고 과정별 짜임으로 바꿨다 |
| `unused/google-test/` | 구글 Cloud·Gemini TTS 시험 음성 | 구글 음성 취소(선불 결제 사건 뒤 일레븐랩스로 통일) |
| `unused/beginner2-variants/ep01g`, `ep01gem`, `ep01gk`, `ep08gem` | 초급 새 짜임의 구글·Gemini 비교판 | 위와 같다 |
| `unused/words-test/` | 단어 과정 첫 시험 조각 | 단어 1트랙 본 제작으로 대체 |
| `unused/compare/` | 클릭음·발음 고친 줄 비교용 | 비교 끝 |
| `unused/tws-fix/` | 한 줄 발음 고치기 시험 | 고친 줄이 본 조각에 들어감 |
| `unused/album3-pieces/p4-old/` | 앨범 3 4부의 옛 조각 | 4부를 다시 이어 붙였다(줄 사이 0.35초) |
| `unused/podcast-checks/` | The Replay 인트로·이음매 확인용 짧은 파일 | 확인 끝 |
| `unused/shadowing-tests/profanity-test/` | 쉐도잉 욕설 읽기 시험 | 시험 끝 |
| `unused/uiux-study-tests/UIClick-Crisp_cheerful_notif-Elevenlabs.mp3` | 클릭음 후보 | 고르지 않음(부드러운 클릭음으로 정함) |
| `unused/uiux-study-tests/podcast-profanity-test-mike.mp3`, `podcast-voice-test-dana.mp3` | 팟캐스트 욕설·목소리 시험 | 시험 끝(결과는 팟캐스트 설계 문서에 있다) |
| `unused/uiux-study-tests/sample-mina-coach-1.mp3`, `-2.mp3`, `speech-jessica.mp3`, `sfx-door-chime.mp3` | 첫 시험 때 목소리·효과음 견본 | 이야기 짜임과 함께 쓰지 않게 됐다 |
| `unused/uiux-study-tests/voice-test-season1/` | 시즌 1 인물 목소리 오디션 | 목소리 고른 뒤 끝난 시험 |
| `unused/uiux-study-tests/episode-01-subway/episode-01.mp3` | 첫 시험 에피소드의 다른 판 | 위 episode-01과 같은 이유 |

## 옛 uiux-study 폴더에서 옮기지 않은 것

`uiux-study/sounds`의 나머지(초급 옛 트랙 `b1-01~07.mp3`, 시즌 1 조각 `season-1-part-1/`, 첫 시험 조각 `episode-01-subway/`의 인물 목소리, `sfx-start.mp3`·`sfx-end.mp3`·`narrator-mina.mp3`·`taylor-4.mp3`·`episode-01-voice.mp3`·`episode-01.mp3`)는 이 프로젝트의 `audio/season/`, `audio/raw/`, `audio/` 에 바이트까지 똑같은 파일이 이미 있어서 복사하지 않았다.
