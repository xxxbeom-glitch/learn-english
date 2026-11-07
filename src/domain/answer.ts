import type { Sentence } from './types';

export type AnswerResult = 'empty' | 'notEnglish' | 'correct' | 'accepted' | 'typo' | 'wrong';

const HANGUL = /[ᄀ-ᇿ㄰-㆏가-힯]/;

function normalize(text: string): string {
  return text.trim().toLowerCase().replace(/[’‘]/g, "'");
}

/** True when the edit distance between a and b is exactly 1. */
function isOneEditApart(a: string, b: string): boolean {
  if (a === b) return false;
  const [short, long] = a.length <= b.length ? [a, b] : [b, a];
  if (long.length - short.length > 1) return false;
  let i = 0;
  while (i < short.length && short[i] === long[i]) i++;
  if (short.length === long.length) return short.slice(i + 1) === long.slice(i + 1);
  return short.slice(i) === long.slice(i + 1);
}

export function checkAnswer(sentence: Sentence, input: string): AnswerResult {
  const value = normalize(input);
  if (value === '') return 'empty';
  if (HANGUL.test(value)) return 'notEnglish';
  const answer = normalize(sentence.answer);
  if (value === answer) return 'correct';
  if (sentence.accepted.some((a) => normalize(a) === value)) return 'accepted';
  if (answer.length >= 4 && isOneEditApart(answer, value)) return 'typo';
  return 'wrong';
}
