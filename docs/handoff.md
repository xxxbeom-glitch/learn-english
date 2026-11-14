# 인수인계 기록 (Claude와 Codex 공용)

규칙은 루트의 `AGENTS.md`. 한 줄 형식: `날짜 | 누가 | 무엇을 | 어디까지 | 고친 파일`

## 진행 중


## 끝남

- 2026-11-14 Claude: 속도 미리듣기 예문을 두 시트 모두 "I think it's going to rain today."로 통일. 크롬 확인, APK 설치. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 속도 슬라이더를 움직일 때마다 약 3초 미리듣기. 크롬 확인, APK 설치. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 음성 속도 표시에서 × 뺌(1.0처럼 숫자만). APK 설치. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 설정에 음성 속도 묶음(Audiobook 0.5~2배 `sidea-audio-x`, Game 0.5~1.5배 `sidea-game-x`) 추가. 크롬 확인, APK 설치. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 설정의 한 판 문제 수를 게임마다 따로(Sentence game, Fill the blank 두 줄과 시트 둘). 크롬 확인, APK 설치. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 게임 중 Game 탭을 다시 누르면 나가기 확인 창(결과 화면이면 바로 진입 화면). 크롬 확인, APK 설치. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 게임 개인 기록(문장별, 단어별, 헷갈린 말)과 자동 배치(새 5, 약점 3, 복습 2, 복습 간격 1/3/7/14일), 설정의 한 판 문제 수(5/10/15/20), 헤더에 게임 이름과 (n/n). 크롬 확인, APK 설치. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 빈칸 게임 빈칸 후보를 문장의 모든 단어로 넓힘(고유명사 61개와 맨 앞 감탄사 제외, 문제마다 무작위). 고유명사 목록은 새 `game_names.py`가 만들어 게임 자료 names로 R2에 올림(판 202611142031). 보기는 묶음 먼저, 모자라면 비슷한 단어. 크롬 확인, APK 설치. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, `game_names.py`(새 파일), `build_pwa.py`, `data_pack.py`, `app/game-data.js`, 빌드 결과, `data-published.json`, `side-a/www/`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 게임 결과 화면에 'Back to games' 글자 버튼(Play again 위, 배경 없음) 추가, 누르면 진입 화면. 크롬 확인, APK 설치. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 문장 게임에서 맨 앞 감탄사(oh, whoa, ha 등, 60문장)를 카드에서 빼고 답 줄 맨 앞에 흐린 글자로 미리 놓음. 크롬 확인, APK 설치. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: Game 탭 작업 정리. 끝난 팁 먼저 보기 시험 코드(`GAME_TIP_FIRST`) 지움, 진입 화면과 속도 시트 주석을 지금 모습에 맞춤. 설계 문서의 진입, 중단, 빈칸 게임 기록을 한 묶음으로 다시 씀(Figma와 게임 자료는 성범 결정으로 보류). 크롬으로 두 게임 확인, APK 설치. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 빈칸 고르기 빈칸 박스 다듬음(성범 요청): 테두리 뺌, 문장 줄 가운데 맞춤, 너비를 정답 단어 길이에 맞춤. 크롬으로 확인, APK 설치. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 두 번째 게임 'Fill the blank'(듣고 빈칸 고르기) 시험판 넣음(성범 확정, 한 판 2문제). 진입 화면 카드 두 장, 빈칸은 사각 박스, 보기 2×2. 크롬으로 진입부터 결과까지 확인, APK 설치(폰 잠겨 있어 폰에서 눌러 보기는 못 함). 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 게임 진입 카드의 단계 알약을 빼고 초록 시작 버튼 START GAME(하던 판이면 CONTINUE)을 넣음(성범 요청). 폰에서 시작과 CONTINUE 확인, APK 설치. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 게임 진입 카드를 크게, 가운데 정렬로 바꿈(성범 요청). 원 72 아이콘, 제목 Bold 26, 상태는 알약. 폰에서 화면 확인, APK 설치. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 게임 중단 넣음(성범 요청). 게임 헤더 왼쪽 속도 버튼 자리에 뒤로 버튼, 누르거나 안드로이드 뒤로 가기 하면 'Leave this game?' 확인 창, Leave면 판을 버리고 진입 화면으로. 속도 시트는 게임 화면에서 열 길이 없어짐(성범 확인 필요). 폰에서 창 열기, Cancel, Leave 확인, APK 설치. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: Game 탭 진입 화면 넣음(성범 요청). 탭을 누르면 문장 게임 카드 한 장이 먼저 나오고, 카드를 눌러야 오디오북이 멈추고 게임이 시작됨. 하던 판은 카드에 Continue로 보임, 게임 안 뒤로 가기는 진입 화면으로. 폰에서 진입, 시작, 뒤로 가기 확인, APK 설치. R2 안 올림, 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 앱 화면 손가락 확대와 두 번 눌러 확대 막음(성범 지적, 화면 설정 줄에 `user-scalable=no`). 폰 화면 비율 그대로 확인, APK 설치. 커밋 안 함. 고친 파일: `spikes/episode-01/build_pwa.py`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 당겨서 새로고침 단계 설계 넣음(성범 확정): 기준선 넘으면 진동, 놓으면 Checking… 글자, 결과별 안내(Up to date., Updated., Update ready…, Couldn't check…). 앱 VIBRATE 권한 추가. 브라우저에서 네 가지 결과 확인, APK 폰 설치. 폰에서 진동 확인은 아직. R2 안 올림, 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, `side-a/android/app/src/main/AndroidManifest.xml`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-delivery.md`.
- 2026-11-14 Claude: 설정에서 Download all audio와 Wi-Fi only를 뺌(성범 결정, 한 번 들은 화는 폰에 남는 캐시 방식이라). Storage used, Delete downloads는 남김. 브라우저 확인, APK 폰 설치. R2 안 올림, 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, `spikes/episode-01/build_pwa.py`(설명 글만), 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-delivery.md`, `side-a-app-screens.md`.
- 2026-11-14 Claude: 성범 폰 시험용으로 Test Album을 서버에 올렸다가(판 202611141859) 빼고 원래 목록으로 되돌림(판 202611141900). 같은 분 안에 두 번 올리면 판 번호가 같아 폰이 못 알아보던 문제를 `data_pack.py`에서 고침(올린 판보다 항상 크게). 커밋 안 함.
- 2026-11-14 Claude: 홈에서 당겨서 새로고침 넣음(성범 요청, 아이콘 없이 화면이 따라 내려옴), 돌아올 때 반영이 늦던 기다림 두 가지(2초, 켤 때 2.5초) 없앰. 서버에 시험 앨범(Test Album)을 올려 폰에서 반영 확인(판 202611141832) 뒤 원래 목록으로 되돌려 올림(판 202611141835). 브라우저에서 당기기, Up to date, 새 판 반영 확인. APK 폰 설치, 폰에서 당겨 보기는 아직. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-delivery.md`, `spikes/episode-01/data-published.json`.
- 2026-11-14 Claude: 앱을 끄지 않아도 새 판 반영. 돌아올 때마다 판 확인(30초 중복 방지, 옛 10분 제한 없앰), 재생, 게임, 받기, 시트 중이면 기다렸다가 멈추거나 나갈 때 다시 불러오기, 다시 불러온 뒤 보던 화면, 스크롤, 듣던 위치 유지(시작 애니메이션 없음). 브라우저에서 판 번호를 올려 확인. APK 폰 설치, 폰에서 눌러 보기는 아직. R2 안 올림, 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-delivery.md`.
- 2026-11-14 Claude: 한 번 들은 화의 소리를 폰(`audio-v1`)에 남겨 다음부터 저장본으로 바로 재생, 옛 판 소리 파일 자동 정리, 다운로드 지우기 때 함께 지움. 브라우저에서 저장, 0.03초 재생, 옛 판 지우기, 다운로드 지우기 확인. APK 폰 설치(화면이 잠겨 폰에서 눌러 보기는 못 함). R2 안 올림, 커밋 안 함. 그리고 오늘 앞선 APK 두 번은 `copy-web` 단계 없이 만들어 화면 코드가 옛것이었음(이번 APK에는 다 들어감). 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `side-a/www/`, `docs/superpowers/specs/side-a-app-delivery.md`.
- 2026-11-14 Claude: 재생 2~3초 지연 재확인. 무선 디버깅으로 폰 앱 안을 재 보니 누르고 소리 시작까지 0.15~0.5초(Level 1, 쉐도잉, 팟캐스트, 다운로드 없는 상태). 늦은 순간은 못 잡음. 짐작: R2 개발용 주소(r2.dev)의 일시적 느림이나 새 판 받기와 겹침. 코드 안 바꿈, 원래 APK 다시 설치, 커밋 안 함. 고친 파일: `docs/handoff.md`.
- 2026-11-14 Claude: 트랙 눌러 재생까지 2~3초 걸린다는 제보 확인. 폰에서 재 보니 0.06~0.2초라 고치지 않음(성범도 "이제 잘되는데"). 커버 교체 직후 새 판을 받던 때의 일로 보임. 재려고 잠깐 디버그 켠 APK를 깔았다가 원래 APK(새 커버 포함)로 다시 설치함. 코드 안 바꿈, 커밋 안 함. 고친 파일: `docs/handoff.md`.
- 2026-11-14 Claude: Level 1~4 앨범 커버를 Figma cover_lv1~4로 교체하고 앨범 색도 커버 바탕색으로 바꿈. R2 판 202611141327 올림(폰은 앱 다시 켜면 반영). APK는 빌드만, 폰 연결 안 돼 설치 안 함. 커밋 안 함. 고친 파일: `spikes/episode-01/app/cover-b0~b3.webp`, `spikes/episode-01/albums.json`, 빌드 결과, `data-published.json`, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: Figma 안 쓰는 화면 10장(01 홈, 07 설정, 27 설정 탭, 01b, 옛 21, 안 A, B, C, 24, 24c)을 '99 보관' 페이지 새 구역 '보관 · 2026-11-14 안 쓰는 화면 정리'로 옮김(지운 것 없음). 04 에셋 페이지의 이름 없는 그림 10개는 그대로 둠. 커밋 안 함. 고친 파일: Figma EN-AudioBook, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 맞음 판 뜻 줄과 영어 정답 문장을 다시 가운데 정렬(팁 박스만 왼쪽). APK 폰 설치함. 코드만 바뀌어 R2 안 올림. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 게임 팁을 1,294문장 모두에 닮(새로 866개, 5~8묶음). 앱 반영, R2 판 202611140159 올림(tips 1,294개 확인), APK 폰 설치. 커밋 안 함. 고친 파일: `content/game/tips-batch-05.md`~`08.md`(새로), `tips-batch-05.md`, `06.md` 각 한 줄 손봄, 빌드 결과, `docs/superpowers/specs/side-a-app-screens.md`.
- 2026-11-14 Claude: 게임 팁 먼저 보기 시험 끔(`GAME_TIP_FIRST = false`), 맞음 판 정답 문장과 뜻 왼쪽 정렬, APK 폰 설치. 코드만 바뀌어 R2는 안 올림. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `docs/superpowers/specs/side-a-app-screens.md`.

- 2026-11-14 Claude: 게임 팁 3, 4묶음(194 + 166) 써서 팁 모두 428개, 앱 빌드, APK 폰 설치, R2 올림(판 202611140141). `GAME_TIP_FIRST` 시험은 아직 켜 둠. 커밋 안 함. 고친 파일: `content/game/tips-batch-03.md`, `tips-batch-04.md`(새), 빌드 결과, `data-published.json`, `docs/superpowers/specs/side-a-app-screens.md`.

- 2026-11-14 Claude: 게임 팁 2묶음 중 어려운 팁 8곳(5, 8, 19, 34, 35, 38, 40, 45번) 쉽게 고치고 APK 폰 설치. 커밋 안 함. 고친 파일: `content/game/tips-batch-02.md`, 빌드 결과, `docs/superpowers/specs/side-a-app-screens.md`.

- 2026-11-14 Claude: 게임에 팁 먼저 보기 시험(`GAME_TIP_FIRST = true`, 한 판을 팁 달린 문장으로만) 넣고 APK 폰 설치. 시험 끝나면 false로 되돌릴 것. 커밋 안 함. 고친 파일: `spikes/episode-01/app/template.html`, 빌드 결과, `docs/superpowers/specs/side-a-app-screens.md`.

- 2026-11-14 Claude: 게임 팁 2묶음 45개 써서 성범 검수("그대로 넣어줘") 뒤 앱에 넣고 APK 폰 설치(앱 안 팁 67개). R2 안 올림, 커밋 안 함. 고친 파일: `content/game/tips-batch-02.md`(새), `spikes/episode-01/app/game-data.js` 등 빌드 결과, `docs/superpowers/specs/side-a-app-screens.md`.

- 2026-11-14 | Claude | 게임 팁 22개 앱에 넣음(원본 content/game/tips-*.md, game_tips.py가 game-data.js와 R2 묶음에 넣음, 시험용 팁 지움), APK 폰 설치 | 끝. R2 올리기는 안 함(앱 안 팁으로 동작), 커밋 안 함 | `content/game/tips-pilot-20.md`, `spikes/episode-01/game_tips.py`, `spikes/episode-01/build_pwa.py`, `spikes/episode-01/data_pack.py`, `spikes/episode-01/app/template.html`, `spikes/episode-01/app/game-data.js`, `docs/superpowers/specs/side-a-app-screens.md`, `docs/handoff.md`
- 2026-11-14 | Claude | 게임 팁 20개를 '그 문장에서 짚을 핵심이 맞는지'로 점검, 4개 바꿈(1, 7, 14, 15) | 끝. 성범 검수 대기, 앱에는 아직 안 넣음, 커밋 안 함 | `content/game/tips-pilot-20.md`, `docs/superpowers/specs/side-a-app-screens.md`, `docs/handoff.md`
- 2026-11-14 | Claude | 게임 팁 20개 점검(5개 고침, 두 줄 길이 확인), 팁 쓰기 점검 규칙 6가지 설계 문서에 적음 | 끝. 성범 검수 대기, 앱에는 아직 안 넣음, 커밋 안 함 | `content/game/tips-pilot-20.md`, `docs/superpowers/specs/side-a-app-screens.md`, `docs/handoff.md`
- 2026-11-14 | Claude | 게임 팁 시험 20개를 문법 11, 어휘 9로 고침(소리 팁 뺌, 과거형과 미래형 팁 더함) | 끝. 성범 검수 대기, 앱에는 아직 안 넣음, 커밋 안 함 | `content/game/tips-pilot-20.md`, `docs/superpowers/specs/side-a-app-screens.md`, `docs/handoff.md`
- 2026-11-14 | Claude | 게임 팁 시험 20개 초안(쓰임 12, 뜻 5, 소리 3) | 끝. 성범 검수 대기, 앱에는 아직 안 넣음, 커밋 안 함 | `content/game/tips-pilot-20.md`, `docs/handoff.md`
- 2026-11-14 | Claude | 게임 팁에 쓰임 팁(예: these는 언제 쓰는지) 더하고, 팁을 다는 문장을 넓히기로 기록 | 끝. 설계만, 팁 글은 아직, 커밋 안 함 | `docs/superpowers/specs/side-a-app-screens.md`, `docs/handoff.md`
- 2026-11-14 | Claude | 게임 헤더 하트(Figma 21, 22, 22b, 23, 25), 앱에 하트 토글(세 배 출제, 겹치면 큰 쪽)과 팁 박스(24e), 건너뛰기와 skip 기록 없앰, APK 폰 설치 | 끝. 팁 글은 시험용 1개뿐(진짜 팁 20개는 아직), 폰에서 눌러 보기 남음, 커밋 안 함 | Figma SideA, `spikes/episode-01/app/template.html`, `spikes/episode-01/app/episode-01.html`, `spikes/episode-01/web/`, `docs/superpowers/specs/side-a-app-screens.md`, `docs/handoff.md`
- 2026-11-14 | Claude | 게임 팁 박스는 24e(박스 안 첫 줄 'Tip' 제목)로 확정 기록 | 끝. 코드와 APK, 21~23, 25번 헤더 하트 교체는 아직, 커밋 안 함 | `docs/superpowers/specs/side-a-app-screens.md`, `docs/handoff.md`
- 2026-11-14 | Claude | 팁 라벨 아이콘 빼고 회색 바탕과 진한 글자로 바꿈(24c), 비교 시안 24e(팁 제목을 박스 안 첫 줄로) 그림 | 끝. 24c와 24e 중 성범 선택 대기, 커밋 안 함 | Figma SideA, `docs/superpowers/specs/side-a-app-screens.md`, `docs/handoff.md`
- 2026-11-14 | Claude | 게임 하트를 헤더 오른쪽(건너뛰기 자리)으로 옮기고 건너뛰기 없앰, 팁을 박스에 걸친 사각 라벨로 바꿈(시안 24c, 24d), 아이콘 컴포넌트 heart, heart-fill, lightbulb 추가 | 끝. 시안과 설계만, 21~23, 25번 헤더와 코드는 아직, 커밋 안 함 | Figma SideA, `docs/superpowers/specs/side-a-app-screens.md`, `docs/handoff.md`
- 2026-11-14 | Claude | 게임 맞음 판 하트와 팁 박스 Figma 시안 24c(하트 끔, 팁 있음), 24d(하트 켬, 팁 없음) 그림 | 끝. 시안만, 코드와 APK는 아직, 커밋 안 함 | Figma SideA '02 화면' 게임 구역, `docs/superpowers/specs/side-a-app-screens.md`, `docs/handoff.md`
- 2026-11-13 | Claude | 게임 맞음 판의 하트(세 배 출제)와 팁 박스(뜻 팁, 소리 팁, 20개 먼저 검수) 방향 정함 | 끝. 설계만, 화면과 팁 글은 아직 안 만듦, 커밋 안 함 | `docs/superpowers/specs/side-a-app-screens.md`, `docs/handoff.md`

- 2026-11-13 | Claude | Level 1과 Level 2에 같은 문장 3개의 한국어 뜻을 Level 2에 맞춤, 2화와 5화 음성 다시 잇고 R2 판 202611132146 | 끝 | `content/stories/course-basics.md`, `spikes/episode-01/audio/basics/ep02/`, `spikes/episode-01/audio/basics/ep05/`, `docs/superpowers/specs/side-a-courses.md`

- 2026-11-13 | Claude | Level 1 뼈대 3~14화 대본과 음성 | 끝. 3~14화 대본, 음성, R2(판 202611132139). 4~14화는 성범 지시로 글 검수 없이 진행, 폰 듣기 확인 남음, 커밋 안 함 | `content/stories/course-basics.md`, `spikes/episode-01/audio/basics/ep03~ep14/`, `spikes/episode-01/app/episode-01.html`, `spikes/episode-01/data-pack/`, `docs/superpowers/specs/side-a-courses.md`

- 2026-11-13 | Claude | 임시 'Game sounds' 화면에 'To check'와 'Checked' 탭, 재생한 문장은 Checked로 옮김. APK 새로 만들어 폰에 설치함 | 끝 | `spikes/episode-01/app/template.html`, `docs/superpowers/specs/side-a-app-screens.md`

- 2026-11-13 | Claude | `AGENTS.md`에 Codex 규칙(결과는 초안, 방향은 새로 정하지 않고 '확인 필요')과 넘기기 규칙(3절, 모델 표 자리) 더함. Codex(gpt-6.1-sol)로 Level 1 3화 예문 5개 초안 시험, 56,432토큰, 대본 파일에는 넣지 않음 | 끝 | `AGENTS.md`, `docs/handoff.md`

- 2026-11-13 | Claude | 게임 문장 19개 앞 삑 소리 고쳐 R2 판 202611132028로 올림, 설정에 임시 'Game sounds' 듣기 화면, 길게 눌러 글자 선택 막기(APK 새로 만들어 폰에 설치함) | 끝 | `spikes/episode-01/build_game.py`, `spikes/episode-01/game-cut-fix.json`, `spikes/episode-01/app/template.html`, `docs/superpowers/specs/side-a-app-screens.md`

- 2026-11-13 | Claude | 공동 작업 규칙 `AGENTS.md`와 이 기록 파일 만들기 | 끝 | `AGENTS.md`, `CLAUDE.md`, `docs/handoff.md`
