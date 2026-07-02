"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { CalendarDays, Check, ExternalLink, Loader2, Mail, Plus, RefreshCcw, Trash2, X } from "lucide-react";
import { toast } from "sonner";

import { BriefMarkdown } from "@/components/brief/BriefMarkdown";
import { DashboardPageContainer } from "@/components/DashboardPageContainer";
import { WorkspacePageHeader } from "@/components/WorkspacePageHeader";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";
import { useToken } from "@/hooks/useToken";
import { apiFetch } from "@/lib/api";
import type { Brief, BriefConfig, BriefCustomSection, GoogleStatus } from "@/types/brief";

const STATUS_BADGE: Record<string, string> = {
  unread: "bg-primary/10 text-primary",
  read: "",
  dismissed: "opacity-60",
};

function formatRange(brief: Brief): string {
  const opts: Intl.DateTimeFormatOptions = { month: "short", day: "numeric" };
  const start = new Date(brief.period_start).toLocaleDateString(undefined, opts);
  const end = new Date(brief.period_end).toLocaleDateString(undefined, opts);
  return start === end ? end : `${start} – ${end}`;
}

const DEFAULT_CONFIG: BriefConfig = {
  enabled: true,
  min_interval_hours: 12,
  include_signals: true,
  include_journal: true,
  include_calendar: true,
  include_email: true,
  max_items_per_section: 8,
  custom_sections: [],
};

