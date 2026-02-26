"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { useToken } from "@/hooks/useToken";
import {
  ChevronDown,
  ChevronRight,
  ExternalLink,
  Heart,
  Newspaper,
  RefreshCw,
  Search,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { apiFetch } from "@/lib/api";

interface IntelItem {
  source: string;
  title: string;
  url: string;
  summary: string;
  published?: string;
  tags?: string[];
}

interface ScraperHealth {
  source: string;
  last_run_at: string | null;
  last_success_at: string | null;
  consecutive_errors: number;
  total_runs: number;
  total_errors: number;
  last_error: string | null;
  backoff_until: string | null;
}

function timeAgo(dateStr: string | null): string {
  if (!dateStr) return "never";
  const diff = Date.now() - new Date(dateStr).getTime();
  const hours = Math.floor(diff / 3600000);
  if (hours < 1) return "< 1h ago";
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

function healthColor(h: ScraperHealth): "green" | "yellow" | "red" {
  if (h.consecutive_errors >= 3) return "red";
  if (h.last_success_at) {
    const hoursSinceSuccess =
      (Date.now() - new Date(h.last_success_at).getTime()) / 3600000;
    if (hoursSinceSuccess > 72) return "red";
  } else if (h.total_runs > 0) {
    return "red";
  }
  if (h.consecutive_errors > 0) return "yellow";
  return "green";
}

const dotColors = {
  green: "bg-green-500",
  yellow: "bg-yellow-500",
  red: "bg-red-500",
};

function HealthDashboard({ token }: { token: string }) {
  const [health, setHealth] = useState<ScraperHealth[]>([]);
  const [expanded, setExpanded] = useState(false);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    apiFetch<{ scrapers: ScraperHealth[] }>("/api/intel/health", {}, token)
      .then((d) => setHealth(d.scrapers))
      .catch(() => {})
      .finally(() => setLoaded(true));
  }, [token]);

  if (!loaded || health.length === 0) return null;

  const healthyCount = health.filter((h) => healthColor(h) === "green").length;

  return (
    <Card>
      <CardHeader
        className="cursor-pointer pb-3"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Heart className="h-4 w-4 text-muted-foreground" />
            <CardTitle className="text-base">Source health</CardTitle>
            <Badge variant={healthyCount === health.length ? "secondary" : "destructive"}>
              {healthyCount}/{health.length} healthy
            </Badge>
          </div>
          {expanded ? (
            <ChevronDown className="h-4 w-4 text-muted-foreground" />
          ) : (
            <ChevronRight className="h-4 w-4 text-muted-foreground" />
          )}
        </div>
      </CardHeader>
      {expanded && (
        <CardContent>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {health.map((h) => {
              const color = healthColor(h);
              return (
                <div
                  key={h.source}
                  className="rounded-lg border p-3 text-sm"
                >
                  <div className="flex items-center gap-2">
                    <span className={`h-2.5 w-2.5 rounded-full ${dotColors[color]}`} />
                    <span className="font-medium">{h.source}</span>
                  </div>
                  <div className="mt-2 space-y-0.5 text-xs text-muted-foreground">
                    <p>Last scan: {timeAgo(h.last_success_at)}</p>
                    <p>
                      Runs: {h.total_runs} | Errors: {h.total_errors}
                    </p>
                    {h.last_error && (
                      <p className="truncate text-red-500" title={h.last_error}>
                        {h.last_error.slice(0, 80)}
                      </p>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      )}
    </Card>
  );
}

function IntelSkeleton() {
  return (
    <Card>
      <CardHeader className="pb-2">
        <div className="h-4 w-3/4 animate-pulse rounded bg-muted" />
        <div className="flex gap-2">
          <div className="h-5 w-16 animate-pulse rounded bg-muted" />
          <div className="h-4 w-20 animate-pulse rounded bg-muted" />
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-1.5">
          <div className="h-3 w-full animate-pulse rounded bg-muted" />
          <div className="h-3 w-2/3 animate-pulse rounded bg-muted" />
        </div>
      </CardContent>
    </Card>
  );
}

export default function IntelPage() {
  const token = useToken();
  const [items, setItems] = useState<IntelItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");
  const [scraping, setScraping] = useState(false);

  const loadRecent = () => {
    if (!token) {
      setLoading(false);
      return;
    }
    apiFetch<IntelItem[]>("/api/intel/recent?limit=50", {}, token)
      .then(setItems)
      .catch((e) => toast.error(e.message))
      .finally(() => setLoading(false));
  };

  useEffect(loadRecent, [token]);

  const handleSearch = async () => {
    if (!token || !query.trim()) {
      loadRecent();
      return;
    }
    setLoading(true);
    try {
      const results = await apiFetch<IntelItem[]>(
        `/api/intel/search?q=${encodeURIComponent(query)}&limit=20`,
        {},
        token
      );
      setItems(results);
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleScrape = async () => {
    if (!token) return;
    setScraping(true);
    try {
      await apiFetch("/api/intel/scrape", { method: "POST" }, token);
      toast.success("Scrape completed");
      loadRecent();
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setScraping(false);
    }
  };

  return (
    <div className="space-y-6 p-4 md:p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Radar</h1>
        <Button
          variant="outline"
          onClick={handleScrape}
          disabled={scraping}
        >
          <RefreshCw className={`mr-2 h-4 w-4 ${scraping ? "animate-spin" : ""}`} />
          {scraping ? "Scanning..." : "Scan Now"}
        </Button>
      </div>

      {/* Scraper Health */}
      {token && <HealthDashboard token={token} />}

      {/* Search */}
      <div className="flex gap-2">
        <Input
          placeholder="Search your radar..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          className="max-w-md"
        />
        <Button variant="outline" onClick={handleSearch}>
          <Search className="h-4 w-4" />
        </Button>
      </div>

      {/* Loading */}
      {loading && (
        <div className="space-y-3">
          {Array.from({ length: 5 }).map((_, i) => (
            <IntelSkeleton key={i} />
          ))}
        </div>
      )}

      {/* Empty state */}
      {!loading && items.length === 0 && (
        <div className="flex flex-col items-center justify-center py-16 text-center">
          <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-muted">
            <Newspaper className="h-7 w-7 text-muted-foreground" />
          </div>
          <h3 className="text-lg font-medium">Your radar is quiet</h3>
          <p className="mt-1 max-w-sm text-sm text-muted-foreground">
            I haven&apos;t scanned anything yet. Run a scan to pull in signals from
            Hacker News, GitHub, arXiv, and RSS feeds.
          </p>
          <Button
            variant="outline"
            className="mt-4"
            onClick={handleScrape}
            disabled={scraping}
          >
            <RefreshCw className={`mr-2 h-4 w-4 ${scraping ? "animate-spin" : ""}`} />
            {scraping ? "Scanning..." : "Run First Scan"}
          </Button>
        </div>
      )}

      {/* Items */}
      {!loading && items.length > 0 && (
        <div className="space-y-3">
          {items.map((item, i) => (
            <Card key={i}>
              <CardHeader className="pb-2">
                <div className="flex items-start justify-between">
                  <div>
                    <CardTitle className="text-base">
                      <a
                        href={item.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="hover:underline"
                      >
                        {item.title}
                        <ExternalLink className="ml-1 inline h-3 w-3" />
                      </a>
                    </CardTitle>
                    <CardDescription className="flex items-center gap-2">
                      <Badge variant="outline">{item.source}</Badge>
                      {item.published && (
                        <span>{new Date(item.published).toLocaleDateString()}</span>
                      )}
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">{item.summary}</p>
                {item.tags && item.tags.length > 0 && (
                  <div className="mt-2 flex flex-wrap gap-1">
                    {item.tags.map((t) => (
                      <Badge key={t} variant="secondary" className="text-xs">
                        {t}
                      </Badge>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
