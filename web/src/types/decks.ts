export interface Flashcard {
  id: string;
  deck_id: string;
  front: string;
  back: string;
  tags: string[];
  easiness_factor: number;
  interval_days: number;
  repetitions: number;
  next_review: string | null;
  last_reviewed: string | null;
  created_at: string | null;
}

export interface Deck {
  id: string;
  title: string;
  description: string;
  source: "created" | "imported";
  card_count: number;
  due_count: number;
  created_at: string | null;
}

export interface DeckDetail extends Deck {
  cards: Flashcard[];
}

export interface DeckImportResult extends Deck {
  skipped_empty: number;
  skipped_media: number;
}

export type FlashcardRating = "again" | "hard" | "good" | "easy";
