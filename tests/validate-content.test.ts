import { describe, it, expect } from 'vitest';
import { validateContent } from '../scripts/validate-content';
import type { Sentence, Word } from '../src/domain/types';

const w: Word = { id: 'w1', word: 'borrow', meaning: '빌리다', level: 1, courseId: 'daily' };
const base: Sentence = {
  id: 's1', wordId: 'w1',
  before: 'Can I ', answer: 'borrow', after: ' your pen?',
  ko: '펜 좀 빌려도 될까요?', koHighlight: '빌려도', gloss: '빌리다',
  accepted: [], notes: { '*': '빌릴 때 쓰는 말이에요.' },
};
const s2: Sentence = { ...base, id: 's2', before: 'I ', answer: 'borrow', after: ' books often.', ko: '나는 책을 자주 빌려요.', koHighlight: '빌려요' };
const ok = (over: Partial<Sentence> = {}): Sentence[] => [{ ...base, ...over }, s2];

describe('validateContent', () => {
  it('정상 문장은 오류가 없다', () => expect(validateContent([w], ok())).toEqual([]));
  it('8단어가 넘는 초급 문장을 잡는다', () => {
    const errs = validateContent([w], ok({ after: ' your pen for a little while please?' }));
    expect(errs.some((e) => e.includes('단어'))).toBe(true);
  });
  it('koHighlight가 ko에 없으면 잡는다', () => {
    expect(validateContent([w], ok({ koHighlight: '없는말' })).some((e) => e.includes('koHighlight'))).toBe(true);
  });
  it('단어마다 문장이 2개 미만이면 잡는다', () => {
    expect(validateContent([w], [base]).some((e) => e.includes('2개'))).toBe(true);
  });
  it('notes에 "*"가 없으면 잡는다', () => {
    expect(validateContent([w], ok({ notes: {} })).some((e) => e.includes('"*"'))).toBe(true);
  });
  it('gonna, wanna, idk가 본문에 있으면 잡는다', () => {
    expect(validateContent([w], ok({ before: 'I am gonna ' })).some((e) => e.includes('gonna'))).toBe(true);
    expect(validateContent([w], ok({ alsoSay: "I'm gonna borrow it" }))).toEqual([]);
  });
  it('colour, favourite 같은 영국식 철자를 잡는다', () => {
    expect(validateContent([w], ok({ before: 'My favourite ' })).some((e) => e.includes('favourite'))).toBe(true);
  });
  it('accepted에 answer가 들어 있으면 잡는다', () => {
    expect(validateContent([w], ok({ accepted: ['borrow'] })).some((e) => e.includes('accepted'))).toBe(true);
  });
});
