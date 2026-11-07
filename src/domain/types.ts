export type Course = { id: string; order: number; title: string; summary: string };
export type Word = { id: string; word: string; meaning: string; level: 1 | 2 | 3 | 4 | 5; courseId: string };
export type Sentence = {
  id: string;
  wordId: string;
  before: string;
  answer: string;
  after: string; // en = before + answer + after
  ko: string;
  koHighlight: string;
  gloss: string;
  accepted: string[]; // 맞는 말이지만 이번 정답은 아닌 답
  notes: Record<string, string>; // 답별 설명. 기본 설명은 "*" 키
  alsoSay?: string; // 이렇게도 써요
};
