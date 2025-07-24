import { z } from "zod";
import { UserSchema } from "./user";

export const ArticleStatusSchema = z.enum(["pending", "approved", "rejected"]);
export type ArticleStatus = z.infer<typeof ArticleStatusSchema>;

export const ArticleSchema = z.object({
  id: z.number(),
  title: z.string(),
  content: z.string(),
  author_id: z.number(),
  status: ArticleStatusSchema,
  review_comments: z.string().optional(),
  submitted_at: z.string(),
  reviewed_at: z.string().optional(),
  author: UserSchema.optional(),
});

export type Article = z.infer<typeof ArticleSchema>;
