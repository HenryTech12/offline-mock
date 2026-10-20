import { z } from 'zod';

const explanation = z.object({ short: z.string().min(1), steps: z.array(z.string()).min(1), misconception: z.string().optional(), memoryAid: z.string().optional() });
export const questionSchema = z.object({ id: z.string().min(1), text: z.string().min(1), options: z.array(z.string().min(1)).min(2).max(6), answer: z.number().int().nonnegative(), topic: z.string().min(1), difficulty: z.enum(['easy', 'medium']), explanation: z.object({ english: explanation, pidgin: explanation }) }).strict().refine(q => q.answer < q.options.length, 'answer must point to an option');
export const packSchema = z.object({ id: z.string().min(1), version: z.number().int().positive(), title: z.string().min(1), subject: z.string().min(1), level: z.string().min(1), topic: z.string().min(1), description: z.string().min(1), estimatedMinutes: z.number().positive(), language: z.string().min(1), questions: z.array(questionSchema).min(1) }).strict();
export function parsePack(input: unknown) { return packSchema.parse(input); }
