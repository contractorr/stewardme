import Link from "next/link";
import { BookOpen, Clock } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { Guide } from "@/types/curriculum";
import { DifficultyBadge } from "./DifficultyBadge";
import { ProgressRing } from "./ProgressRing";

function formatTime(minutes: number): string {
  if (minutes < 60) return `${minutes}m`;
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return m > 0 ? `${h}h ${m}m` : `${h}h`;
}

const categoryLabels: Record<string, string> = {
  science: "Science",
  humanities: "Humanities",
  business: "Business",
  technology: "Technology",
  industry: "Industry",
  social_science: "Social Science",
  professional: "Professional",
};

export function GuideCard({ guide }: { guide: Guide }) {
  const pct = guide.progress_pct ?? 0;
  return (
    <Link href={`/learn/${guide.id}`}>
      <Card className="h-full transition-colors hover:border-primary/40 hover:shadow-md">
        <CardHeader className="pb-2">
          <div className="flex items-start justify-between gap-2">
            <CardTitle className="text-base leading-snug">{guide.title}</CardTitle>
            {pct > 0 && <ProgressRing progress={pct} size={36} />}
          </div>
          <div className="flex flex-wrap gap-1.5 pt-1">
            <Badge variant="secondary" className="text-[10px]">
              {categoryLabels[guide.category] ?? guide.category}
            </Badge>
            <DifficultyBadge level={guide.difficulty} />
          </div>
        </CardHeader>
        <CardContent className="pt-0">
          <div className="flex items-center gap-3 text-xs text-muted-foreground">
            <span className="flex items-center gap-1">
              <BookOpen className="h-3 w-3" />
              {guide.chapter_count} chapters
            </span>
            <span className="flex items-center gap-1">
              <Clock className="h-3 w-3" />
              {formatTime(guide.total_reading_time_minutes)}
            </span>
          </div>
          {(guide.chapters_completed ?? 0) > 0 && (
            <div className="mt-2">
              <div className="h-1.5 rounded-full bg-muted overflow-hidden">
                <div
                  className="h-full rounded-full bg-primary transition-all"
                  style={{ width: `${pct}%` }}
                />
              </div>
              <p className="mt-1 text-[10px] text-muted-foreground">
                {guide.chapters_completed}/{guide.chapters_total} completed
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </Link>
  );
}
