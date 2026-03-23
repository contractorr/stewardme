import Link from "next/link";
import { Check, Circle, Clock } from "lucide-react";
import { cn } from "@/lib/utils";
import type { Chapter } from "@/types/curriculum";

function StatusIcon({ status }: { status?: string }) {
  if (status === "completed")
    return <Check className="h-4 w-4 text-green-500 shrink-0" />;
  if (status === "in_progress")
    return <Clock className="h-4 w-4 text-yellow-500 shrink-0" />;
  return <Circle className="h-4 w-4 text-muted-foreground/40 shrink-0" />;
}

interface ChapterListProps {
  guideId: string;
  chapters: Chapter[];
  activeChapterId?: string;
}

export function ChapterList({ guideId, chapters, activeChapterId }: ChapterListProps) {
  return (
    <div className="space-y-0.5">
      {chapters.map((ch) => {
        const isActive = ch.id === activeChapterId;
        return (
          <Link
            key={ch.id}
            href={`/learn/${guideId}/${ch.id.split("/").pop()}`}
            className={cn(
              "flex items-center gap-2.5 rounded-md px-3 py-2 text-sm transition-colors hover:bg-accent",
              isActive && "bg-accent font-medium",
              ch.is_glossary && "opacity-60"
            )}
          >
            <StatusIcon status={ch.status} />
            <span className="truncate flex-1">{ch.title}</span>
            <span className="text-[10px] text-muted-foreground shrink-0">
              {ch.reading_time_minutes}m
            </span>
          </Link>
        );
      })}
    </div>
  );
}