export default function BriefPage() {
  const token = useToken();
  const router = useRouter();
  const searchParams = useSearchParams();
  const [briefs, setBriefs] = useState<Brief[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [config, setConfig] = useState<BriefConfig>(DEFAULT_CONFIG);
  const [google, setGoogle] = useState<GoogleStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [savingConfig, setSavingConfig] = useState(false);

  const load = useCallback(async () => {
    if (!token) return;
    try {
      const [history, cfg, googleStatus] = await Promise.all([
        apiFetch<Brief[]>("/api/v1/brief?limit=30", {}, token),
        apiFetch<BriefConfig>("/api/v1/brief/config", {}, token),
        apiFetch<GoogleStatus>("/api/v1/google/status", {}, token).catch(() => null),
      ]);
      setBriefs(history);
      setConfig(cfg);
      setGoogle(googleStatus);
      setSelectedId((current) => current ?? history[0]?.id ?? null);
    } catch (error) {
      toast.error((error as Error).message);
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    void load();
  }, [load]);

  // Toast once after returning from the Google consent flow, then clean the URL.
  useEffect(() => {
    const result = searchParams.get("google");
    if (!result) return;
    if (result === "connected") {
      toast.success("Google connected — calendar and inbox will appear in your next brief");
    } else {
      toast.error("Google connection failed. Try again.");
    }
    router.replace("/brief");
  }, [searchParams, router]);

  const connectGoogle = useCallback(async () => {
    if (!token) return;
    try {
      const { url } = await apiFetch<{ url: string }>("/api/v1/google/auth-url", {}, token);
      window.location.href = url;
    } catch (error) {
      toast.error((error as Error).message);
    }
  }, [token]);

  const disconnectGoogle = useCallback(async () => {
    if (!token) return;
    try {
      await apiFetch("/api/v1/google/disconnect", { method: "POST" }, token);
      setGoogle((prev) => (prev ? { ...prev, connected: false, email: null } : prev));
      toast.success("Google disconnected");
    } catch (error) {
      toast.error((error as Error).message);
    }
  }, [token]);

  const selected = briefs.find((b) => b.id === selectedId) ?? null;

  const generateNow = useCallback(async () => {
    if (!token || generating) return;
    setGenerating(true);
    try {
      const fresh = await apiFetch<Brief>(
        "/api/v1/brief/generate?force=true",
        { method: "POST" },
        token
      );
      setBriefs((prev) => [fresh, ...prev.filter((b) => b.id !== fresh.id)]);
      setSelectedId(fresh.id);
      toast.success("Brief generated");
    } catch (error) {
      toast.error((error as Error).message);
    } finally {
      setGenerating(false);
    }
  }, [token, generating]);

  const setStatus = useCallback(
    async (brief: Brief, action: "read" | "dismiss") => {
      if (!token) return;
      try {
        await apiFetch(`/api/v1/brief/${brief.id}/${action}`, { method: "POST" }, token);
        setBriefs((prev) =>
          prev.map((b) =>
            b.id === brief.id ? { ...b, status: action === "read" ? "read" : "dismissed" } : b
          )
        );
      } catch (error) {
        toast.error((error as Error).message);
      }
    },
    [token]
  );

  const saveConfig = useCallback(async () => {
    if (!token) return;
    setSavingConfig(true);
    try {
      const saved = await apiFetch<BriefConfig>(
        "/api/v1/brief/config",
        { method: "PUT", body: JSON.stringify(config) },
        token
      );
      setConfig(saved);
      toast.success("Brief settings saved");
    } catch (error) {
      toast.error((error as Error).message);
    } finally {
      setSavingConfig(false);
    }
  }, [token, config]);

  const updateCustomSection = (index: number, patch: Partial<BriefCustomSection>) => {
    setConfig((prev) => ({
      ...prev,
      custom_sections: prev.custom_sections.map((section, i) =>
        i === index ? { ...section, ...patch } : section
      ),
    }));
  };

  if (loading) {
    return (
      <DashboardPageContainer className="animate-pulse space-y-4 py-6">
        <div className="h-28 rounded-2xl bg-muted" />
        <div className="h-64 rounded-2xl bg-muted" />
      </DashboardPageContainer>
    );
  }

  return (
    <DashboardPageContainer className="space-y-6 py-4 md:py-6">
      <WorkspacePageHeader
        eyebrow="Digest"
        title="Brief"
        description="A configurable digest of what changed in your sources, what your journal is telling you, and the standing topics you always want covered."
        actions={
          <Button size="sm" onClick={() => void generateNow()} disabled={generating}>
            {generating ? (
              <Loader2 className="mr-1.5 h-3.5 w-3.5 animate-spin" />
            ) : (
              <RefreshCcw className="mr-1.5 h-3.5 w-3.5" />
            )}
            Generate now
          </Button>
        }
      />

      <section className="grid gap-4 lg:grid-cols-[minmax(280px,0.8fr)_minmax(0,1.6fr)]">
        {/* History */}
        <Card className="gap-3 self-start py-4">
          <CardHeader className="px-4 pb-0">
            <CardTitle className="text-base">Past briefs</CardTitle>
          </CardHeader>
          <CardContent className="space-y-1 px-2">
            {briefs.length === 0 ? (
              <p className="px-2 py-4 text-sm text-muted-foreground">
                No briefs yet. Generate your first one.
              </p>
            ) : (
              briefs.map((brief) => (
                <button
                  key={brief.id}
                  onClick={() => setSelectedId(brief.id)}
                  className={`flex w-full flex-col gap-1 rounded-xl px-3 py-2 text-left transition-colors ${
                    brief.id === selectedId ? "bg-accent" : "hover:bg-accent/50"
                  } ${STATUS_BADGE[brief.status] ?? ""}`}
                >
                  <span className="flex items-center justify-between gap-2 text-sm font-medium">
                    {formatRange(brief)}
                    {brief.status !== "read" ? (
                      <Badge variant={brief.status === "unread" ? "default" : "secondary"} className="text-[10px]">
                        {brief.status}
                      </Badge>
                    ) : null}
                  </span>
                  <span className="line-clamp-2 text-xs text-muted-foreground">{brief.summary}</span>
                </button>
              ))
            )}
          </CardContent>
        </Card>

        {/* Selected brief */}
        <div className="space-y-4">
          {selected ? (
            <Card className="gap-4 py-5">
              <CardHeader className="px-5 pb-0">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div className="space-y-1">
                    <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-muted-foreground">
                      {formatRange(selected)}
                    </p>
                    <CardTitle className="text-lg leading-snug">{selected.summary}</CardTitle>
                  </div>
                  {selected.status !== "dismissed" ? (
                    <div className="flex shrink-0 gap-1.5">
                      {selected.status === "unread" ? (
                        <Button size="sm" variant="outline" onClick={() => void setStatus(selected, "read")}>
                          <Check className="mr-1 h-3.5 w-3.5" /> Mark read
                        </Button>
                      ) : null}
                      <Button size="sm" variant="ghost" onClick={() => void setStatus(selected, "dismiss")}>
                        <X className="mr-1 h-3.5 w-3.5" /> Dismiss
                      </Button>
                    </div>
                  ) : (
                    <Badge variant="secondary">dismissed</Badge>
                  )}
                </div>
              </CardHeader>
              <CardContent className="space-y-6 px-5">
                {selected.sections.map((section, index) => (
                  <div key={`${section.kind}-${index}`} className="space-y-2">
                    <div className="flex items-center gap-2">
                      <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">
                        {section.title}
                      </h2>
                      {section.researched ? (
                        <Badge variant="secondary" className="text-[10px]">web-researched</Badge>
                      ) : null}
                    </div>
                    <BriefMarkdown content={section.body} />
                    {section.sources?.length ? (
                      <div className="flex flex-wrap gap-2 pt-1">
                        {section.sources.map((source) => (
                          <a
                            key={source.url}
                            href={source.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1 rounded-full border px-2.5 py-1 text-xs text-muted-foreground transition-colors hover:text-foreground"
                          >
                            <ExternalLink className="h-3 w-3" />
                            {source.title || source.url}
                          </a>
                        ))}
                      </div>
                    ) : null}
                  </div>
                ))}
              </CardContent>
            </Card>
          ) : (
            <Card className="py-10">
              <CardContent className="text-center text-sm text-muted-foreground">
                Generate a brief to see it here.
              </CardContent>
            </Card>
          )}
        </div>
      </section>

      {/* Configuration */}
      <Card className="gap-4 py-5">
        <CardHeader className="px-5 pb-0">
          <CardTitle className="text-base">Brief settings</CardTitle>
        </CardHeader>
        <CardContent className="space-y-5 px-5">
          {google?.available ? (
            <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border p-3">
              <div className="flex items-center gap-3">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
                  <CalendarDays className="h-4 w-4 text-primary" />
                </div>
                <div>
                  <p className="text-sm font-medium">Google Calendar &amp; Gmail</p>
                  <p className="text-xs text-muted-foreground">
                    {google.connected
                      ? `Connected as ${google.email ?? "your Google account"} (read-only)`
                      : "Connect to plan your day and watch important email in each brief."}
                  </p>
                </div>
              </div>
              {google.connected ? (
                <Button size="sm" variant="outline" onClick={() => void disconnectGoogle()}>
                  Disconnect
                </Button>
              ) : (
                <Button size="sm" onClick={() => void connectGoogle()}>
                  Connect Google
                </Button>
              )}
            </div>
          ) : null}

          <div className="grid gap-4 sm:grid-cols-3">
            <div className="flex items-center justify-between gap-3 rounded-xl border p-3 sm:flex-col sm:items-start">
              <Label htmlFor="brief-signals" className="text-sm">What changed (sources)</Label>
              <Switch
                id="brief-signals"
                checked={config.include_signals}
                onCheckedChange={(checked) => setConfig((prev) => ({ ...prev, include_signals: checked }))}
              />
            </div>
            <div className="flex items-center justify-between gap-3 rounded-xl border p-3 sm:flex-col sm:items-start">
              <Label htmlFor="brief-journal" className="text-sm">From your journal</Label>
              <Switch
                id="brief-journal"
                checked={config.include_journal}
                onCheckedChange={(checked) => setConfig((prev) => ({ ...prev, include_journal: checked }))}
              />
            </div>
            <div className="flex items-center justify-between gap-3 rounded-xl border p-3 sm:flex-col sm:items-start">
              <Label htmlFor="brief-interval" className="text-sm">Hours between briefs</Label>
              <Input
                id="brief-interval"
                type="number"
                min={1}
                max={168}
                className="h-8 w-24"
                value={config.min_interval_hours}
                onChange={(event) =>
                  setConfig((prev) => ({
                    ...prev,
                    min_interval_hours: Math.max(1, Math.min(168, Number(event.target.value) || 12)),
                  }))
                }
              />
            </div>
          </div>

          {google?.connected ? (
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="flex items-center justify-between gap-3 rounded-xl border p-3">
                <Label htmlFor="brief-calendar" className="flex items-center gap-2 text-sm">
                  <CalendarDays className="h-4 w-4 text-muted-foreground" />
                  Coming up (calendar)
                </Label>
                <Switch
                  id="brief-calendar"
                  checked={config.include_calendar}
                  onCheckedChange={(checked) => setConfig((prev) => ({ ...prev, include_calendar: checked }))}
                />
              </div>
              <div className="flex items-center justify-between gap-3 rounded-xl border p-3">
                <Label htmlFor="brief-email" className="flex items-center gap-2 text-sm">
                  <Mail className="h-4 w-4 text-muted-foreground" />
                  Inbox watch (email)
                </Label>
                <Switch
                  id="brief-email"
                  checked={config.include_email}
                  onCheckedChange={(checked) => setConfig((prev) => ({ ...prev, include_email: checked }))}
                />
              </div>
            </div>
          ) : null}

          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium">Standing sections</p>
                <p className="text-xs text-muted-foreground">
                  Instructions every brief follows — e.g. &ldquo;always include a well-researched summary of an esoteric but important topic&rdquo;.
                </p>
              </div>
              <Button
                size="sm"
                variant="outline"
                onClick={() =>
                  setConfig((prev) => ({
                    ...prev,
                    custom_sections: [
                      ...prev.custom_sections,
                      { id: "", title: "", instructions: "", use_research: true },
                    ],
                  }))
                }
              >
                <Plus className="mr-1 h-3.5 w-3.5" /> Add
              </Button>
            </div>

            {config.custom_sections.map((section, index) => (
              <div key={section.id || `new-${index}`} className="space-y-2 rounded-xl border p-3">
                <div className="flex items-center gap-2">
                  <Input
                    placeholder="Section title (optional)"
                    value={section.title}
                    className="h-8"
                    onChange={(event) => updateCustomSection(index, { title: event.target.value })}
                  />
                  <div className="flex shrink-0 items-center gap-2">
                    <Label htmlFor={`research-${index}`} className="text-xs text-muted-foreground">
                      Web research
                    </Label>
                    <Switch
                      id={`research-${index}`}
                      checked={section.use_research}
                      onCheckedChange={(checked) => updateCustomSection(index, { use_research: checked })}
                    />
                    <Button
                      variant="ghost"
                      size="icon-sm"
                      title="Remove section"
                      onClick={() =>
                        setConfig((prev) => ({
                          ...prev,
                          custom_sections: prev.custom_sections.filter((_, i) => i !== index),
                        }))
                      }
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                </div>
                <Textarea
                  placeholder="Standing instruction, e.g. 'Always include a well-researched summary of an esoteric but important topic I might find interesting.'"
                  value={section.instructions}
                  rows={2}
                  onChange={(event) => updateCustomSection(index, { instructions: event.target.value })}
                />
              </div>
            ))}
          </div>

          <div className="flex justify-end">
            <Button size="sm" onClick={() => void saveConfig()} disabled={savingConfig}>
              {savingConfig ? <Loader2 className="mr-1.5 h-3.5 w-3.5 animate-spin" /> : null}
              Save settings
            </Button>
          </div>
        </CardContent>
      </Card>
    </DashboardPageContainer>
  );
}
