"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { useToken } from "@/hooks/useToken";
import { ChatInterface } from "@/components/ChatInterface";
import { apiFetch } from "@/lib/api";
import type { BriefingResponse } from "@/types/briefing";

interface ProfileStatus {
  has_profile: boolean;
  is_stale: boolean;
  has_api_key: boolean;
}

export default function HomePage() {
  const token = useToken();
  const router = useRouter();
  const [briefing, setBriefing] = useState<BriefingResponse | null>(null);
  const [needsOnboarding, setNeedsOnboarding] = useState<boolean | null>(null);
  const [userName, setUserName] = useState<string | null>(null);

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
      apiFetch<ProfileStatus>("/api/onboarding/profile-status", {}, token),
      apiFetch<{ name: string | null }>("/api/user/me", {}, token),
    ]).then(([, settingsRes, profileRes, userRes]) => {
      if (cancelled) return;

      const noApiKey =
        settingsRes.status === "fulfilled" &&
        !settingsRes.value.llm_api_key_set;
      const noProfile =
        profileRes.status === "fulfilled" &&
        !profileRes.value.has_profile;

      if (noApiKey || noProfile) {
        router.replace("/onboarding");
        return;
      }

      if (userRes.status === "fulfilled" && userRes.value.name) {
        setUserName(userRes.value.name);
      }
      setNeedsOnboarding(false);
    });

    return () => {
      cancelled = true;
    };
  }, [token, loadBriefing, router]);

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
        onboardingMode={false}
        userName={userName}
      />
    </div>
  );
}
