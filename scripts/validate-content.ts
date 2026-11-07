import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import type { Course, Sentence, Word } from '../src/domain/types';

const INFORMAL = ['gonna', 'wanna', 'idk', 'gotta', 'kinda'];
const BRITISH = [
  'colour', 'favourite', 'flavour', 'neighbour', 'behaviour', 'honour', 'humour', 'labour',
  'centre', 'theatre', 'metre', 'litre', 'organise', 'realise', 'recognise', 'apologise',
  'grey', 'programme', 'cheque', 'travelling', 'cancelled', 'jewellery',
];

const wordCount = (text: string) => text.trim().split(/\s+/).filter(Boolean).length;
const hasWord = (text: string, list: string[]) => {
  const lower = text.toLowerCase();
  return list.filter((w) => new RegExp(`(^|[^a-z])${w}($|[^a-z])`).test(lower));
};

export function validateContent(words: Word[], sentences: Sentence[]): string[] {
  const errors: string[] = [];
  const wordsById = new Map(words.map((w) => [w.id, w]));
  const counts = new Map<string, number>();

  for (const s of sentences) {
    const en = s.before + s.answer + s.after;
    const tag = `문장 ${s.id}`;
    const word = wordsById.get(s.wordId);
    if (!word) errors.push(`${tag}: wordId ${s.wordId} 단어가 없어요`);
    else {
      counts.set(word.id, (counts.get(word.id) ?? 0) + 1);
      const n = wordCount(en);
      if (word.level <= 2 && (n < 3 || n > 7)) errors.push(`${tag}: 레벨 ${word.level} 문장은 3~7단어여야 해요 (현재 ${n}단어)`);
    }
    if (!s.answer.trim()) errors.push(`${tag}: answer가 비어 있어요`);
    if (!s.koHighlight || !s.ko.includes(s.koHighlight)) errors.push(`${tag}: koHighlight가 ko에 없어요`);
    if (!s.notes || !('*' in s.notes)) errors.push(`${tag}: notes에 "*" 키가 없어요`);
    for (const f of hasWord(en, INFORMAL)) errors.push(`${tag}: 본문에 줄임말 ${f}를 쓰면 안 돼요`);
    for (const b of hasWord(en, BRITISH)) errors.push(`${tag}: 영국식 철자 ${b}를 쓰면 안 돼요`);
    if (s.accepted?.some((a) => a.trim().toLowerCase() === s.answer.trim().toLowerCase()))
      errors.push(`${tag}: accepted에 answer가 들어 있어요`);
  }

  for (const w of words) {
    if ((counts.get(w.id) ?? 0) < 2) errors.push(`단어 ${w.id}: 문장이 2개 이상 있어야 해요 (현재 ${counts.get(w.id) ?? 0}개)`);
  }
  return errors;
}

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(path, 'utf8')) as T;
}

export function validateContentDir(dir: string): string[] {
  const errors: string[] = [];
  const coursesPath = join(dir, 'courses.json');
  if (!existsSync(coursesPath)) return [`${coursesPath} 파일이 없어요`];
  const courses = readJson<Course[]>(coursesPath);
  const words: Word[] = [];
  const sentences: Sentence[] = [];
  for (const f of readdirSync(dir).filter((f) => f.endsWith('.json') && f !== 'courses.json')) {
    const data = readJson<{ words?: Word[]; sentences?: Sentence[] }>(join(dir, f));
    words.push(...(data.words ?? []));
    sentences.push(...(data.sentences ?? []));
  }
  const courseIds = new Set(courses.map((c) => c.id));
  for (const w of words) if (!courseIds.has(w.courseId)) errors.push(`단어 ${w.id}: courseId ${w.courseId} 코스가 없어요`);
  return [...errors, ...validateContent(words, sentences)];
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const dir = resolve(fileURLToPath(import.meta.url), '../../content');
  const errors = validateContentDir(dir);
  if (errors.length) {
    console.error(errors.join('\n'));
    process.exit(1);
  }
  console.log('콘텐츠 검사를 통과했어요');
}
