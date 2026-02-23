"use client";

import { useEffect, useState, useCallback } from "react";
import { useToken } from "@/hooks/useToken";
import { ChatInterface } from "@/components/ChatInterface";
import { apiFetch } from "@/lib/api";
import type { BriefingResponse } from "@/types/briefing";

export default function HomePage() {
  const token = useToken();
  const [briefing, setBriefing] = useState<BriefingResponse | null>(null);
  const [needsOnboarding, setNeedsOnboarding] = useState<boolean | null>(null);

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
        !settingsRes.value.llm_api_key_set
      ) {
        setNeedsOnboarding(true);
      } else {
        setNeedsOnboarding(false);
      }
    });

    return () => {
      cancelled = true;
    };
  }, [token, loadBriefing]);

  const handleRefresh = () => {
    if (!token) return;
    setNeedsOnboarding(false);
    loadBriefing(token);
  };

  // Wait for settings check before rendering
  if (!token || needsOnboarding === null) return null;

  return (
    <div className="h-full flex flex-col">
      <ChatInterface
        token={token}
        briefing={briefing}
        onRefresh={handleRefresh}
        onboardingMode={needsOnboarding}
      />
    </div>
  );
}
