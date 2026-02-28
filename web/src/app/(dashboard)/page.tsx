"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { useToken } from "@/hooks/useToken";
import { BriefingPanel } from "@/components/BriefingPanel";
import { ChatSheet } from "@/components/ChatSheet";
import { Brain, Send } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { apiFetch } from "@/lib/api";
import { buildSuggestionChips, getGreeting } from "@/components/BriefingPanel";
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
  const [inlineChatQuestion, setInlineChatQuestion] = useState<string | null>(null);
  const [input, setInput] = useState("");

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

  const handleAsk = useCallback((text: string) => {
    setInlineChatQuestion(text);
  }, []);

  const handleSubmit = useCallback(() => {
    if (!input.trim()) return;
    handleAsk(input.trim());
    setInput("");
  }, [input, handleAsk]);

  // Wait for settings check before rendering
  if (!token || needsOnboarding === null) return null;

  const showBriefing = briefing?.has_data;

  return (
    <div className="h-full overflow-y-auto px-4 py-4">
      {showBriefing && briefing && (
        <BriefingPanel
          briefing={briefing}
          onChipClick={handleAsk}
          token={token}
          userName={userName}
        />
      )}

      {!showBriefing && (
        <div className="mx-auto max-w-2xl flex flex-col items-center justify-center py-16 text-center">
          <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-muted">
            <Brain className="h-7 w-7 text-muted-foreground" />
          </div>
          <h3 className="text-lg font-medium">
            {userName ? `${getGreeting()}, ${userName}` : getGreeting()}
          </h3>
          <p className="mt-1 max-w-md text-sm text-muted-foreground">
            Ask me anything — a decision, a priority, a goal, or what to do next.
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-2">
            {buildSuggestionChips(briefing).map((chip) => (
              <button
                key={chip}
                onClick={() => handleAsk(chip)}
                className="rounded-full border px-3 py-1.5 text-xs hover:bg-accent transition-colors"
              >
                {chip}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Always-visible ask input */}
      <div className="mx-auto max-w-2xl mt-4 mb-4">
        <div className="flex gap-2">
          <Textarea
            rows={1}
            placeholder="Ask anything..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSubmit();
              }
            }}
            className="flex-1 resize-none"
          />
          <Button onClick={handleSubmit} disabled={!input.trim()}>
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Chat Sheet — slides in from right */}
      {token && (
        <ChatSheet
          token={token}
          open={!!inlineChatQuestion}
          initialQuestion={inlineChatQuestion}
          onOpenChange={(open) => {
            if (!open) setInlineChatQuestion(null);
          }}
        />
      )}
    </div>
  );
}
