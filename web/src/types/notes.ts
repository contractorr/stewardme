export type NoteStatus = "pending" | "accepted";

export type CorrectionType =
  | "spelling"
  | "grammar"
  | "factual"
  | "rewording"
  | "removal";

export interface NoteCorrection {
  type: CorrectionType;
  original: string;
  corrected: string;
  reason: string;
}

export interface NoteSummary {
  id: string;
  title: string;
  status: NoteStatus;
  created_at: string | null;
  accepted_at: string | null;
}

export interface Note extends NoteSummary {
  original_text: string | null;
  polished_markdown: string;
  polished_html: string;
  diff: string;
  corrections: NoteCorrection[];
}
