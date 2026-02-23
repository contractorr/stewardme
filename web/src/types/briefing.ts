export interface BriefingSignal {
  id: number;
  type: string;
  severity: number;
  title: string;
  detail: string;
  suggested_actions: string[];
  evidence: string[];
  created_at: string;
}

export interface BriefingPattern {
  type: string;
  confidence: number;
  summary: string;
  evidence: string[];
  coaching_prompt: string;
}

export interface BriefingRecommendation {
  id: string;
  category: string;
  title: string;
  description: string;
  score: number;
  status: string;
}

export interface BriefingGoal {
  path: string;
  title: string;
  status: string;
  days_since_check: number;
}

export interface BriefingResponse {
  signals: BriefingSignal[];
  patterns: BriefingPattern[];
  recommendations: BriefingRecommendation[];
  stale_goals: BriefingGoal[];
  has_data: boolean;
}
