"use client";

import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";
import { ArrowRight, Check, Newspaper, X } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useToken } from "@/hooks/useToken";
import { apiFetch } from "@/lib/api";
import type { Brief, BriefLatestResponse } from "@/types/brief";

function formatWindow(brief: Brief): string {
  const start = new Date(brief.period_start);
  const end = new Date(brief.period_end);
  const days = Math.max(1, Math.round((end.getTime() - start.getTime()) / 86_400_000));
  return days === 1 ? "Covering the last day" : `Covering the last ${days} days`;
}

export function BriefCard() {
  const token = useToken();
  const [brief, setBrief] = useState<Brief | null>(null);
  const [generating, setGenerating] = useState(false);
  const requested = useRef(false);

  useEffect(() => {
    if (!token || requested.current) return;
    requested.current = true;
    let cancelled = false;

    apiFetch<BriefLatestResponse>("/api/v1/brief/latest", {}, token)
      .then((data) => {
        if (cancelled) return;
        if (data.brief?.status === "unread") setBrief(data.brief);
        if (data.should_generate) {
          setGenerating(true);
          apiFetch<Brief>("/api/v1/brief/generate", { method: "POST" }, token)
            .then((fresh) => {
              if (!cancelled && fresh.status === "unread") setBrief(fresh);
            })
            .catch(() => {})
            .finally(() => {
              if (!cancelled) setGenerating(false);
            });
        }
      })
      .catch(() => {});

    return () => {
      cancelled = true;
    };
  }, [token]);

  const setStatus = useCallback(
    (action: "read" | "dismiss") => {
      if (!token || !brief) return;
      apiFetch(`/api/v1/brief/${brief.id}/${action}`, { method: "POST" }, token).catch(() => {});
      setBrief(null);
    },
    [token, brief]
  );

  if (!brief && !generating) return null;

  if (!brief && generating) {
    return (
      <Card className="animate-pulse gap-3 py-4">
        <CardHeader className="px-4 pb-0">
          <div className="h-4 w-40 rounded bg-muted" />
        </CardHeader>
        <CardContent className="space-y-2 px-4">
          <div className="h-3 w-3/4 rounded bg-muted" />
          <div className="h-3 w-1/2 rounded bg-muted" />
        </CardContent>
      </Card>
    );
  }

  if (!brief) return null;

  return (
    <Card className="gap-3 border-primary/15 py-4">
      <CardHeader className="px-4 pb-0 sm:px-5">
        <div className="flex flex-wrap items-start justify-between gap-2">
          <div className="space-y-1">
            <div className="flex items-center gap-2 text-xs font-medium text-muted-foreground">
              <Newspaper className="h-3.5 w-3.5 text-primary" />
              Your brief
              <Badge variant="secondary" className="text-[10px]">{formatWindow(brief)}</Badge>
            </div>
            <CardTitle className="text-base leading-snug">{brief.summary}</CardTitle>
          </div>
          <div className="flex shrink-0 items-center gap-1">
            <Button
              variant="ghost"
              size="icon-sm"
              title="Mark as read"
              onClick={() => setStatus("read")}
            >
              <Check className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="icon-sm"
              title="Dismiss"
              onClick={() => setStatus("dismiss")}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent className="flex flex-wrap items-center gap-2 px-4 sm:px-5">
        {brief.sections.map((section) => (
          <Badge key={section.title} variant="outline" className="text-[11px] font-normal">
            {section.title}
          </Badge>
        ))}
        <Button variant="ghost" size="sm" className="ml-auto gap-1" asChild>
          <Link href="/brief">
            Read brief <ArrowRight className="h-3.5 w-3.5" />
          </Link>
        </Button>
      </CardContent>
    </Card>
  );
}
