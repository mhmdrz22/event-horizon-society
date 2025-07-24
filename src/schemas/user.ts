import { z } from "zod";

export const UserSchema = z.object({
  id: z.number(),
  full_name: z.string(),
  email: z.string().email(),
  is_active: z.boolean(),
  is_superuser: z.boolean(),
  role: z.string(),
});

export type User = z.infer<typeof UserSchema>;
