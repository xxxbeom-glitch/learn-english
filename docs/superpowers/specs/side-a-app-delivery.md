# Side A 앱 저장, 소리 받기, 배포, 네이티브 앱

목차는 [2026-11-07-story-audio-english-design.md](2026-11-07-story-audio-english-design.md). 화면은 [side-a-app-screens.md](side-a-app-screens.md). 개발 계획과 단계별 결과는 `docs/archive/plans/2026-11-09-side-a-android-app.md`.

## 1. 앱 형태

- **안드로이드 네이티브 앱으로 낸다 (2026-11-09):** 지금 만든 웹 코드(HTML, CSS, JS 한 장짜리 앱)를 Capacitor로 감싼다. 처음부터 다시 짜지 않는다. 그래서 상태 표시줄과 아래 버튼 바 뒤까지 배경을 깔 수 있고, 내려받기와 폰 안 예약 알림을 쓸 수 있다. 앱 폴더는 `side-a/android`.
- 플레이스토어에 올리지 않고 설치 파일(APK)을 폰에 직접 깔아 혼자 쓴다. 설치는 갤럭시 보안폴더에 같이 깔리지 않게 `adb install --user 0`.
- 설치형 웹앱(Vercel 프로젝트 `iyagi-english`, https://iyagi-english.vercel.app)과 아티팩트는 개발 중 확인용으로 계속 쓴다. 앱 출력 확인은 아티팩트로 올려 아티팩트 창으로 연다. 주소는 아는 사람이면 열 수 있고 검색 노출은 막았다.
- 처음 기획의 React, Vite, Dexie 앱은 만들지 않았고 한 장짜리 앱이 그 자리를 대신한다.
- 디자인, 개발 계획, 개발, 배포는 성범이 지시할 때 시작한다.

## 2. 만드는 순서

- 화면: `spikes/episode-01/app/template.html` → `spikes/episode-01/build_page.py`가 소리 목록과 커버를 넣어 아티팩트용 한 장짜리 `app/episode-01.html`을 만든다.
- 소리를 새로 만들면: `build_page.py` → `upload_r2.py` → `build_pwa.py`.
- 화면 코드만 바꿨을 때(2026-11-13): `fill_template.py` → `build_pwa.py`. `fill_template.py`는 지금 있는 `app/episode-01.html`의 데이터(시간표, 대본, 커버)를 그대로 두고 template의 화면 코드만 새로 넣는다. 자른 쉐도잉 소리가 R2에 올라가기 전에는 `build_page.py` 대신 이것을 쓴다.
- 문장 게임의 정답·오답 효과음 `app/sfx-correct.mp3`, `app/sfx-wrong.mp3`는 R2가 아니라 앱 안에 넣는다(`build_pwa.py`가 복사).
- 문장 게임의 문제 소리 `app/game/*.webm`(1,294개, 약 12MB)은 R2의 `audio/game/`에 올린다(`upload_game_r2.py`, 2026-11-13 성범 요청. 같은 날 먼저는 앱 안에 넣었다). 목록 `app/game-data.js`만 앱 안에 넣는다. `build_game.py`가 만든다.
- **받기는 설정 한 곳에서 (2026-11-13):** 앨범 전체 받기 단추를 없애고 설정의 Download all audio가 모든 소리(화, 쉐도잉 해설, 게임. 약 91MB)를 여섯 개씩 동시에 받아 `audio-v1`에 넣는다. 아래 '앨범 전체 받기' 설명은 옛 방식이고, Wi-Fi only와 저장본 쓰는 방식은 그대로다. `build_page.py`를 다시 돌려 시간표가 바뀌면 `build_game.py`도 다시 돌린다.
- **내용을 고쳤을 때 (2026-11-13):** `build_pwa.py` → `publish_data.py`. 설치 없이 폰에 반영된다(아래 3-1). 게임 문장의 뜻을 고쳤으면 그 앞에 `build_game.py --list`, 소리가 바뀌었으면 그 앞에 `upload_r2.py`나 `upload_game_r2.py`.
- 웹: `build_pwa.py`가 `web/`을 만들고(설치 설정 manifest, 아이콘 Lucide headphones, sw.js), `web/`에서 `npx vercel deploy --prod --yes`.
- 앱: `build_pwa.py` 결과를 Capacitor로 감싸 APK를 만든다(자세한 단계는 개발 계획).

## 3. 소리 파일: Cloudflare R2 (2026-11-09 결정, 2026-11-10 옮김 완료)

- 앱이 쓰는 모든 소리(코스, 팟캐스트, 쉐도잉, Words, 효과음)는 R2에 올리고 앱은 R2 주소에서 받는다. 앱 안에는 소리가 없다(APK 74MB → 6MB). Firebase 저장소에는 소리를 두지 않는다.
- 통 `side-a-audio`, 공개 주소 `https://pub-54e325ce90af4f1bad3644fc22432096.r2.dev/audio/<파일 이름>.webm`. CORS는 모든 곳에서 GET/HEAD와 Range 머리글 허용. 계정은 `Psblove88@gmail.com's Account`이고, 같은 계정의 `tampin-media-prod` 통은 다른 앱 것이라 건드리지 않는다.
- `spikes/episode-01/upload_r2.py`가 화면이 쓰는 `app/*.webm`만 올리고, 같은 내용은 `r2-uploaded.json`의 내용 지문으로 건너뛴다. `build_pwa.py`는 소리 주소를 R2 주소 + `?v=지문`으로 바꿔 다시 만든 화는 새로 받게 한다.
- 올리는 규칙: 소리를 새로 만들거나 다시 만들면 같은 작업에서 R2에도 올린다. 앱이 받을 목록(화별 소리 주소)은 앱 안의 콘텐츠 목록에 적는다.
- 무료 범위는 한 달 저장 10GB, 올리기 100만 번, 읽기 1,000만 번, 내려받는 양 무료. 2026-11-09에 `tampin-media-prod`가 3.25GB를 써서 약 6.7GB가 남았다. 10GB를 넘기기 전에 성범에게 먼저 알린다.
- R2 주소를 아는 사람이 받는 것까지는 막지 않는다.

## 3-1. 내용과 커버도 R2에서 받는다 (2026-11-13 성범 요청)

- **무엇을:** 대본과 시간표, 게임 문장, 앨범 커버와 프로필 사진. 전에는 APK 안에만 있어서 뜻 하나를 고쳐도 다시 설치해야 했다. 이제 R2에 올리면 앱을 다시 켤 때 설치 없이 반영된다.
- **R2에 두는 파일 (`data/` 아래, 공개 주소 `https://pub-54e325ce90af4f1bad3644fc22432096.r2.dev/data/`):**

| 파일 | 내용 | 크기 |
|---|---|---|
| `manifest.json` (목록) | 판 번호 `v`, 묶음 모양 번호 `fmt`, 아래 파일들의 이름. 캐시하지 않는다(`no-store`) | 약 1KB |
| `content-지문.json` | `eps`(시간표), `scripts`(대본), `mb`(전체 소리 크기). 소리 주소는 R2 주소 + `?v=지문`이라 소리와 시간표가 한 판으로 묶인다 | 약 1.6MB |
| `game-지문.json` | `ver`, `audio`, `bank`. `app/game-data.js`와 같은 내용 | 약 0.1MB |
| `cover-이름-지문.webp` 14장 | `app/cover-*.webp` | 모두 약 0.3MB |

- **판 번호:** 올린 날짜와 시간(예 202611131308). 큰 쪽이 새 판이다. 파일 이름에는 내용 지문이 들어가서 이름이 같으면 내용도 같고, 그래서 r2.dev의 하루짜리 캐시에 걸리지 않는다. 앱은 이름이 달라진 파일만 받는다.
- **만들고 올리기:** `build_pwa.py`가 `data_pack.py`로 `data-pack/`에 묶음을 만들고 그 목록을 앱 안에 기본 복사본 표시로 넣는다. `publish_data.py`가 바뀐 파일만 올리고 목록을 맨 마지막에 올린다. 올린 목록은 `data-published.json`에 적는다. 빠르게 올리려면 `SIDEA_WRANGLER`에 wrangler.js 경로를 준다.
- **앱이 하는 일 (`template.html` 맨 아래 부팅 코드):**

| 상황 | 동작 |
|---|---|
| 켤 때, 새 판 없음 | 목록만 확인하고 지금 가진 판으로 켠다 |
| 켤 때, 새 판 있음 | 시작 애니메이션이 도는 동안 2.5초까지 기다려 바뀐 파일을 받고 새 판으로 켠다. 그 안에 못 받으면 지금 판으로 켜고, 마저 받아 다음에 적용한다 |
| 인터넷 없음 | 폰에 저장된 묶음, 없으면 APK에 든 기본 복사본으로 켠다 |
| 앱을 끄지 않고 돌아옴 | 10분에 한 번 확인한다. 새 판을 받았고 재생 중도 게임 중도 받는 중도 아니면 새로 켠 것처럼 다시 그린다. 아니면 다음에 켤 때 적용한다 |

- **폰 저장:** 받은 것은 `data-v1` 저장소의 `/live.json` 한 묶음으로 둔다(커버는 그림 자체를 글자로 바꿔 넣어 인터넷 없이도, 잠금 화면 알림에도 보인다). Delete downloads는 소리(`audio-v1`)만 지우고 이 묶음은 남긴다. Wi-Fi only는 내용 확인에 적용하지 않는다(작아서).
- **기본 복사본:** APK에는 지금처럼 내용과 커버가 전부 들어 있다(약 2MB). 처음 켤 때와 인터넷이 없을 때 쓴다. 저장된 묶음이 APK의 기본 복사본보다 옛 판이면 기본 복사본을 쓴다.
- **본문 스크립트는 부팅 뒤에 돈다:** `template.html`의 본문은 `<script type="text/sidea" id="main">`에 두고, 부팅 코드가 묶음을 준비한 뒤 실행한다. 목록이 없는 페이지(아티팩트용 `app/episode-01.html`)는 기본 복사본만 쓴다.
- **화면 표시는 없다:** 설정에 판 번호를 보이는 줄(Content)은 성범이 넣지 않기로 했다(2026-11-13).
- **Download all audio**는 그대로 소리만 받는다. 내용과 커버는 켤 때 저절로 받아 저장된다.
- 확인(2026-11-13, 브라우저): 새 판이 없을 때 목록만 확인, 뜻 하나와 커버 한 장을 바꿔 올리면 그 두 파일만 받아 같은 실행에서 바뀜(약 1초), R2에 닿지 않을 때 저장된 묶음과 기본 복사본으로 켜지고 커버가 보임, 들은 기록 유지. 폰에서도 확인했다(2026-11-13 성범 "바뀌었어요"): 초급 커버를 바꾼 시험 판을 올리고 앱을 껐다 켜니 설치 없이 바뀌었다. 그 뒤 원래 커버 판(202611131324)을 다시 올렸다. 비행기 모드에서도 앱이 켜지고 문제없다(같은 날 성범 확인). 앱을 끄지 않고 돌아왔을 때 다시 그리는 길만 확인 전이다.
- 아직 코드에 박혀 있는 것: 앨범 목록(이름, 소개, 색), 과정 목차, 쉐도잉 한국어 해설 글과 소리 목록. 이것까지 옮기면 새 앨범도 설치 없이 넣을 수 있다(하지 않음).
- 자른 쉐도잉 소리는 아직 R2에 올리지 않았다(성범이 자른 줄을 확인하기 전). 올릴 때는 `build_page.py` → `upload_r2.py` → `build_game.py` → `upload_game_r2.py` → `build_pwa.py` → `publish_data.py` 순서로 하면 소리와 시간표가 한 판으로 바뀐다.

## 4. 받기와 저장

- 음성은 Opus 24kbps(webm). 전체를 처음에 받지 않는다. 처음 듣는 화는 인터넷이 필요하다.
- 재생 중에는 다음 화 음성을 미리 받아 둔다(백그라운드 끊김 방지). 그 밖에 재생할 때 저절로 쌓아 두는 받기는 하지 않고, 오프라인용 받기는 앨범 화면의 **앨범 전체 받기 단추**로만 한다.
- 앨범 전체 받기(2026-11-10 실제 연결): 그 앨범의 소리를 R2에서 3개씩 동시에 받아 기기의 `audio-v1` 저장소(Cache Storage)에 넣는다. 다 받으면 화 번호를 저장해 단추를 숨기고 "Downloaded. This album plays without internet."을 띄운다. 실패하면 "Couldn't download…". Wi-Fi only가 켜져 있고 와이파이가 아니면 받지 않는다. 받는 도중 데이터로 바뀌어도 멈추고 "Wi-Fi only is on…"을 띄운다. 연결 종류는 앱에서 `@capacitor/network`(getStatus의 connectionType)로 묻고, 브라우저에서만 `navigator.connection`을 쓴다(2026-11-10 성범 제보: 안드로이드 WebView는 navigator.connection.type을 주지 않아 데이터에서도 받아졌다). 재생할 때 저장본이 있으면 쓴다(앱도 웹과 같은 방식).
- Storage used는 기기가 알려 주는 사용량, Delete downloads는 저장본과 받은 앨범 표시를 함께 지운다.
- 받은 음성은 폰 파일 탐색기에서 일반 음원으로 보이지 않게 앱 전용 저장 공간에만 둔다. 암호로 잠그지는 않는다.
- sw.js(웹): 건너뛰기용 구간 요청은 저장본에서 잘라 준다.

## 5. 들은 기록

- **이름표로 옮기기 (2026-11-13):** 화마다 이름표(`과정|화 번호`)를 두고 마지막에 쓴 이름표 목록을 `S.ids`로 저장한다. 내용이 새 판이 되어 순서가 달라지면 앱이 켤 때 기록을 이름표 기준으로 새 자리에 옮긴다. 그래서 화를 중간에 끼우거나 빼도 기록이 밀리지 않는다. 다만 과정 이름이나 화 번호 자체를 바꾸면 그 화의 기록은 이어지지 않는다.
- **고친 것 (2026-11-13):** 켤 때마다 첫 화(초급 1화)의 들은 기록이 지워지던 문제. 글자 크기를 맞추는 코드가 화를 고르기 전에 저장을 불렀다.
- 기록은 지금 폰 안에만 저장한다. 들은 기록은 앱 목록의 **자리 번호**로 저장되므로 새 트랙은 목록 뒤에 붙인다(코스 → 팟캐스트 → 심화·고급 → 쉐도잉 → Words 순으로 붙여 왔다). 앞에 끼우면 기록이 어긋난다. 목록을 바꿔야 하면 The Replay 합치기처럼 앱이 한 번 옮기게 한다([팟캐스트](side-a-podcasts.md)).
- 폰 저장소가 지워지면 기록은 사라진다. 첫 버전에서는 받아들인다.
- 나중에: 구글 로그인(Firebase Authentication)과 들은 기록(Firestore). Firebase는 `xxx.beom@gmail.com` 계정의 무료 Spark 요금제로 두고 카드 등록이 필요한 Blaze로 올리지 않는다. Supabase는 무료 프로젝트 한도 때문에 쓰지 않는다.

## 6. 백그라운드 재생

- 화면이 꺼지거나 다른 앱을 써도 재생이 이어지고, 잠금 화면에서 멈출 수 있어야 한다. 백그라운드 재생은 안드로이드 크롬과 갤럭시 기준이다.
- 2026-11-09 고친 것: 다음 화로 넘어갈 때 화면이 꺼진 안드로이드가 절전 때문에 인터넷을 막아 받기에 실패하고 재생이 조용히 거부됐다. 재생이 시작되면 다음 화를 미리 받아 두고, 재생 시작이 거부되면 음성이 준비되는 대로 다시 틀고, 음성 오류는 같은 위치에서 저장본이나 인터넷으로 네 번까지 다시 연결한다. 폰에서 실제로 고쳐졌는지와 화면을 끈 채 듣는 시험은 아직 확인 전이다.
- **이어폰을 빼면 멈춘다 (2026-11-11 성범 제보):** 유선 이어폰을 빼거나 블루투스 이어폰이 끊기면 스피커로 계속 나오던 것을 스포티파이처럼 멈추게 했다. `MainActivity`가 안드로이드의 `ACTION_AUDIO_BECOMING_NOISY` 알림을 받아 WebView에 `sidea-noisy` 이벤트를 보내고, `template.html`이 재생 중이면 일시정지한다. 다시 꽂아도 저절로 다시 틀지 않는다. 브라우저에서 이벤트로 멈추는 것은 확인했고, 폰에서 실제로 빼 보는 시험은 성범 확인 전이다.
- **PIP 작은 창 (2026-11-12 성범 요청):** 안드로이드 기본 PIP를 쓴다(권한 없음). `AndroidManifest.xml`의 `supportsPictureInPicture`, `MainActivity`가 창 비율 16:9와 단추 세 개(`res/drawable/ic_pip_*.xml`)를 정하고, 재생 중일 때만 홈으로 나갈 때 저절로 들어가게 한다(안드로이드 12 이상 `setAutoEnterEnabled`, 8~11은 `onUserLeaveHint`). 웹 코드는 재생/멈춤이 바뀔 때 `window.SideAPip.setPlaying`으로 알리고, 안드로이드는 창이 되거나 돌아올 때 `sidea-pip`, 단추를 누르면 `sidea-pip-act` 이벤트를 보낸다. `template.html`은 `body.in-pip`일 때 `#pip`만 보이고, 재생 화면 가사(`#script`)를 `#pipList`에 옮겨 지금 줄로 민다(`pipFill`, `pipLine`). 검토하고 안 쓴 방법: 웹 표준 Document PIP(안드로이드 미지원), 다른 앱 위에 그리는 떠 있는 창(권한 필요, 화면을 안드로이드 코드로 다시 그려야 함), 갤럭시 팝업 화면. 브라우저에서 창 화면과 단추 이벤트를 확인했고, 폰에 설치했다. 폰에서 창이 뜨는 것은 성범이 확인했다(첫 판 기준). 전체 가사 스크롤 판은 폰 확인 전이다.
- **앱 빌드에는 JDK 21:** PC 기본 Java는 17이라 `gradlew`가 멈춘다. `JAVA_HOME`을 `C:\Program Files\Android\Android Studio\jbr`로 두고 `side-a/android`에서 `./gradlew assembleRelease`.

## 7. 옛 코드 처리

| 항목 | 처리 |
|---|---|
| `src/domain/answer.ts`, `tests/answer.test.ts` 답 판정 | 쓰지 않는다. 삭제 시점은 개발 계획에서 정한다 |
| `src/domain/types.ts`, `scripts/validate-content.ts` | 빈칸 문제 형식이라 쓰지 않는다 |
| `content/courses.json` | 배경 상황 참고로만 쓴다 |
| 옛 시즌 1 Part 1 대본(`content/stories/season-1-part-1*.md`)과 지하철 시험판(`spikes/episode-01/script.md`) | 새 커리큘럼 이전 결과물. 시험판으로 남긴다 |
