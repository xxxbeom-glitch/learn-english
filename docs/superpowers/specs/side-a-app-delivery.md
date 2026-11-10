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
- 웹: `build_pwa.py`가 `web/`을 만들고(설치 설정 manifest, 아이콘 Lucide headphones, sw.js), `web/`에서 `npx vercel deploy --prod --yes`.
- 앱: `build_pwa.py` 결과를 Capacitor로 감싸 APK를 만든다(자세한 단계는 개발 계획).

## 3. 소리 파일: Cloudflare R2 (2026-11-09 결정, 2026-11-10 옮김 완료)

- 앱이 쓰는 모든 소리(코스, 팟캐스트, 쉐도잉, Words, 효과음)는 R2에 올리고 앱은 R2 주소에서 받는다. 앱 안에는 소리가 없다(APK 74MB → 6MB). Firebase 저장소에는 소리를 두지 않는다.
- 통 `side-a-audio`, 공개 주소 `https://pub-54e325ce90af4f1bad3644fc22432096.r2.dev/audio/<파일 이름>.webm`. CORS는 모든 곳에서 GET/HEAD와 Range 머리글 허용. 계정은 `Psblove88@gmail.com's Account`이고, 같은 계정의 `tampin-media-prod` 통은 다른 앱 것이라 건드리지 않는다.
- `spikes/episode-01/upload_r2.py`가 화면이 쓰는 `app/*.webm`만 올리고, 같은 내용은 `r2-uploaded.json`의 내용 지문으로 건너뛴다. `build_pwa.py`는 소리 주소를 R2 주소 + `?v=지문`으로 바꿔 다시 만든 화는 새로 받게 한다.
- 올리는 규칙: 소리를 새로 만들거나 다시 만들면 같은 작업에서 R2에도 올린다. 앱이 받을 목록(화별 소리 주소)은 앱 안의 콘텐츠 목록에 적는다.
- 무료 범위는 한 달 저장 10GB, 올리기 100만 번, 읽기 1,000만 번, 내려받는 양 무료. 2026-11-09에 `tampin-media-prod`가 3.25GB를 써서 약 6.7GB가 남았다. 10GB를 넘기기 전에 성범에게 먼저 알린다.
- R2 주소를 아는 사람이 받는 것까지는 막지 않는다.

## 4. 받기와 저장

- 음성은 Opus 24kbps(webm). 전체를 처음에 받지 않는다. 처음 듣는 화는 인터넷이 필요하다.
- 재생 중에는 다음 화 음성을 미리 받아 둔다(백그라운드 끊김 방지). 그 밖에 재생할 때 저절로 쌓아 두는 받기는 하지 않고, 오프라인용 받기는 앨범 화면의 **앨범 전체 받기 단추**로만 한다.
- 앨범 전체 받기(2026-11-10 실제 연결): 그 앨범의 소리를 R2에서 3개씩 동시에 받아 기기의 `audio-v1` 저장소(Cache Storage)에 넣는다. 다 받으면 화 번호를 저장해 단추를 숨기고 "Downloaded. This album plays without internet."을 띄운다. 실패하면 "Couldn't download…". Wi-Fi only가 켜져 있고 와이파이가 아니면 받지 않는다. 받는 도중 데이터로 바뀌어도 멈추고 "Wi-Fi only is on…"을 띄운다. 연결 종류는 앱에서 `@capacitor/network`(getStatus의 connectionType)로 묻고, 브라우저에서만 `navigator.connection`을 쓴다(2026-11-10 성범 제보: 안드로이드 WebView는 navigator.connection.type을 주지 않아 데이터에서도 받아졌다). 재생할 때 저장본이 있으면 쓴다(앱도 웹과 같은 방식).
- Storage used는 기기가 알려 주는 사용량, Delete downloads는 저장본과 받은 앨범 표시를 함께 지운다.
- 받은 음성은 폰 파일 탐색기에서 일반 음원으로 보이지 않게 앱 전용 저장 공간에만 둔다. 암호로 잠그지는 않는다.
- sw.js(웹): 건너뛰기용 구간 요청은 저장본에서 잘라 준다.

## 5. 들은 기록

- 지금은 폰 안에만 저장한다. 들은 기록은 앱 목록의 **자리 번호**로 저장되므로 새 트랙은 목록 뒤에 붙인다(코스 → 팟캐스트 → 심화·고급 → 쉐도잉 → Words 순으로 붙여 왔다). 앞에 끼우면 기록이 어긋난다. 목록을 바꿔야 하면 The Replay 합치기처럼 앱이 한 번 옮기게 한다([팟캐스트](side-a-podcasts.md)).
- 폰 저장소가 지워지면 기록은 사라진다. 첫 버전에서는 받아들인다.
- 나중에: 구글 로그인(Firebase Authentication)과 들은 기록(Firestore). Firebase는 `xxx.beom@gmail.com` 계정의 무료 Spark 요금제로 두고 카드 등록이 필요한 Blaze로 올리지 않는다. Supabase는 무료 프로젝트 한도 때문에 쓰지 않는다.

## 6. 백그라운드 재생

- 화면이 꺼지거나 다른 앱을 써도 재생이 이어지고, 잠금 화면에서 멈출 수 있어야 한다. 백그라운드 재생은 안드로이드 크롬과 갤럭시 기준이다.
- 2026-11-09 고친 것: 다음 화로 넘어갈 때 화면이 꺼진 안드로이드가 절전 때문에 인터넷을 막아 받기에 실패하고 재생이 조용히 거부됐다. 재생이 시작되면 다음 화를 미리 받아 두고, 재생 시작이 거부되면 음성이 준비되는 대로 다시 틀고, 음성 오류는 같은 위치에서 저장본이나 인터넷으로 네 번까지 다시 연결한다. 폰에서 실제로 고쳐졌는지와 화면을 끈 채 듣는 시험은 아직 확인 전이다.

## 7. 옛 코드 처리

| 항목 | 처리 |
|---|---|
| `src/domain/answer.ts`, `tests/answer.test.ts` 답 판정 | 쓰지 않는다. 삭제 시점은 개발 계획에서 정한다 |
| `src/domain/types.ts`, `scripts/validate-content.ts` | 빈칸 문제 형식이라 쓰지 않는다 |
| `content/courses.json` | 배경 상황 참고로만 쓴다 |
| 옛 시즌 1 Part 1 대본(`content/stories/season-1-part-1*.md`)과 지하철 시험판(`spikes/episode-01/script.md`) | 새 커리큘럼 이전 결과물. 시험판으로 남긴다 |
