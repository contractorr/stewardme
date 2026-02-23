"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import {
  Area,
  AreaChart,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { TrendingUp, BookOpen } from "lucide-react";
import { useToken } from "@/hooks/useToken";
import { apiFetch } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import type { MoodDataPoint, TopicTrend } from "@/types/trends";
import Link from "next/link";

const DAYS_OPTIONS = [7, 30, 90] as const;

function moodColor(score: number) {
  if (score > 0.2) return "#22c55e";
  if (score < -0.2) return "#ef4444";
  return "#eab308";
}

function MoodSkeleton() {
  return (
    <div className="space-y-4">
      <div className="h-64 w-full animate-pulse rounded bg-muted" />
      <div className="flex gap-4">
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="h-16 w-32 animate-pulse rounded bg-muted" />
        ))}
      </div>
    </div>
  );
}

function TopicSkeleton() {
  return (
    <div className="space-y-3">
      {Array.from({ length: 4 }).map((_, i) => (
        <Card key={i}>
          <CardHeader className="pb-2">
            <div className="h-4 w-1/3 animate-pulse rounded bg-muted" />
          </CardHeader>
          <CardContent>
            <div className="h-3 w-2/3 animate-pulse rounded bg-muted" />
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

function directionBadge(direction: string) {
  const variant =
    direction === "emerging"
      ? "default"
      : direction === "declining"
        ? "destructive"
        : "secondary";
  return <Badge variant={variant}>{direction}</Badge>;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function CustomTooltip({ active, payload }: any) {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload as MoodDataPoint;
  return (
    <div className="rounded border bg-popover p-2 text-sm shadow">
      <p className="font-medium">{d.date}</p>
      <p style={{ color: moodColor(d.score) }}>
        Score: {d.score.toFixed(2)} ({d.label})
      </p>
      {d.title && <p className="text-muted-foreground">{d.title}</p>}
    </div>
  );
}

export default function TrendsPage() {
  const token = useToken();
  const [mood, setMood] = useState<MoodDataPoint[]>([]);
  const [topics, setTopics] = useState<TopicTrend[]>([]);
  const [moodLoading, setMoodLoading] = useState(true);
  const [topicsLoading, setTopicsLoading] = useState(true);
  const [days, setDays] = useState<number>(30);

  useEffect(() => {
    if (!token) {
      setMoodLoading(false);
      setTopicsLoading(false);
      return;
    }
    setMoodLoading(true);
    apiFetch<MoodDataPoint[]>(`/api/trends/mood?days=${days}`, {}, token)
      .then(setMood)
      .catch((e) => toast.error(e.message))
      .finally(() => setMoodLoading(false));
  }, [token, days]);

  useEffect(() => {
    if (!token) return;
    setTopicsLoading(true);
    apiFetch<TopicTrend[]>("/api/trends/topics?days=90", {}, token)
      .then(setTopics)
      .catch((e) => toast.error(e.message))
      .finally(() => setTopicsLoading(false));
  }, [token]);

  const avgScore =
    mood.length > 0
      ? (mood.reduce((s, m) => s + m.score, 0) / mood.length).toFixed(2)
      : "—";

  const chartData = mood.map((m) => ({
    ...m,
    fill: moodColor(m.score),
  }));

  return (
    <div className="space-y-6 p-6">
      <h1 className="text-2xl font-semibold">Trends</h1>

      <Tabs defaultValue="mood">
        <TabsList>
          <TabsTrigger value="mood">Mood</TabsTrigger>
          <TabsTrigger value="topics">Topics</TabsTrigger>
        </TabsList>

        {/* Mood tab */}
        <TabsContent value="mood" className="space-y-4">
          <div className="flex items-center gap-2">
            {DAYS_OPTIONS.map((d) => (
              <Button
                key={d}
                variant={days === d ? "default" : "outline"}
                size="sm"
                onClick={() => setDays(d)}
              >
                {d}d
              </Button>
            ))}
          </div>

          {moodLoading && <MoodSkeleton />}

          {!moodLoading && mood.length === 0 && (
            <div className="flex flex-col items-center justify-center py-16 text-center">
              <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-muted">
                <BookOpen className="h-7 w-7 text-muted-foreground" />
              </div>
              <h3 className="text-lg font-medium">No mood data yet</h3>
              <p className="mt-1 max-w-sm text-sm text-muted-foreground">
                Write more journal entries to see your mood trends over time.
              </p>
              <Link href="/journal">
                <Button variant="outline" className="mt-4">
                  Go to Journal
                </Button>
              </Link>
            </div>
          )}

          {!moodLoading && mood.length > 0 && (
            <>
              <div className="flex gap-4">
                <Card className="flex-1">
                  <CardHeader className="pb-1">
                    <CardDescription>Avg Score</CardDescription>
                    <CardTitle className="text-xl">{avgScore}</CardTitle>
                  </CardHeader>
                </Card>
                <Card className="flex-1">
                  <CardHeader className="pb-1">
                    <CardDescription>Entries</CardDescription>
                    <CardTitle className="text-xl">{mood.length}</CardTitle>
                  </CardHeader>
                </Card>
              </div>

              <Card>
                <CardContent className="pt-6">
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={chartData}>
                      <defs>
                        <linearGradient
                          id="moodGradient"
                          x1="0"
                          y1="0"
                          x2="0"
                          y2="1"
                        >
                          <stop
                            offset="5%"
                            stopColor="#22c55e"
                            stopOpacity={0.3}
                          />
                          <stop
                            offset="95%"
                            stopColor="#ef4444"
                            stopOpacity={0.1}
                          />
                        </linearGradient>
                      </defs>
                      <XAxis
                        dataKey="date"
                        tick={{ fontSize: 12 }}
                        tickLine={false}
                      />
                      <YAxis domain={[-1, 1]} tick={{ fontSize: 12 }} />
                      <Tooltip content={<CustomTooltip />} />
                      <Area
                        type="monotone"
                        dataKey="score"
                        stroke="#6366f1"
                        strokeWidth={2}
                        fill="url(#moodGradient)"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </>
          )}
        </TabsContent>

        {/* Topics tab */}
        <TabsContent value="topics" className="space-y-4">
          {topicsLoading && <TopicSkeleton />}

          {!topicsLoading && topics.length === 0 && (
            <div className="flex flex-col items-center justify-center py-16 text-center">
              <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-muted">
                <TrendingUp className="h-7 w-7 text-muted-foreground" />
              </div>
              <h3 className="text-lg font-medium">Not enough data</h3>
              <p className="mt-1 max-w-sm text-sm text-muted-foreground">
                Write more journal entries to see topic trends. At least 8
                entries with embeddings are needed.
              </p>
              <Link href="/journal">
                <Button variant="outline" className="mt-4">
                  Go to Journal
                </Button>
              </Link>
            </div>
          )}

          {!topicsLoading && topics.length > 0 && (
            <div className="space-y-3">
              {topics.map((t, i) => (
                <Card key={i}>
                  <CardHeader className="pb-2">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-base">{t.topic}</CardTitle>
                      <div className="flex items-center gap-2">
                        {directionBadge(t.direction)}
                        <Badge variant="outline">
                          {(t.growth_rate * 100).toFixed(0)}%
                        </Badge>
                      </div>
                    </div>
                    <CardDescription>
                      {t.total_entries} entries across {t.windows.length} windows
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center gap-4">
                      <div className="h-10 w-32">
                        <ResponsiveContainer width="100%" height="100%">
                          <LineChart data={t.counts.map((c, j) => ({ v: c, w: t.windows[j] }))}>
                            <Line
                              type="monotone"
                              dataKey="v"
                              stroke="#6366f1"
                              strokeWidth={1.5}
                              dot={false}
                            />
                          </LineChart>
                        </ResponsiveContainer>
                      </div>
                      {t.representative_titles.length > 0 && (
                        <p className="text-xs text-muted-foreground line-clamp-2">
                          {t.representative_titles.join(" · ")}
                        </p>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
