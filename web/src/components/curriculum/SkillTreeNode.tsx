"use client";

import { forwardRef } from "react";
import { useRouter } from "next/navigation";
import { Diamond } from "lucide-react";
import { cn } from "@/lib/utils";
import type { SkillTreeNode as SkillTreeNodeType } from "@/types/curriculum";

interface SkillTreeNodeProps {
  node: SkillTreeNodeType;
  trackColor: string;
}

const statusStyles: Record<string, string> = {
  not_started: "bg-muted text-muted-foreground",
  enrolled: "bg-background ring-1 ring-blue-200 border-blue-300",
  in_progress: "bg-background ring-1 ring-amber-200 border-amber-300",
  completed: "bg-green-50 border-green-300 dark:bg-green-950/30",
};

export const SkillTreeNodeCard = forwardRef<HTMLDivElement, SkillTreeNodeProps>(
  function SkillTreeNodeCard({ node, trackColor }, ref) {
    const router = useRouter();

    return (
      <div
        ref={ref}
        role="button"
        tabIndex={0}
        onClick={() => router.push(`/learn/${node.id}`)}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") router.push(`/learn/${node.id}`);
        }}
        className={cn(
          "w-40 cursor-pointer rounded-md border p-2.5 transition-shadow hover:shadow-md",
          statusStyles[node.status] ?? statusStyles.not_started,
        )}
        style={{ borderLeftWidth: 4, borderLeftColor: trackColor }}
      >
        <div className="flex items-start gap-1">
          {node.is_entry_point && (
            <Diamond
              className="mt-0.5 h-3 w-3 shrink-0 fill-current text-orange-500"
              title="Entry point - recommended starting guide"
            />
          )}
          <p className="line-clamp-2 text-xs font-medium leading-tight">{node.title}</p>
        </div>

        {node.mastery_score > 0 && (
          <p className="mt-1 text-[10px] text-muted-foreground">
            Mastery {Math.round(node.mastery_score)}%
          </p>
        )}

        {node.enrolled && node.progress_pct > 0 && (
          <div className="mt-1.5">
            <div className="h-1 rounded-full bg-muted overflow-hidden">
              <div
                className="h-full rounded-full bg-primary transition-all"
                style={{ width: `${node.progress_pct}%` }}
              />
            </div>
          </div>
        )}
      </div>
    );
  },
);
