import { describe, expect, it } from 'vitest';
import { demoPacks } from './data/demoPacks';
import { parsePack } from './lib/validation';

describe('question packs', () => {
  it('validates the complete demo packs', () => {
    expect(demoPacks).toHaveLength(2);
    expect(() => parsePack(demoPacks[0])).not.toThrow();
    expect(demoPacks.every(pack => pack.questions.length === 10)).toBe(true);
  });
  it('rejects an answer index outside the options', () => {
    const invalid = structuredClone(demoPacks[0]);
    invalid.questions[0].answer = 99;
    expect(() => parsePack(invalid)).toThrow();
  });
  it('keeps explanation language variants separate', () => {
    const question = demoPacks[1].questions[0];
    expect(question.explanation.english.short).not.toBe(question.explanation.pidgin.short);
  });
});
