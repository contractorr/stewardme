export interface MoodDataPoint {
  date: string;
  score: number;
  label: string;
  title: string;
}

export interface TopicTrend {
  topic: string;
  direction: string;
  growth_rate: number;
  counts: number[];
  windows: string[];
  total_entries: number;
  representative_titles: string[];
}
