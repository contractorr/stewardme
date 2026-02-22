"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { useToken } from "@/hooks/useToken";
import { BookOpen, Newspaper, Plus, Target } from "lucide-react";
import { OnboardingDialog } from "@/components/OnboardingDialog";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";

interface JournalEntry {
  path: string;
  title: string;
  type: string;
  created: string | null;
  tags: string[];
  preview: string;
}

interface Goal {
  path: string;
  title: string;
  status: string;
  days_since_check: number;
  is_stale: boolean;
}

function CardSkeleton() {
  return (
    <Card>
      <CardHeader>
        <div className="h-4 w-32 animate-pulse rounded bg-muted" />
        <div className="h-3 w-20 animate-pulse rounded bg-muted" />
      </CardHeader>
      <CardContent className="space-y-2">
        <div className="h-3 w-full animate-pulse rounded bg-muted" />
        <div className="h-3 w-3/4 animate-pulse rounded bg-muted" />
        <div className="h-3 w-1/2 animate-pulse rounded bg-muted" />
      </CardContent>
    </Card>
  );
}

function EmptyCard({
  icon: Icon,
  title,
  description,
  href,
  action,
}: {
  icon: React.ElementType;
  title: string;
  description: string;
  href: string;
  action: string;
}) {
  return (
    <div className="flex flex-col items-center justify-center py-6 text-center">
      <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-full bg-muted">
        <Icon className="h-5 w-5 text-muted-foreground" />
      </div>
      <p className="text-sm text-muted-foreground">{description}</p>
      <Button asChild variant="link" size="sm" className="mt-1">
        <Link href={href}>{action}</Link>
      </Button>
    </div>
  );
}

export default function DashboardPage() {
  const token = useToken();
  const [entries, setEntries] = useState<JournalEntry[]>([]);
  const [goals, setGoals] = useState<Goal[]>([]);
  const [intel, setIntel] = useState<Record<string, unknown>[]>([]);
  const [loading, setLoading] = useState(!!token);
  const [showOnboarding, setShowOnboarding] = useState(false);

  const loadDashboard = useCallback((t: string) => {
    return Promise.allSettled([
      apiFetch<JournalEntry[]>("/api/journal?limit=5", {}, t),
      apiFetch<Goal[]>("/api/goals", {}, t),
      apiFetch<Record<string, unknown>[]>("/api/intel/recent?limit=5", {}, t),
      apiFetch<{ llm_api_key_set: boolean }>("/api/settings", {}, t),
    ]);
  }, []);

  useEffect(() => {
    if (!token) return;
    let cancelled = false;
    setLoading(true);
    loadDashboard(token).then(([journalRes, goalsRes, intelRes, settingsRes]) => {
      if (cancelled) return;
      if (journalRes.status === "fulfilled") setEntries(journalRes.value);
      if (goalsRes.status === "fulfilled") setGoals(goalsRes.value);
      if (intelRes.status === "fulfilled") setIntel(intelRes.value);
      if (settingsRes.status === "fulfilled") {
        if (!settingsRes.value.llm_api_key_set && !localStorage.getItem("onboarding_dismissed")) {
          setShowOnboarding(true);
        }
      }
      setLoading(false);
    });
    return () => { cancelled = true; };
  }, [token, loadDashboard]);

  const fetchData = useCallback(() => {
    if (!token) return;
    loadDashboard(token).then(([journalRes, goalsRes, intelRes]) => {
      if (journalRes.status === "fulfilled") setEntries(journalRes.value);
      if (goalsRes.status === "fulfilled") setGoals(goalsRes.value);
      if (intelRes.status === "fulfilled") setIntel(intelRes.value);
    });
  }, [token, loadDashboard]);

  const dismissOnboarding = () => {
    localStorage.setItem("onboarding_dismissed", "true");
    setShowOnboarding(false);
  };

  return (
    <div className="space-y-6">
      {token && (
        <OnboardingDialog
          open={showOnboarding}
          onClose={dismissOnboarding}
          onComplete={fetchData}
          token={token}
        />
      )}
      <div>
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <p className="text-sm text-muted-foreground">
          Your personal assistant overview
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Recent Journal */}
        {loading ? (
          <CardSkeleton />
        ) : (
          <Card>
            <CardHeader>
              <CardTitle className="text-base">
                <Link href="/journal" className="hover:underline">
                  Recent Journal
                </Link>
              </CardTitle>
              <CardDescription>{entries.length} recent entries</CardDescription>
            </CardHeader>
            <CardContent>
              {entries.length > 0 ? (
                <div className="space-y-2">
                  {entries.map((e) => (
                    <div key={e.path} className="text-sm">
                      <span className="font-medium">{e.title}</span>
                      <Badge variant="outline" className="ml-2 text-xs">
                        {e.type}
                      </Badge>
                    </div>
                  ))}
                </div>
              ) : (
                <EmptyCard
                  icon={BookOpen}
                  title="Journal"
                  description="Start journaling to track your thoughts"
                  href="/journal"
                  action="Write first entry"
                />
              )}
            </CardContent>
          </Card>
        )}

        {/* Goals */}
        {loading ? (
          <CardSkeleton />
        ) : (
          <Card>
            <CardHeader>
              <CardTitle className="text-base">
                <Link href="/goals" className="hover:underline">
                  Active Goals
                </Link>
              </CardTitle>
              <CardDescription>
                {goals.filter((g) => g.status === "active").length} active
              </CardDescription>
            </CardHeader>
            <CardContent>
              {goals.length > 0 ? (
                <div className="space-y-2">
                  {goals
                    .filter((g) => g.status === "active")
                    .slice(0, 5)
                    .map((g) => (
                      <div key={g.path} className="flex items-center gap-2 text-sm">
                        <span className="font-medium">{g.title}</span>
                        {g.is_stale && (
                          <Badge variant="destructive" className="text-xs">
                            Stale
                          </Badge>
                        )}
                      </div>
                    ))}
                </div>
              ) : (
                <EmptyCard
                  icon={Target}
                  title="Goals"
                  description="Set goals to track your progress"
                  href="/goals"
                  action="Create first goal"
                />
              )}
            </CardContent>
          </Card>
        )}

        {/* Intel */}
        {loading ? (
          <CardSkeleton />
        ) : (
          <Card>
            <CardHeader>
              <CardTitle className="text-base">
                <Link href="/intel" className="hover:underline">
                  Latest Intel
                </Link>
              </CardTitle>
              <CardDescription>{intel.length} recent items</CardDescription>
            </CardHeader>
            <CardContent>
              {intel.length > 0 ? (
                <div className="space-y-2">
                  {intel.map((item, i) => (
                    <div key={i} className="text-sm">
                      <a
                        href={item.url as string}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="font-medium hover:underline"
                      >
                        {item.title as string}
                      </a>
                      <Badge variant="outline" className="ml-2 text-xs">
                        {item.source as string}
                      </Badge>
                    </div>
                  ))}
                </div>
              ) : (
                <EmptyCard
                  icon={Newspaper}
                  title="Intel"
                  description="Scrape sources to populate intelligence"
                  href="/intel"
                  action="Go to Intel"
                />
              )}
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
