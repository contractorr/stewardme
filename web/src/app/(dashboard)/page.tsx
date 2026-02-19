"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useToken } from "@/hooks/useToken";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
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

export default function DashboardPage() {
  const token = useToken();
  const [entries, setEntries] = useState<JournalEntry[]>([]);
  const [goals, setGoals] = useState<Goal[]>([]);
  const [intel, setIntel] = useState<Record<string, unknown>[]>([]);

  useEffect(() => {
    if (!token) return;
    apiFetch<JournalEntry[]>("/api/journal?limit=5", {}, token).then(setEntries).catch(() => {});
    apiFetch<Goal[]>("/api/goals", {}, token).then(setGoals).catch(() => {});
    apiFetch<Record<string, unknown>[]>("/api/intel/recent?limit=5", {}, token).then(setIntel).catch(() => {});
  }, [token]);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Dashboard</h1>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Recent Journal */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">
              <Link href="/journal" className="hover:underline">
                Recent Journal
              </Link>
            </CardTitle>
            <CardDescription>{entries.length} recent entries</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            {entries.map((e) => (
              <div key={e.path} className="text-sm">
                <span className="font-medium">{e.title}</span>
                <Badge variant="outline" className="ml-2 text-xs">
                  {e.type}
                </Badge>
              </div>
            ))}
            {entries.length === 0 && (
              <p className="text-sm text-muted-foreground">No entries yet</p>
            )}
          </CardContent>
        </Card>

        {/* Goals */}
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
          <CardContent className="space-y-2">
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
            {goals.length === 0 && (
              <p className="text-sm text-muted-foreground">No goals yet</p>
            )}
          </CardContent>
        </Card>

        {/* Intel */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">
              <Link href="/intel" className="hover:underline">
                Latest Intel
              </Link>
            </CardTitle>
            <CardDescription>{intel.length} recent items</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
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
            {intel.length === 0 && (
              <p className="text-sm text-muted-foreground">No intel yet</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
