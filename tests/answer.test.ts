import { describe, expect, it } from 'vitest';
import { checkAnswer } from '../src/domain/answer';
import type { Sentence } from '../src/domain/types';

const make = (answer: string, accepted: string[] = []): Sentence => ({
  id: 's',
  wordId: 'w',
  before: '',
  answer,
  after: '',
  ko: '',
  koHighlight: '',
  gloss: '',
  accepted,
  notes: {},
});

const s = make('get', ['have']);
const dont = make('don’t');
const coffee = make('coffee');

describe('checkAnswer', () => {
  it('correct, trimmed and case-insensitive', () => {
    expect(checkAnswer(s, '  Get ')).toBe('correct');
  });
  it('accepted', () => {
    expect(checkAnswer(s, 'have')).toBe('accepted');
    expect(checkAnswer(s, ' HAVE ')).toBe('accepted');
  });
  it('wrong', () => {
    expect(checkAnswer(s, 'bring')).toBe('wrong');
  });
  it('empty', () => {
    expect(checkAnswer(s, '')).toBe('empty');
    expect(checkAnswer(s, '   ')).toBe('empty');
  });
  it('notEnglish', () => {
    expect(checkAnswer(s, '겟')).toBe('notEnglish');
    expect(checkAnswer(s, 'get 겟')).toBe('notEnglish');
  });
  it('curly quotes', () => {
    expect(checkAnswer(dont, 'don’t')).toBe('correct');
    expect(checkAnswer(dont, "don't")).toBe('correct');
    expect(checkAnswer(make("don't"), 'don’t')).toBe('correct');
    expect(checkAnswer(make('x', ['don’t']), "don't")).toBe('accepted');
  });
  it('typo', () => {
    expect(checkAnswer(coffee, 'cofee')).toBe('typo');
    expect(checkAnswer(coffee, 'coffees')).toBe('typo');
    expect(checkAnswer(coffee, 'coffxe')).toBe('typo');
    expect(checkAnswer(coffee, 'cofe')).toBe('wrong');
  });
  it('no typo leniency for 3 letters or fewer', () => {
    expect(checkAnswer(s, 'got')).toBe('wrong');
  });
  it('typo compares against answer only', () => {
    const t = make('bring', ['coffee']);
    expect(checkAnswer(t, 'cofee')).toBe('wrong');
  });
});
