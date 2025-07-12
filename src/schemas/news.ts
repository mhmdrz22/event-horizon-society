import { UserProfile } from "@/contexts/AuthContext";

export type NewsStatus = "draft" | "published";

export interface News {
  id: number;
  title: string;
  content: string;
  author_id: number;
  status: NewsStatus;
  created_at: string;
  updated_at: string;
  author?: UserProfile;
}
