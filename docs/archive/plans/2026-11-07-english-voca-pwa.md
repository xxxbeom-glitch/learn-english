# 개인 영어 어휘 학습 PWA 개발 계획

> 2026-11-10 보관: 어휘 PWA는 개발이 멈춘 상태다. 다시 시작하면 시안 확정 뒤 계획을 새로 쓴다.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 갤럭시 폰 크롬에 설치해서, 한글 뜻을 보고 영어 문장의 빈칸을 직접 쓰며 생활회화 어휘를 익히는 1인용 앱을 만든다.

**Architecture:** 학습 규칙은 화면과 분리한 순수 함수로 만들고, 기록은 폰의 IndexedDB에 저장한다. 문장은 미리 검사한 JSON 파일로 앱에 포함한다. 서버는 AI 질문을 Claude API로 전달하는 함수 하나만 둔다.

**Tech Stack:** TypeScript, React, Vite, React Router, vite-plugin-pwa, Dexie, lucide-react, Vitest, Testing Library, fake-indexeddb, Playwright, Vercel Functions, `@anthropic-ai/sdk`

**Spec:** [개인 영어 학습 웹앱 기획서](https://claude.ai/artifact/QtTP9oy2WzCtictebBS2M3)
**디자인 레퍼런스:** `docs/archive/design/2026-11-07-design-references.md`

## Global Constraints

- 사용자는 한 명이고 대상 환경은 안드로이드 갤럭시 폰의 크롬이다. 로그인과 기기 동기화는 없다.
- 푸시 알림, 뱃지, 연속 학습 기록, 밀린 개수 강조는 어떤 화면에도 넣지 않는다.
- 빈칸은 항상 직접 입력한다. 보기 선택 문제를 만들지 않는다.
- 인터넷이 없어도 AI 질문을 뺀 모든 학습이 동작한다.
- 복습 간격은 5분, 1일, 3일, 7일, 14일, 30일이다.
- 하루 목표의 약 30%는 복습이 많아도 새 단어로 남긴다.
- 문장은 평범한 구어체 한 가지와 미국식 철자만 쓴다. 말해보카의 문장, 문구, 캐릭터, 외형을 가져오지 않는다.
- UI 아이콘은 `lucide-react`만 쓴다. 새 화면의 시각 디자인은 Taste Skill로 만들고, 완성 후 Impeccable은 검수만 한다.
- Anthropic API 키와 앱 암호는 서버 환경변수에만 둔다. 코드, 저장소, 브라우저 번들에 넣지 않는다.
- 와이어프레임과 기획서가 다르면 기획서를 따른다. A1 학습 목적, 표현과 문법 카드, 사전, 학습 시간 통계는 만들지 않는다.

## Review Focus

1. 삼성 키보드가 한글 상태일 때 입력하면 오답이 아니라 `영어로 써주세요` 안내가 나오고 기록은 바뀌지 않는다. (Task 2, 7)
2. 한글 조합 중 확인 키를 눌러도 답이 제출되지 않고, 자동 대문자와 맞춤법 교정이 답을 바꾸지 않는다. (Task 7)
3. 2주를 쉬고 돌아와도 하루 목표 개수만 보이고, 새 단어가 남아 있으면 약 30%가 유지된다. (Task 4)
4. 손상된 백업 파일을 불러오면 기존 기록이 한 글자도 바뀌지 않는다. (Task 5)
5. 비행기 모드에서 앱을 다시 열어도 학습이 되고, AI 질문만 안내 문구와 함께 멈춘다. (Task 9, 12)

---

## File Structure

```text
api/ask.ts                     AI 질문 서버 함수
content/courses.json           코스 목록
content/words/<courseId>.json  코스별 단어와 문장
scripts/validate-content.ts    문장 규칙 자동 검사
src/domain/types.ts            공통 타입
src/domain/answer.ts           답 판정
src/domain/srs.ts              복습 일정
src/domain/session.ts          오늘의 학습 구성과 진행 순서
src/domain/placement.ts        레벨 테스트
src/data/db.ts                 Dexie 저장소
src/data/repo.ts               기록 읽기와 쓰기
src/data/backup.ts             백업과 복원
src/data/content.ts            콘텐츠 불러오기
src/platform/speech.ts         폰 영어 음성 읽기
src/platform/ask.ts            AI 질문 요청
src/screens/onboarding/*       A2~A5
src/screens/home/*             B1, B2
src/screens/learn/*            C1~C9
src/screens/library/*          D1~D6
src/screens/settings/*         E1, E2
e2e/*.spec.ts                  실제 브라우저 흐름 시험
```

---

### Task 1: 프로젝트와 콘텐츠 형식

**Files:**
- Create: `package.json`, `vite.config.ts`, `tsconfig.json`, `src/domain/types.ts`, `scripts/validate-content.ts`, `content/courses.json`
- Test: `tests/validate-content.test.ts`

**Interfaces:**
- Produces:

```ts
export type Course = { id: string; order: number; title: string; summary: string };
export type Word = { id: string; word: string; meaning: string; level: 1|2|3|4|5; courseId: string };
export type Sentence = {
  id: string; wordId: string;
  before: string; answer: string; after: string;  // en = before + answer + after
  ko: string; koHighlight: string; gloss: string;
  accepted: string[];                             // 맞는 말이지만 이번 정답은 아닌 답
  notes: Record<string, string>;                  // 답별 설명. 기본 설명은 "*" 키
  alsoSay?: string;                               // 이렇게도 써요
};
export function validateContent(words: Word[], sentences: Sentence[]): string[]; // 오류 문구 목록
```

- [ ] **Step 1:** `git init` 후 Vite React TypeScript 프로젝트를 만들고 위 의존성을 설치한다. `.env*`를 `.gitignore`에 넣는다.
- [ ] **Step 2: 실패하는 시험을 쓴다.** `tests/validate-content.test.ts`

```ts
it('정상 문장은 오류가 없다', () => expect(validateContent([w], [s])).toEqual([]));
it('8단어가 넘는 초급 문장을 잡는다', ...);        // level 1~2는 3~7단어
it('koHighlight가 ko에 없으면 잡는다', ...);
it('단어마다 문장이 2개 미만이면 잡는다', ...);    // 복습에서 다른 예문을 쓰기 위함
it('notes에 "*"가 없으면 잡는다', ...);
it('gonna, wanna, idk가 본문에 있으면 잡는다', ...); // alsoSay에는 허용
it('colour, favourite 같은 영국식 철자를 잡는다', ...);
it('accepted에 answer가 들어 있으면 잡는다', ...);
```

- [ ] **Step 3:** `npx vitest run tests/validate-content.test.ts`가 함수 없음으로 실패하는지 확인한다.
- [ ] **Step 4:** 타입과 `validateContent`를 구현한다. `content/courses.json`에 기획서의 8개 코스를 순서대로 넣는다.
- [ ] **Step 5:** 같은 시험이 통과하는지 확인한다.
- [ ] **Step 6:** 커밋한다. `feat: 프로젝트와 콘텐츠 형식 추가`

### Task 2: 답 판정

**Files:**
- Create: `src/domain/answer.ts`
- Test: `tests/answer.test.ts`

**Interfaces:**
- Consumes: `Sentence`
- Produces:

```ts
export type AnswerResult = 'empty' | 'notEnglish' | 'correct' | 'accepted' | 'typo' | 'wrong';
export function checkAnswer(sentence: Sentence, input: string): AnswerResult;
```

- [ ] **Step 1: 실패하는 시험을 쓴다.** `answer`가 `get`, `accepted`가 `['have']`인 문장 기준이다.

```ts
expect(checkAnswer(s, '  Get ')).toBe('correct');
expect(checkAnswer(s, 'have')).toBe('accepted');
expect(checkAnswer(s, 'bring')).toBe('wrong');
expect(checkAnswer(s, '')).toBe('empty');
expect(checkAnswer(s, '겟')).toBe('notEnglish');
expect(checkAnswer(dont, 'don’t')).toBe('correct');   // 굽은 따옴표
expect(checkAnswer(coffee, 'cofee')).toBe('typo');    // 4글자 이상, 편집 거리 1
expect(checkAnswer(s, 'got')).toBe('wrong');          // 3글자 이하는 철자 봐주기 없음
```

- [ ] **Step 2:** 시험이 실패하는지 확인한다.
- [ ] **Step 3:** 앞뒤 공백 제거, 소문자화, 굽은 따옴표 치환 후 판정한다. 한글이 하나라도 있으면 `notEnglish`다.
- [ ] **Step 4:** 시험이 통과하는지 확인한다.
- [ ] **Step 5:** 커밋한다. `feat: 답 판정 추가`

### Task 3: 복습 일정

**Files:**
- Create: `src/domain/srs.ts`
- Test: `tests/srs.test.ts`

**Interfaces:**
- Produces:

```ts
export type Outcome = 'correct' | 'correctWithHint' | 'wrong' | 'revealed';
export type WordState = { wordId: string; stage: 0|1|2|3|4|5; dueAt: number; lastAt: number;
  correctCount: number; wrongCount: number };
export const STAGE_DAYS = [1, 3, 7, 14, 30] as const;
export const RETRY_MS = 5 * 60 * 1000;
export function applyOutcome(prev: WordState | undefined, wordId: string, outcome: Outcome, now: number): WordState;
```

- [ ] **Step 1: 실패하는 시험을 쓴다.**

```ts
// 처음 본 단어는 결과와 상관없이 5분 뒤
expect(applyOutcome(undefined, 'w', 'correct', T)).toMatchObject({ stage: 0, dueAt: T + RETRY_MS });
// 5분 뒤 맞히면 1일
expect(applyOutcome(s0, 'w', 'correct', T)).toMatchObject({ stage: 1, dueAt: T + DAY });
// 단계별 3일, 7일, 14일, 30일
expect(applyOutcome(s4, 'w', 'correct', T)).toMatchObject({ stage: 5, dueAt: T + 30 * DAY });
// 마지막 단계는 30일 유지
expect(applyOutcome(s5, 'w', 'correct', T)).toMatchObject({ stage: 5, dueAt: T + 30 * DAY });
// 힌트 정답은 간격을 늘리지 않음
expect(applyOutcome(s2, 'w', 'correctWithHint', T)).toMatchObject({ stage: 2, dueAt: T + 3 * DAY });
// 틀리거나 정답 보기는 5분 뒤, 한 단계 내림
expect(applyOutcome(s3, 'w', 'wrong', T)).toMatchObject({ stage: 2, dueAt: T + RETRY_MS });
expect(applyOutcome(s0, 'w', 'revealed', T)).toMatchObject({ stage: 0, dueAt: T + RETRY_MS });
```

- [ ] **Step 2:** 시험이 실패하는지 확인한다.
- [ ] **Step 3:** `applyOutcome`을 구현한다. `stage`가 `n`인 단어의 힌트 정답 간격은 `STAGE_DAYS[max(n-1, 0)]`일이다. 횟수도 함께 갱신한다.
- [ ] **Step 4:** 시험이 통과하는지 확인한다.
- [ ] **Step 5:** 커밋한다. `feat: 복습 일정 추가`

### Task 4: 오늘의 학습 구성

**Files:**
- Create: `src/domain/session.ts`
- Test: `tests/session.test.ts`

**Interfaces:**
- Consumes: `Word`, `Course`, `WordState`
- Produces:

```ts
export type Plan = { reviewIds: string[]; newIds: string[] };
export function planToday(input: { words: Word[]; courses: Course[]; states: WordState[];
  dailyGoal: number; startLevel: number; now: number }): Plan;
export type Queue = { items: { wordId: string; readyAt: number }[] };
export function nextItem(queue: Queue, now: number): string | null;  // 준비된 항목이 없으면 null
export function requeue(queue: Queue, wordId: string, readyAt: number): Queue;
```

- [ ] **Step 1: 실패하는 시험을 쓴다.**

```ts
// 목표 10, 밀린 복습 100개, 새 단어 충분: 복습 7 + 새 단어 3
// 목표 10, 복습 2개: 복습 2 + 새 단어 8
// 새 단어가 없으면 복습으로 목표를 채움
// 복습은 오래된 dueAt부터, 새 단어는 코스 순서 다음 level 순서
// startLevel 3이면 level 1, 2 단어는 새 단어로 뽑지 않음
// nextItem: readyAt이 지난 항목만 반환하고, 5분 대기 항목만 남으면 null
```

- [ ] **Step 2:** 시험이 실패하는지 확인한다.
- [ ] **Step 3:** 복습 상한은 `dailyGoal - ceil(dailyGoal * 0.3)`으로 계산한 뒤 새 단어가 모자라면 남는 칸을 복습에 돌린다. 세션 끝에 5분 대기 항목만 남으면 세션을 마치고, 그 단어는 `dueAt`에 따라 다음 학습에 나온다.
- [ ] **Step 4:** 시험이 통과하는지 확인한다.
- [ ] **Step 5:** 커밋한다. `feat: 오늘의 학습 구성 추가`

### Task 5: 저장소와 백업

**Files:**
- Create: `src/data/db.ts`, `src/data/repo.ts`, `src/data/backup.ts`
- Test: `tests/repo.test.ts`, `tests/backup.test.ts`

**Interfaces:**
- Consumes: `WordState`
- Produces:

```ts
export type Attempt = { id?: number; wordId: string; sentenceId: string; input: string;
  usedHint: boolean; result: AnswerResult | 'revealed'; at: number };
export type Settings = { dailyGoal: number; startLevel: number; onboarded: boolean; passcode?: string };
export type Marks = { sentenceId: string; saved: boolean; flagged: boolean };
export function recordAttempt(a: Attempt, next: WordState): Promise<void>;  // 한 트랜잭션
export function getSettings(): Promise<Settings>;
export function saveSettings(p: Partial<Settings>): Promise<void>;
export function setMark(sentenceId: string, p: Partial<Omit<Marks, 'sentenceId'>>): Promise<void>;
export function exportBackup(): Promise<string>;                // version 1 JSON, passcode 제외
export function importBackup(json: string): Promise<{ ok: true } | { ok: false; reason: string }>;
```

- [ ] **Step 1: 실패하는 시험을 쓴다.** `fake-indexeddb` 기준이다.

```ts
// recordAttempt 뒤 답안 기록과 단어 기록이 같이 저장된다
// exportBackup -> 빈 DB에 importBackup -> 같은 데이터, onboarded true
// exportBackup 결과에 passcode가 없다
// 손상된 JSON, version 2, 필드 누락 파일: ok false이고 기존 기록 그대로
```

- [ ] **Step 2:** 시험이 실패하는지 확인한다.
- [ ] **Step 3:** Dexie 테이블 `states`, `attempts`, `marks`, `settings`를 구현한다. 복원은 검사를 마친 뒤 한 트랜잭션에서 교체한다. 앱 시작 때 `navigator.storage.persist()`를 요청한다.
- [ ] **Step 4:** 시험이 통과하는지 확인한다.
- [ ] **Step 5:** 커밋한다. `feat: 저장소와 백업 추가`

### Task 6: 첫 콘텐츠

**Files:**
- Create: `content/words/greetings.json`, `content/words/daily.json`, `content/words/cafe.json`, `src/data/content.ts`
- Test: `tests/content.test.ts`

**Interfaces:**
- Consumes: `validateContent`
- Produces: `loadContent(): { courses: Course[]; words: Word[]; sentences: Sentence[] }`

- [ ] **Step 1: 실패하는 시험을 쓴다.** 전체 콘텐츠의 `validateContent` 결과가 빈 배열이고, 코스 1~3에 단어가 각각 30개 이상이며, level 1~5가 모두 있는지 확인한다.
- [ ] **Step 2:** 시험이 실패하는지 확인한다.
- [ ] **Step 3:** 코스 1~3의 단어 90개와 단어당 문장 2개를 새로 쓴다. 기획서의 `문장 기준`을 따르고 책이나 다른 앱의 문장을 베끼지 않는다.
- [ ] **Step 4:** 별도 리뷰어가 문장 전체를 읽고 어색한 표현, 틀린 해석, 답이 둘 이상인데 `accepted`에 없는 경우를 고친다.
- [ ] **Step 5:** 시험이 통과하는지 확인한다.
- [ ] **Step 6:** 커밋한다. `feat: 코스 1~3 콘텐츠 추가`

### Task 7: 학습 화면

**Files:**
- Create: `src/screens/learn/LearnSession.tsx`, `QuestionCard.tsx`, `ResultPanel.tsx`, `WordInfo.tsx`, `SessionDone.tsx`
- Test: `tests/learn.test.tsx`, `e2e/learn.spec.ts`

**Interfaces:**
- Consumes: `checkAnswer`, `applyOutcome`, `planToday`, `nextItem`, `requeue`, `recordAttempt`, `setMark`, `loadContent`
- Produces: `<LearnSession plan={Plan} />`, 라우트 `/learn`

복습 때는 그 단어의 문장 중 가장 오래전에 낸 문장을 고른다. `이상해요`로 표시한 문장은 고르지 않고, 단어의 문장이 모두 표시되면 그 단어를 오늘 계획에서 뺀다.

- [ ] **Step 1: 실패하는 시험을 쓴다.** 화면 동작을 시험한다.

```ts
// 입력에 autocapitalize off, autocorrect off, spellcheck false, enterKeyHint done
// isComposing 중 Enter는 제출하지 않는다
// 'accepted': 안내가 나오고 입력이 비며 기록은 안 바뀐다
// 'typo': 철자 확인 안내 후 다시 입력, 기록은 안 바뀐다
// 'notEnglish': 영어로 써주세요 안내, 기록은 안 바뀐다
// 힌트 1회: 첫 글자가 입력되고 버튼이 정답 보기로 바뀐다
// 힌트 뒤 정답: 'correctWithHint'로 기록된다
// 정답 보기: 'revealed'로 기록되고 5분 뒤 다시 낸다
// 오답: 내가 쓴 답, notes[input] 또는 notes['*'], 5분 뒤 복습 문구가 보인다
// 정답: 다음 복습 시점, 예문 저장, 다른 예문, 단어 정보, 이상해요가 보인다
```

- [ ] **Step 2:** 시험이 실패하는지 확인한다.
- [ ] **Step 3:** 와이어프레임 C1~C7, C9 구조로 구현한다. 입력칸은 문장 속 빈칸 자리에 두고, 힌트는 키보드 바로 위에 둔다. 키보드가 올라와도 문제 문장과 입력칸이 보이도록 `visualViewport` 높이에 맞춘다. 오답 화면은 내가 쓴 답과 정답을 같은 글자 크기로 위아래에 놓고 빨강을 쓰지 않는다. 다음 복습 시점은 문장 옆 작은 라벨로 보여준다. 시각 디자인은 기본값으로 두고 Task 13에서 입힌다.
- [ ] **Step 4:** 시험과 `npx playwright test e2e/learn.spec.ts`가 Galaxy 크기 모바일 화면에서 통과하는지 확인한다.
- [ ] **Step 5:** 커밋한다. `feat: 학습 화면 추가`

### Task 8: 문장 듣기

**Files:**
- Create: `src/platform/speech.ts`
- Modify: `src/screens/learn/ResultPanel.tsx`
- Test: `tests/speech.test.ts`

**Interfaces:**
- Produces:

```ts
export function pickEnglishVoice(voices: SpeechSynthesisVoice[]): SpeechSynthesisVoice | null;
export function loadVoices(timeoutMs?: number): Promise<SpeechSynthesisVoice[]>; // 기본 1500ms
export function speak(text: string): Promise<boolean>; // 음성이 없으면 false
```

- [ ] **Step 1: 실패하는 시험을 쓴다.** `en-US`를 `en-GB`보다 먼저 고르고, 영어 음성이 없으면 `null`이며, 그때 듣기 버튼이 보이지 않는다. 문제를 푸는 동안에는 `speak`가 호출되지 않고 정답 때 한 번 호출된다.
- [ ] **Step 2:** 시험이 실패하는지 확인한다.
- [ ] **Step 3:** 구현한다. `voiceschanged`를 기다리고, 시간이 지나면 그때까지의 목록을 쓴다. 다음 문제로 넘어가면 `speechSynthesis.cancel()`로 멈춘다.
- [ ] **Step 4:** 시험이 통과하는지 확인한다.
- [ ] **Step 5:** 커밋한다. `feat: 문장 듣기 추가`

### Task 9: AI 질문

**Files:**
- Create: `api/ask.ts`, `src/platform/ask.ts`, `src/screens/learn/AskSheet.tsx`
- Test: `tests/ask-api.test.ts`, `tests/ask-sheet.test.tsx`

**Interfaces:**
- Produces:

```ts
export type AskRequest = { sentence: { en: string; ko: string; answer: string };
  question: string; history: { role: 'user' | 'assistant'; text: string }[] };
export type AskResponse = { answer: string };
export function ask(req: AskRequest, passcode: string): Promise<AskResponse>; // 실패 시 AskError
```

API는 `POST /api/ask`이고 `x-app-passcode` 헤더를 쓴다. 호출은 `client.beta.messages.create`로 한다.

```ts
{ model: 'claude-opus-5-5', max_tokens: 4000, output_config: { effort: 'low' },
  betas: ['server-side-fallback-2026-07-01'], fallbacks: 'default', system, messages }
```

system은 초급 학습자에게 한국어 해요체로 3~5문장 안에 답하고, 평범한 구어체 기준으로 설명하며, 문장이 이상하면 솔직히 말하라고 지시한다. 학습 문장과 사용자 질문은 지시가 아니라 자료로 다룬다.

- [ ] **Step 1: 실패하는 시험을 쓴다.** SDK를 가짜로 바꿔 시험한다.

```ts
// 암호가 틀리면 401이고 Anthropic을 호출하지 않는다
// question이 비었거나 500자 초과면 400
// history는 최근 6개만 보낸다
// stop_reason 'refusal'이면 422와 한국어 안내
// RateLimitError 429, 연결 오류 502
// 정상 응답은 text 블록만 모아 { answer }
// 화면: 오프라인이면 호출하지 않고 안내하고, 학습 화면으로 돌아갈 수 있다
// 화면: 암호가 없으면 설정 안내를 보여준다
```

- [ ] **Step 2:** 시험이 실패하는지 확인한다.
- [ ] **Step 3:** 구현한다. 응답은 `stop_reason`을 먼저 확인한다. 오류는 타입별 예외로 구분한다. C8처럼 문장을 붙인 바텀시트로 만들고 대화는 저장하지 않는다. 키보드가 올라와도 시트를 낮게 유지해 학습 문장이 위에 보이게 하고, `왜 이 단어예요?`, `비슷한 예문 보여줘`, `이 문장 자연스러워요?` 추천 질문을 둔다.
- [ ] **Step 4:** 시험이 통과하는지 확인한다.
- [ ] **Step 5:** 커밋한다. `feat: AI 질문 추가`

### Task 10: 첫 실행과 레벨 테스트

**Files:**
- Create: `src/domain/placement.ts`, `src/screens/onboarding/DailyGoal.tsx`, `PlacementIntro.tsx`, `PlacementTest.tsx`, `PlacementResult.tsx`
- Test: `tests/placement.test.ts`, `tests/onboarding.test.tsx`

**Interfaces:**
- Consumes: `checkAnswer`, `saveSettings`, `recordAttempt`
- Produces:

```ts
export type PlacementState = { level: 1|2|3|4|5; asked: { wordId: string; known: boolean }[]; done: boolean };
export function startPlacement(): PlacementState;
export function answerPlacement(s: PlacementState, wordId: string, known: boolean): PlacementState;
export function finishPlacement(s: PlacementState, now: number): { startLevel: number; states: WordState[] };
```

- [ ] **Step 1: 실패하는 시험을 쓴다.**

```ts
// 수준마다 3문제, 최대 15문제
// 한 수준에서 2개 이상 맞히면 다음 수준으로, 2개 이상 놓치면 종료
// startLevel은 2개 이상 맞힌 마지막 수준 + 1, 최대 5. 아무 수준도 통과 못 하면 1
// 맞힌 단어는 stage 3, dueAt now + 7일
// 통과한 수준에서 놓친 단어는 stage 0, dueAt now
// 모르겠어요는 known false이고 안내 없이 다음 문제로 간다
// onboarded true면 /로 가고 첫 실행 화면을 다시 보여주지 않는다
```

- [ ] **Step 2:** 시험이 실패하는지 확인한다.
- [ ] **Step 3:** A2~A5를 구현한다. 하루 목표 기본값은 10개이고 5, 10, 15개 중 고른다. 결과 화면은 점수 없이 시작 위치만 말한다.
- [ ] **Step 4:** 시험이 통과하는지 확인한다.
- [ ] **Step 5:** 커밋한다. `feat: 첫 실행과 레벨 테스트 추가`

### Task 11: 홈, 복습 자료, 설정

**Files:**
- Create: `src/screens/home/Home.tsx`, `TodaySheet.tsx`, `src/screens/library/*`, `src/screens/settings/Stats.tsx`, `Settings.tsx`
- Test: `tests/home.test.tsx`, `tests/library.test.tsx`, `tests/settings.test.tsx`

**Interfaces:**
- Consumes: `planToday`, `exportBackup`, `importBackup`, `saveSettings`, `Marks`

- [ ] **Step 1: 실패하는 시험을 쓴다.**

```ts
// 2주 쉰 기록에서 홈에 밀린 개수가 표시되지 않고 오늘 할 개수만 보인다
// B2에 코스 이름, 새 단어 수, 복습 단어 수가 보인다
// D3는 최근에 잊은 단어, 자주 잊는 단어, 저장한 예문으로 나뉜다
// D4 가리기는 목록 전체의 뜻과 철자를 각각 한 번에 숨기고, 항목을 누르면 그 항목만 보인다
// D5는 틀린 답안을 단어별로 묶는다
// D6는 5분, 1일, 3일, 7일, 14일, 30일을 설명한다
// E1은 배운 단어 수와 익힌 단어 수만 보이고 연속 기록이 없다
// E2에서 하루 목표 변경, 레벨 테스트 다시 보기, 암호 입력, 백업, 복원이 된다
// 복원 실패는 사유를 보여주고 기록을 유지한다
```

- [ ] **Step 2:** 시험이 실패하는지 확인한다.
- [ ] **Step 3:** B1, B2, D1~D6, E1, E2를 구현한다. B2는 레벨 대신 현재 코스 이름을 보여준다.
- [ ] **Step 4:** 시험이 통과하는지 확인한다.
- [ ] **Step 5:** 커밋한다. `feat: 홈과 복습 자료, 설정 추가`

### Task 12: 설치와 배포

**Files:**
- Modify: `vite.config.ts`
- Create: `public/icons/*`, `vercel.json`, `e2e/offline.spec.ts`, `README.md`

- [ ] **Step 1: 실패하는 시험을 쓴다.** `e2e/offline.spec.ts`에서 빌드본을 한 번 연 뒤 오프라인으로 새로고침하고, 한 문제를 풀어 기록이 남는지 확인한다.
- [ ] **Step 2:** 시험이 실패하는지 확인한다.
- [ ] **Step 3:** `vite-plugin-pwa`로 앱 설명 파일과 오프라인 캐시를 설정한다. `/api/*`는 캐시하지 않는다. 사용자가 켜지 않는 한 어떤 알림 권한도 요청하지 않는다.
- [ ] **Step 4:** 시험과 `npm run build`가 통과하는지 확인한다.
- [ ] **Step 5:** 커밋한 뒤, 사용자 확인을 받고 Vercel에 배포한다. 사용자가 `ANTHROPIC_API_KEY`와 `APP_PASSCODE`를 직접 넣는다.
- [ ] **Step 6:** 실제 갤럭시에서 설치, 키보드, 영어 음성, 비행기 모드, AI 질문을 확인한다. 결과를 `README.md`에 적는다.

### Task 13: 시각 디자인과 검수

**Files:**
- Modify: `src/styles/*`, `src/screens/**/*`
- Create: `DESIGN.md`

- [ ] **Step 1:** 사용자가 `docs/archive/design/2026-11-07-design-references.md`의 시각 방향을 고른다.
- [ ] **Step 2:** Taste Skill로 색, 글꼴, 간격 토큰을 정하고 C1, C4, B1 시안을 먼저 보여준다.
- [ ] **Step 3:** 사용자 승인 뒤 전체 화면에 적용한다. 동작 시험은 그대로 통과해야 한다.
- [ ] **Step 4:** 피그마에서 A1, 표현과 문법 카드, 사전을 지우고 B2 표시와 듣기 버튼을 맞춘다.
- [ ] **Step 5:** Impeccable로 검수만 하고 디자인 방향은 바꾸지 않는다.
- [ ] **Step 6:** `npm test`, `npx playwright test`, `npm run build`가 통과하면 커밋한다. `feat: 시각 디자인 적용`
