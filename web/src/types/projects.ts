export interface MatchingIssue {
  title: string;
  url: string;
  summary: string;
  tags: string[];
  source: string;
  match_score: number;
}
