"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { useToken } from "@/hooks/useToken";
import { ExternalLink, RefreshCw, Search } from "lucide-react";
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

export default function IntelPage() {
  const token = useToken();
  const [items, setItems] = useState<IntelItem[]>([]);
  const [query, setQuery] = useState("");
  const [scraping, setScraping] = useState(false);

  const loadRecent = () => {
    if (!token) return;
    apiFetch<IntelItem[]>("/api/intel/recent?limit=50", {}, token)
      .then(setItems)
      .catch((e) => toast.error(e.message));
  };

  useEffect(loadRecent, [token]);

  const handleSearch = async () => {
    if (!token || !query.trim()) {
      loadRecent();
      return;
    }
    try {
      const results = await apiFetch<IntelItem[]>(
        `/api/intel/search?q=${encodeURIComponent(query)}&limit=20`,
        {},
        token
      );
      setItems(results);
    } catch (e) {
      toast.error((e as Error).message);
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
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Intelligence</h1>
        <Button
          variant="outline"
          onClick={handleScrape}
          disabled={scraping}
        >
          <RefreshCw className={`mr-2 h-4 w-4 ${scraping ? "animate-spin" : ""}`} />
          {scraping ? "Scraping..." : "Scrape Now"}
        </Button>
      </div>

      {/* Search */}
      <div className="flex gap-2">
        <Input
          placeholder="Search intelligence..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          className="max-w-md"
        />
        <Button variant="outline" onClick={handleSearch}>
          <Search className="h-4 w-4" />
        </Button>
      </div>

      {/* Items */}
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
        {items.length === 0 && (
          <p className="text-muted-foreground">No intelligence items. Try scraping first.</p>
        )}
      </div>
    </div>
  );
}
