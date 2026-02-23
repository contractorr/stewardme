export interface LearningPath {
  id: string;
  skill: string;
  status: string;
  progress: number;
  total_modules: number;
  completed_modules: number;
  created_at: string;
  updated_at: string;
  content?: string;
}
