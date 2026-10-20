export type Language = 'english' | 'pidgin';
export type Question = { id: string; text: string; options: string[]; answer: number; topic: string; difficulty: 'easy' | 'medium'; explanation: { english: { short: string; steps: string[]; misconception?: string; memoryAid?: string }; pidgin: { short: string; steps: string[]; misconception?: string; memoryAid?: string } } };
export type Pack = { id: string; version: number; title: string; subject: string; level: string; topic: string; description: string; estimatedMinutes: number; language: string; questions: Question[] };
export type Result = { packId: string; answers: Record<string, number>; completedAt?: string };
