export interface BriefSource {
  title: string;
  url: string;
}

export interface BriefSection {
  kind: string; // "signals" | "journal" | "custom"
  title: string;
  body: string;
  items?: Array<Record<string, unknown>>;
  sources?: BriefSource[];
  researched?: boolean;
  topic?: string;
}

export type BriefStatus = "unread" | "read" | "dismissed";

export interface Brief {
  id: string;
  status: BriefStatus;
  summary: string;
  period_start: string;
  period_end: string;
  created_at: string;
  sections: BriefSection[];
}

export interface BriefLatestResponse {
  brief: Brief | null;
  should_generate: boolean;
}

export interface BriefCustomSection {
  id: string;
  title: string;
  instructions: string;
  use_research: boolean;
}

export interface BriefConfig {
  enabled: boolean;
  min_interval_hours: number;
  include_signals: boolean;
  include_journal: boolean;
  include_calendar: boolean;
  include_email: boolean;
  max_items_per_section: number;
  custom_sections: BriefCustomSection[];
}

export interface GoogleStatus {
  calendar_connected: boolean;
  gmail_connected: boolean;
  gmail_address: string | null;
}
