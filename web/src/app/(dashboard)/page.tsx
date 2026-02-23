"use client";

import { useEffect, useState, useCallback } from "react";
import { toast } from "sonner";
import { RefreshCw } from "lucide-react";
import { useToken } from "@/hooks/useToken";
import { OnboardingDialog } from "@/components/OnboardingDialog";
import {
  SignalsCard,
  PatternsCard,
  RecommendationsCard,
  StaleGoalsCard,
} from "@/components/DailyBrief";
import { EmbeddedAdvisor } from "@/components/EmbeddedAdvisor";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";
import type { BriefingResponse } from "@/types/briefing";

export default function BriefPage() {
  const token = useToken();
  const [briefing, setBriefing] = useState<BriefingResponse | null>(null);
  const [loading, setLoading] = useState(!!token);
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [prefillQuestion, setPrefillQuestion] = useState<string | undefined>();

  const loadBriefing = useCallback(
    async (t: string) => {
      try {
        const data = await apiFetch<BriefingResponse>("/api/briefing", {}, t);
        setBriefing(data);
      } catch {
        // silent — cards just won't render
      }
    },
    []
  );

  useEffect(() => {
    if (!token) return;
    let cancelled = false;

    Promise.allSettled([
      loadBriefing(token),
      apiFetch<{ llm_api_key_set: boolean }>("/api/settings", {}, token),
    ]).then(([, settingsRes]) => {
      if (cancelled) return;
      if (
        settingsRes.status === "fulfilled" &&
        !settingsRes.value.llm_api_key_set &&
        !localStorage.getItem("onboarding_dismissed")
      ) {
        setShowOnboarding(true);
      }
      setLoading(false);
    });

    return () => {
      cancelled = true;
    };
  }, [token, loadBriefing]);

  const handleRefresh = () => {
    if (!token) return;
    setLoading(true);
    loadBriefing(token).finally(() => setLoading(false));
  };

  const handleDismissSignal = async (signalId: number) => {
    if (!token) return;
    try {
      await apiFetch(`/api/briefing/signals/${signalId}/acknowledge`, { method: "POST" }, token);
      setBriefing((prev) =>
        prev
          ? {
              ...prev,
              signals: prev.signals.filter((s) => s.id !== signalId),
            }
          : prev
      );
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  const handleAskAbout = (question: string) => {
    setPrefillQuestion(question);
  };

  const dismissOnboarding = () => {
    localStorage.setItem("onboarding_dismissed", "true");
    setShowOnboarding(false);
  };

  const today = new Date().toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return (
    <div className="space-y-6">
      {token && (
        <OnboardingDialog
          open={showOnboarding}
          onClose={dismissOnboarding}
          onComplete={handleRefresh}
          token={token}
        />
      )}

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Daily Brief</h1>
          <p className="text-sm text-muted-foreground">{today}</p>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={handleRefresh}
          disabled={loading}
        >
          <RefreshCw className={`mr-1 h-4 w-4 ${loading ? "animate-spin" : ""}`} />
          Refresh
        </Button>
      </div>

      {/* Brief cards */}
      {loading && !briefing ? (
        <div className="grid gap-4 md:grid-cols-2">
          {[1, 2, 3, 4].map((i) => (
            <div
              key={i}
              className="h-32 animate-pulse rounded-lg border bg-muted"
            />
          ))}
        </div>
      ) : briefing && briefing.has_data ? (
        <div className="grid gap-4 md:grid-cols-2">
          <SignalsCard
            signals={briefing.signals}
            onAskAbout={handleAskAbout}
            onDismiss={handleDismissSignal}
          />
          <PatternsCard
            patterns={briefing.patterns}
            onAskAbout={handleAskAbout}
          />
          <RecommendationsCard
            recommendations={briefing.recommendations}
            onAskAbout={handleAskAbout}
          />
          <StaleGoalsCard
            goals={briefing.stale_goals}
            onAskAbout={handleAskAbout}
          />
        </div>
      ) : (
        !loading && (
          <div className="rounded-lg border border-dashed p-8 text-center">
            <p className="text-sm text-muted-foreground">
              No briefing data yet. Use the advisor chat below, write journal
              entries, and run the scheduler to populate signals and patterns.
            </p>
          </div>
        )
      )}

      {/* Embedded advisor */}
      {token && (
        <EmbeddedAdvisor
          token={token}
          prefillQuestion={prefillQuestion}
          onQuestionConsumed={() => setPrefillQuestion(undefined)}
        />
      )}
    </div>
  );
}
