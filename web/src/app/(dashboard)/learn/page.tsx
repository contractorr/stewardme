"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { toast } from "sonner";
import { ArrowRight, RefreshCcw, RotateCcw, Search } from "lucide-react";

import { WorkspacePageHeader } from "@/components/WorkspacePageHeader";
import { GuideCard } from "@/components/curriculum/GuideCard";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useToken } from "@/hooks/useToken";
import { apiFetch } from "@/lib/api";
import {
  buildLearningTaskHref,
  formatLearningMinutes,
  learningTaskLabels,
} from "@/lib/curriculum";
import type { Guide, LearningStats, LearningToday, LearningTodayTask } from "@/types/curriculum";

function sortGuides(guides: Guide[]): Guide[] {
  return [...guides].sort((left, right) => {
    const leftProgress = left.progress_pct ?? 0;
    const rightProgress = right.progress_pct ?? 0;
    const leftActive = left.enrolled && leftProgress < 100;
    const rightActive = right.enrolled && rightProgress < 100;

    if (leftActive !== rightActive) {
      return Number(rightActive) - Number(leftActive);
    }

    const leftStarted = leftProgress > 0;
    const rightStarted = rightProgress > 0;
    if (leftStarted !== rightStarted) {
      return Number(rightStarted) - Number(leftStarted);
    }

    if (leftProgress !== rightProgress) {
      return rightProgress - leftProgress;
    }

    return left.title.localeCompare(right.title);
  });
}

function getReviewCount(
  task: LearningTodayTask | null,
  stats: LearningStats | null,
  today: LearningToday | null,
): number {
  if (!task) {
    return stats?.reviews_due ?? today?.reviews_due ?? 0;
  }
  return task.review_count ?? task.retry_count ?? stats?.reviews_due ?? today?.reviews_due ?? 0;
}

