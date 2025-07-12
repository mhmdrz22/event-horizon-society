import { UserProfile } from "@/contexts/AuthContext";

export type ArticleStatus = "pending" | "approved" | "rejected";

export interface Article {
  id: number;
  title: string;
  content: string;
  author_id: number;
  status: ArticleStatus;
  review_comments?: string;
  submitted_at: string;
  reviewed_at?: string;
  author?: UserProfile;
}
