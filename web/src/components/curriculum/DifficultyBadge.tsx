import { Badge } from "@/components/ui/badge";
import type { DifficultyLevel } from "@/types/curriculum";

const colors: Record<DifficultyLevel, string> = {
  introductory: "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300",
  intermediate: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300",
  advanced: "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300",
};

export function DifficultyBadge({ level }: { level: DifficultyLevel }) {
  return (
    <Badge variant="outline" className={colors[level]}>
      {level}
    </Badge>
  );
}