export default function LearnPage() {
  const token = useToken();
  const [guides, setGuides] = useState<Guide[]>([]);
  const [stats, setStats] = useState<LearningStats | null>(null);
  const [today, setToday] = useState<LearningToday | null>(null);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [search, setSearch] = useState("");

  const loadData = async () => {
    if (!token) return;
    setLoading(true);
    try {
      const [guidesData, statsData, todayData] = await Promise.all([
        apiFetch<Guide[]>("/api/v1/curriculum/guides", {}, token),
        apiFetch<LearningStats>("/api/v1/curriculum/stats", {}, token),
        apiFetch<LearningToday>("/api/v1/curriculum/today", {}, token),
      ]);
      setGuides(guidesData);
      setStats(statsData);
      setToday(todayData);
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadData();
  }, [token]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleSync = async () => {
    if (!token) return;
    setSyncing(true);
    try {
      const result = await apiFetch<{
        synced_guides: number;
        message?: string;
      }>("/api/v1/curriculum/sync", { method: "POST" }, token);
      await loadData();
      toast.success(result.message || `Synced ${result.synced_guides} guides`);
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setSyncing(false);
    }
  };

  const visibleGuides = useMemo(() => {
    const query = search.trim().toLowerCase();
    const filtered = query
      ? guides.filter((guide) => guide.title.toLowerCase().includes(query))
      : guides;
    return sortGuides(filtered);
  }, [guides, search]);

  const reviewTask =
    today?.tasks.find(
      (task) => task.task_type === "due_reviews" || task.task_type === "retry_reviews",
    ) ?? null;

  const nextUpTask =
    today?.tasks.find(
      (task) => task.task_type === "continue_chapter" || task.task_type === "start_guide",
    ) ??
    reviewTask ??
    today?.tasks.find((task) => Boolean(task.guide_id || task.chapter_id)) ??
    today?.tasks[0] ??
    null;

  const reviewCount = getReviewCount(reviewTask, stats, today);
  const inProgressCount = guides.filter(
    (guide) => (guide.progress_pct ?? 0) > 0 && (guide.progress_pct ?? 0) < 100,
  ).length;

  return (
    <div className="mx-auto max-w-6xl space-y-6 p-4 md:p-6">
      <WorkspacePageHeader
        title="Library"
        description="Pick a guide, continue your next chapter, and clear reviews when they are due."
        eyebrow="Curriculum"
        actions={
          <Button
            size="sm"
            variant="outline"
            onClick={handleSync}
            disabled={syncing}
          >
            <RefreshCcw
              className={`mr-1.5 h-3.5 w-3.5 ${syncing ? "animate-spin" : ""}`}
            />
            Sync
          </Button>
        }
      />

      <section className="grid gap-4 lg:grid-cols-[minmax(0,1.5fr)_minmax(280px,0.9fr)]">
        <Card>
          <CardHeader className="space-y-2">
            <div className="space-y-1">
              <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-muted-foreground">
                Next up
              </p>
              <CardTitle className="text-2xl">
                {nextUpTask?.title ?? "Choose a guide to start learning"}
              </CardTitle>
              <CardDescription>
                {nextUpTask?.detail ??
                  "Start with one guide and move through it chapter by chapter."}
              </CardDescription>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            {nextUpTask ? (
              <>
                <div className="flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
                  <span className="rounded-full border px-2 py-1">
                    {learningTaskLabels[nextUpTask.task_type]}
                  </span>
                  <span>{formatLearningMinutes(nextUpTask.estimate_minutes)}</span>
                  {nextUpTask.guide_title ? <span>{nextUpTask.guide_title}</span> : null}
                </div>
                <div className="flex flex-wrap gap-2">
                  <Button asChild>
                    <Link href={buildLearningTaskHref(nextUpTask)}>
                      {nextUpTask.cta_label}
                      <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
                    </Link>
                  </Button>
                  <Button variant="outline" asChild>
                    <Link href="#browse-guides">Browse guides</Link>
                  </Button>
                </div>
              </>
            ) : (
              <Button asChild>
                <Link href="#browse-guides">
                  Browse guides
                  <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
                </Link>
              </Button>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="space-y-2">
            <div className="flex items-center gap-2 text-muted-foreground">
              <RotateCcw className="h-4 w-4" />
              <p className="text-[11px] font-semibold uppercase tracking-[0.18em]">
                Reviews
              </p>
            </div>
            <CardTitle>
              {reviewCount > 0
                ? `${reviewCount} review${reviewCount === 1 ? "" : "s"} due`
                : "You’re caught up"}
            </CardTitle>
            <CardDescription>
              {reviewCount > 0
                ? "Use one short review session to keep what you’ve learned fresh."
                : "New reviews will show up here after you finish more chapters."}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {reviewCount > 0 ? (
              <Button asChild>
                <Link href="/learn/review">Start review</Link>
              </Button>
            ) : (
              <Button variant="outline" asChild>
                <Link href="#browse-guides">Browse guides</Link>
              </Button>
            )}
            <p className="text-sm text-muted-foreground">
              {inProgressCount > 0
                ? `${inProgressCount} guide${inProgressCount === 1 ? "" : "s"} currently in progress.`
                : "No guides in progress yet."}
            </p>
          </CardContent>
        </Card>
      </section>

      <section id="browse-guides" className="space-y-4">
        <div className="space-y-1">
          <h2 className="text-lg font-semibold">Browse guides</h2>
          <p className="text-sm text-muted-foreground">
            Search the catalog and pick one guide to start or continue.
          </p>
        </div>

        <div className="relative max-w-md">
          <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            className="pl-9"
            placeholder="Search guides"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />
        </div>

        {loading ? (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, index) => (
              <Card key={index} className="animate-pulse">
                <CardHeader className="pb-2">
                  <div className="h-5 w-3/4 rounded bg-muted" />
                </CardHeader>
                <CardContent>
                  <div className="h-3 w-1/2 rounded bg-muted" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : visibleGuides.length === 0 ? (
          <Card>
            <CardContent className="p-6 text-sm text-muted-foreground">
              No guides match that search.
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {visibleGuides.map((guide) => (
              <GuideCard key={guide.id} guide={guide} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
