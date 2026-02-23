"use client";

import { useEffect, useState, useCallback } from "react";
import { useToken } from "@/hooks/useToken";
import { OnboardingDialog } from "@/components/OnboardingDialog";
import { ChatInterface } from "@/components/ChatInterface";
import { apiFetch } from "@/lib/api";
import type { BriefingResponse } from "@/types/briefing";

export default function HomePage() {
  const token = useToken();
  const [briefing, setBriefing] = useState<BriefingResponse | null>(null);
  const [showOnboarding, setShowOnboarding] = useState(false);

  const loadBriefing = useCallback(
    async (t: string) => {
      try {
        const data = await apiFetch<BriefingResponse>("/api/briefing", {}, t);
        setBriefing(data);
      } catch {
        // silent
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
    });

    return () => {
      cancelled = true;
    };
  }, [token, loadBriefing]);

  const handleRefresh = () => {
    if (!token) return;
    loadBriefing(token);
  };

  const dismissOnboarding = () => {
    localStorage.setItem("onboarding_dismissed", "true");
    setShowOnboarding(false);
  };

  return (
    <div className="h-full flex flex-col">
      {token && (
        <OnboardingDialog
          open={showOnboarding}
          onClose={dismissOnboarding}
          onComplete={handleRefresh}
          token={token}
        />
      )}
      {token && (
        <ChatInterface
          token={token}
          briefing={briefing}
          onRefresh={handleRefresh}
        />
      )}
    </div>
  );
}
