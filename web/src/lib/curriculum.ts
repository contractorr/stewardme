import type {
  LearningProgramFocusStatus,
  LearningTodayTask,
  RecommendationType,
} from "@/types/curriculum";

export const recommendationLabels: Record<RecommendationType | "fallback", string> = {
  continue: "Continue",
  enrolled: "Enrolled",
  ready: "Unlocked",
  entry: "Entry point",
  fallback: "Next step",
};

export const learningTaskLabels: Record<LearningTodayTask["task_type"], string> = {
  continue_chapter: "Continue",
  due_reviews: "Review",
  start_guide: "Start",
  applied_practice: "Apply",
};

export const learningProgramStatusLabels: Record<LearningProgramFocusStatus, string> = {
  active: "Active path",
  recommended: "Recommended path",
  available: "Available path",
};

export function formatLearningMinutes(minutes: number): string {
  if (minutes <= 0) {
    return "5m";
  }
  if (minutes < 60) {
    return `${minutes}m`;
  }
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  return remainingMinutes > 0 ? `${hours}h ${remainingMinutes}m` : `${hours}h`;
}

export function formatLearningSeconds(seconds: number): string {
  return formatLearningMinutes(Math.max(0, Math.round(seconds / 60)));
}

export function buildLearningTaskHref(task: LearningTodayTask): string {
  if (task.task_type === "due_reviews") {
    return "/learn/review";
  }
  if (task.guide_id && task.chapter_id) {
    return `/learn/${task.guide_id}/${task.chapter_id.split("/").pop()}`;
  }
  if (task.guide_id) {
    return `/learn/${task.guide_id}`;
  }
  return "/learn";
}
