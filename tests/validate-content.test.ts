import { describe, it, expect } from 'vitest';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { validateContent, validateContentDir } from '../scripts/validate-content';
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
  describe('길이 규칙: level 1~2는 3~7단어', () => {
    const withWords = (n: number) => ok({ before: 'w '.repeat(n - 1), after: '' });
    const lengthErr = (errs: string[]) => errs.filter((e) => e.includes('3~7단어'));
    it.each([3, 7])('%i단어는 통과한다', (n) => expect(lengthErr(validateContent([w], withWords(n)))).toEqual([]));
    it.each([2, 8])('%i단어는 길이 오류로 잡는다', (n) => expect(lengthErr(validateContent([w], withWords(n)))).toHaveLength(1));
    it('level 3은 길이 규칙에서 빠진다', () => {
      const w3: Word = { ...w, level: 3 };
      expect(validateContent([w3], withWords(12))).toEqual([]);
      expect(validateContent([w3], withWords(2))).toEqual([]);
    });
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

describe('validateContentDir', () => {
  const write = (dir: string, rel: string, data: unknown) => {
    mkdirSync(join(dir, rel, '..'), { recursive: true });
    writeFileSync(join(dir, rel), JSON.stringify(data));
  };
  const courses = [{ id: 'daily', order: 1, title: '나와 일상', summary: 'x' }];
  const run = (fn: (dir: string) => void) => {
    const dir = mkdtempSync(join(tmpdir(), 'content-'));
    try {
      fn(dir);
      return validateContentDir(dir);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  };

  it('content/words/<코스>.json의 잘못된 문장을 보고한다', () => {
    const errs = run((dir) => {
      write(dir, 'courses.json', courses);
      write(dir, 'words/x.json', { words: [w], sentences: [{ ...base, koHighlight: '없는말' }, s2] });
    });
    expect(errs.some((e) => e.includes('koHighlight'))).toBe(true);
  });
  it('words 폴더가 없으면 오류가 아니다', () => {
    expect(run((dir) => write(dir, 'courses.json', courses))).toEqual([]);
  });
  it('words 밖의 json은 읽지 않는다', () => {
    const errs = run((dir) => {
      write(dir, 'courses.json', courses);
      write(dir, 'stray.json', { words: [w], sentences: [] });
    });
    expect(errs).toEqual([]);
  });
});
