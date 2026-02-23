"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import ReactMarkdown from "react-markdown";
import { ExternalLink, Rocket, Lightbulb, Loader2 } from "lucide-react";
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
import { Separator } from "@/components/ui/separator";
import type { MatchingIssue } from "@/types/projects";

const DAYS_OPTIONS = [7, 14, 30] as const;

function IssueSkeleton() {
  return (
    <Card>
      <CardHeader className="pb-2">
        <div className="h-4 w-3/4 animate-pulse rounded bg-muted" />
        <div className="h-3 w-1/3 animate-pulse rounded bg-muted" />
      </CardHeader>
      <CardContent>
        <div className="h-3 w-full animate-pulse rounded bg-muted" />
      </CardContent>
    </Card>
  );
}

export default function ProjectsPage() {
  const token = useToken();
  const [issues, setIssues] = useState<MatchingIssue[]>([]);
  const [issuesLoading, setIssuesLoading] = useState(true);
  const [days, setDays] = useState<number>(14);
  const [ideas, setIdeas] = useState<string | null>(null);
  const [ideasLoading, setIdeasLoading] = useState(false);
  const [hasKey, setHasKey] = useState(true);

  useEffect(() => {
    if (!token) {
      setIssuesLoading(false);
      return;
    }
    setIssuesLoading(true);
    apiFetch<MatchingIssue[]>(
      `/api/projects/issues?days=${days}&limit=20`,
      {},
      token
    )
      .then(setIssues)
      .catch((e) => toast.error(e.message))
      .finally(() => setIssuesLoading(false));
  }, [token, days]);

  useEffect(() => {
    if (!token) return;
    apiFetch<{ llm_api_key_set: boolean }>("/api/settings", {}, token)
      .then((s) => setHasKey(s.llm_api_key_set))
      .catch(() => {});
  }, [token]);

  const handleGenerateIdeas = async () => {
    if (!token) return;
    setIdeasLoading(true);
    try {
      const res = await apiFetch<{ ideas: string }>(
        "/api/projects/ideas",
        { method: "POST" },
        token
      );
      setIdeas(res.ideas);
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setIdeasLoading(false);
    }
  };

  const noData = !issuesLoading && issues.length === 0 && !ideas;

  return (
    <div className="space-y-6 p-6">
      <h1 className="text-2xl font-semibold">Projects</h1>

      {noData && (
        <div className="flex flex-col items-center justify-center py-16 text-center">
          <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-muted">
            <Rocket className="h-7 w-7 text-muted-foreground" />
          </div>
          <h3 className="text-lg font-medium">No project data yet</h3>
          <p className="mt-1 max-w-sm text-sm text-muted-foreground">
            Run the scraper from the Intel page to find matching GitHub issues,
            or generate project ideas below.
          </p>
        </div>
      )}

      {/* Matching Issues */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-medium">Matching Issues</h2>
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
        </div>

        {issuesLoading && (
          <div className="space-y-3">
            {Array.from({ length: 3 }).map((_, i) => (
              <IssueSkeleton key={i} />
            ))}
          </div>
        )}

        {!issuesLoading && issues.length === 0 && (
          <p className="text-sm text-muted-foreground">
            No GitHub issues found for this time range.
          </p>
        )}

        {!issuesLoading && issues.length > 0 && (
          <div className="space-y-3">
            {issues.map((issue, i) => (
              <Card key={i}>
                <CardHeader className="pb-2">
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-base">
                        <a
                          href={issue.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="hover:underline"
                        >
                          {issue.title}
                          <ExternalLink className="ml-1 inline h-3 w-3" />
                        </a>
                      </CardTitle>
                      <CardDescription className="flex items-center gap-2">
                        <Badge variant="outline">{issue.source}</Badge>
                        {issue.match_score > 0 && (
                          <Badge variant="secondary">
                            match: {issue.match_score}
                          </Badge>
                        )}
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground line-clamp-3">
                    {issue.summary}
                  </p>
                  {issue.tags.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-1">
                      {issue.tags
                        .filter((t) => t.trim())
                        .map((t) => (
                          <Badge
                            key={t}
                            variant="secondary"
                            className="text-xs"
                          >
                            {t.trim()}
                          </Badge>
                        ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </section>

      <Separator />

      {/* Project Ideas */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-medium">Project Ideas</h2>
          <Button
            onClick={handleGenerateIdeas}
            disabled={ideasLoading || !hasKey}
          >
            {ideasLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Lightbulb className="mr-2 h-4 w-4" />
                Generate Ideas
              </>
            )}
          </Button>
        </div>

        {!hasKey && (
          <p className="text-sm text-muted-foreground">
            Set an LLM API key in Settings to generate ideas.
          </p>
        )}

        {ideas && (
          <Card>
            <CardContent className="pt-6">
              <div className="prose prose-sm dark:prose-invert max-w-none">
                <ReactMarkdown>{ideas}</ReactMarkdown>
              </div>
            </CardContent>
          </Card>
        )}

        {!ideas && !ideasLoading && hasKey && (
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Lightbulb className="h-4 w-4" />
            Click Generate to get side-project ideas based on your journal entries.
          </div>
        )}
      </section>
    </div>
  );
}
