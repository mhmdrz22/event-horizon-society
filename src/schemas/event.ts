import { UserProfile } from "@/contexts/AuthContext";

export interface EventBase {
    title: string;
    description?: string;
    event_datetime: string;
    location: string;
    capacity: number;
}

export interface EventResponse extends EventBase {
  id: number;
  organizer_id: number;
  registered_count: number;
  created_at: string;
  updated_at: string;
  organizer?: UserProfile;
}

export interface EventRegistrationResponse {
    id: number;
    user_id: number;
    event_id: number;
    registered_at: string;
    user?: UserProfile;
    event?: EventBase;
}
