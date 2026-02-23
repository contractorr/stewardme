"use client";

import { useRef, useEffect, useState, useCallback } from "react";
import { toast } from "sonner";
import ReactMarkdown from "react-markdown";
import {
  AlertTriangle,
  Brain,
  Lightbulb,
  Plus,
  Send,
  Target,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
} from "@/components/ui/sheet";
import {
  SignalsCard,
  PatternsCard,
  RecommendationsCard,
  StaleGoalsCard,
} from "@/components/DailyBrief";
import { apiFetch, apiFetchSSE } from "@/lib/api";
import type { BriefingResponse } from "@/types/briefing";

const TOOL_LABELS: Record<string, string> = {
  journal_search: "Searching journal",
  journal_read: "Reading journal entry",
  journal_list: "Listing journal entries",
  goals_list: "Checking goals",
  intel_search: "Searching intel",
  intel_get_recent: "Fetching recent intel",
  profile_get: "Loading profile",
  get_context: "Gathering context",
  recommendations_list: "Checking recommendations",
};

interface Message {
  role: "user" | "assistant";
  content: string;
  isGreeting?: boolean;
}

const CONV_KEY = "main_chat_conv_id";

type SheetType = "signals" | "patterns" | "recommendations" | "goals" | null;

export function ChatInterface({
  token,
  briefing,
  onRefresh,
}: {
  token: string;
  briefing: BriefingResponse | null;
  onRefresh: () => void;
}) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [toolStatus, setToolStatus] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [restoredConv, setRestoredConv] = useState(false);
  const [openSheet, setOpenSheet] = useState<SheetType>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Restore conversation on mount
  useEffect(() => {
    const saved = localStorage.getItem(CONV_KEY);
    if (!saved) {
      setRestoredConv(false);
      return;
    }
    (async () => {
      try {
        const conv = await apiFetch<{
          id: string;
          messages: Message[];
        }>(`/api/advisor/conversations/${saved}`, {}, token);
        setConversationId(saved);
        setMessages(conv.messages);
        setRestoredConv(true);
      } catch {
        localStorage.removeItem(CONV_KEY);
        setRestoredConv(false);
      }
    })();
  }, [token]);

  // Proactive greeting when no conversation and briefing data exists
  useEffect(() => {
    if (messages.length > 0 || restoredConv) return;
    if (!briefing?.has_data) return;

    const parts: string[] = [];
    const hour = new Date().getHours();
    const greeting =
      hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";

    parts.push(`${greeting}! Here's what I noticed today:\n`);

    if (briefing.signals.length > 0)
      parts.push(
        `- **${briefing.signals.length} signal${briefing.signals.length > 1 ? "s" : ""}** need attention`
      );
    if (briefing.patterns.length > 0)
      parts.push(
        `- **${briefing.patterns.length} pattern${briefing.patterns.length > 1 ? "s" : ""}** detected in your journal`
      );
    if (briefing.recommendations.length > 0)
      parts.push(
        `- **${briefing.recommendations.length} recommendation${briefing.recommendations.length > 1 ? "s" : ""}** ready to review`
      );
    if (briefing.stale_goals.length > 0)
      parts.push(
        `- **${briefing.stale_goals.length} stale goal${briefing.stale_goals.length > 1 ? "s" : ""}** could use a check-in`
      );

    parts.push("\nWhat would you like to focus on?");

    setMessages([{ role: "assistant", content: parts.join("\n"), isGreeting: true }]);
  }, [briefing, messages.length, restoredConv]);

  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages, loading]);

  const handleNewChat = () => {
    setConversationId(null);
    setMessages([]);
    setRestoredConv(false);
    localStorage.removeItem(CONV_KEY);
  };

  const handlePrefill = (question: string) => {
    setInput(question);
    setOpenSheet(null);
    setTimeout(() => textareaRef.current?.focus(), 100);
  };

  const handleDismissSignal = async (signalId: number) => {
    try {
      await apiFetch(
        `/api/briefing/signals/${signalId}/acknowledge`,
        { method: "POST" },
        token
      );
      onRefresh();
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  const handleSend = useCallback(async () => {
    if (!input.trim() || loading) return;
    const question = input.trim();
    setInput("");
    // Filter out greeting messages before adding user message
    setMessages((prev) => [
      ...prev.filter((m) => !m.isGreeting),
      { role: "user", content: question },
    ]);
    setLoading(true);
    setToolStatus(null);

    try {
      await apiFetchSSE(
        "/api/advisor/ask/stream",
        {
          method: "POST",
          body: JSON.stringify({
            question,
            advice_type: "general",
            conversation_id: conversationId,
          }),
        },
        token,
        (event) => {
          const type = event.type as string;
          if (type === "tool_start") {
            setToolStatus(
              TOOL_LABELS[event.tool as string] || `Running ${event.tool}`
            );
          } else if (type === "tool_done") {
            setToolStatus(null);
          } else if (type === "answer") {
            const cid = event.conversation_id as string;
            setConversationId(cid);
            localStorage.setItem(CONV_KEY, cid);
            setMessages((prev) => [
              ...prev,
              { role: "assistant", content: event.content as string },
            ]);
          } else if (type === "error") {
            toast.error(event.detail as string);
            setMessages((prev) => [
              ...prev,
              { role: "assistant", content: "Error: " + (event.detail as string) },
            ]);
          }
        }
      );
    } catch (e) {
      toast.error((e as Error).message);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Error: " + (e as Error).message },
      ]);
    } finally {
      setLoading(false);
      setToolStatus(null);
    }
  }, [input, loading, conversationId, token]);

  const hasBadges = briefing?.has_data;

  return (
    <div className="flex h-full flex-col">
      {/* Insight badges */}
      {hasBadges && (
        <div className="flex flex-wrap gap-2 px-4 py-3 border-b">
          {briefing!.signals.length > 0 && (
            <button
              onClick={() => setOpenSheet("signals")}
              className="inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-medium hover:bg-accent transition-colors"
            >
              <AlertTriangle className="h-3 w-3" />
              {briefing!.signals.length} Signal{briefing!.signals.length > 1 ? "s" : ""}
            </button>
          )}
          {briefing!.patterns.length > 0 && (
            <button
              onClick={() => setOpenSheet("patterns")}
              className="inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-medium hover:bg-accent transition-colors"
            >
              <Brain className="h-3 w-3" />
              {briefing!.patterns.length} Pattern{briefing!.patterns.length > 1 ? "s" : ""}
            </button>
          )}
          {briefing!.recommendations.length > 0 && (
            <button
              onClick={() => setOpenSheet("recommendations")}
              className="inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-medium hover:bg-accent transition-colors"
            >
              <Lightbulb className="h-3 w-3" />
              {briefing!.recommendations.length} Rec{briefing!.recommendations.length > 1 ? "s" : ""}
            </button>
          )}
          {briefing!.stale_goals.length > 0 && (
            <button
              onClick={() => setOpenSheet("goals")}
              className="inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-medium hover:bg-accent transition-colors"
            >
              <Target className="h-3 w-3" />
              {briefing!.stale_goals.length} Stale Goal{briefing!.stale_goals.length > 1 ? "s" : ""}
            </button>
          )}
        </div>
      )}

      {/* Sheet overlays for detail cards */}
      <Sheet open={openSheet === "signals"} onOpenChange={(o) => !o && setOpenSheet(null)}>
        <SheetContent>
          <SheetHeader>
            <SheetTitle>Signals</SheetTitle>
            <SheetDescription>Items that need your attention</SheetDescription>
          </SheetHeader>
          <div className="overflow-y-auto px-6 pb-6">
            <SignalsCard
              signals={briefing?.signals ?? []}
              onAskAbout={handlePrefill}
              onDismiss={handleDismissSignal}
            />
          </div>
        </SheetContent>
      </Sheet>
      <Sheet open={openSheet === "patterns"} onOpenChange={(o) => !o && setOpenSheet(null)}>
        <SheetContent>
          <SheetHeader>
            <SheetTitle>Patterns</SheetTitle>
            <SheetDescription>Trends detected in your journal</SheetDescription>
          </SheetHeader>
          <div className="overflow-y-auto px-6 pb-6">
            <PatternsCard patterns={briefing?.patterns ?? []} onAskAbout={handlePrefill} />
          </div>
        </SheetContent>
      </Sheet>
      <Sheet open={openSheet === "recommendations"} onOpenChange={(o) => !o && setOpenSheet(null)}>
        <SheetContent>
          <SheetHeader>
            <SheetTitle>Recommendations</SheetTitle>
            <SheetDescription>Suggested actions based on your data</SheetDescription>
          </SheetHeader>
          <div className="overflow-y-auto px-6 pb-6">
            <RecommendationsCard
              recommendations={briefing?.recommendations ?? []}
              onAskAbout={handlePrefill}
            />
          </div>
        </SheetContent>
      </Sheet>
      <Sheet open={openSheet === "goals"} onOpenChange={(o) => !o && setOpenSheet(null)}>
        <SheetContent>
          <SheetHeader>
            <SheetTitle>Stale Goals</SheetTitle>
            <SheetDescription>Goals that haven&apos;t been checked in recently</SheetDescription>
          </SheetHeader>
          <div className="overflow-y-auto px-6 pb-6">
            <StaleGoalsCard
              goals={briefing?.stale_goals ?? []}
              onAskAbout={handlePrefill}
            />
          </div>
        </SheetContent>
      </Sheet>

      {/* Chat messages */}
      <div ref={scrollRef} className="flex-1 space-y-4 overflow-y-auto px-4 py-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-muted">
              <Brain className="h-7 w-7 text-muted-foreground" />
            </div>
            <h3 className="text-lg font-medium">What&apos;s on your mind?</h3>
            <p className="mt-1 max-w-md text-sm text-muted-foreground">
              Ask a question, write a journal entry, check in on a goal — I&apos;ll figure out the rest.
            </p>
          </div>
        )}
        {messages.map((msg, i) => (
          <Card
            key={i}
            className={msg.role === "user" ? "ml-12 bg-primary/5" : "mr-12"}
          >
            <CardHeader className="pb-2">
              <CardTitle className="text-xs text-muted-foreground">
                {msg.role === "user" ? "You" : "Advisor"}
              </CardTitle>
            </CardHeader>
            <CardContent>
              {msg.role === "assistant" ? (
                <div className="prose prose-sm max-w-none dark:prose-invert">
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
              ) : (
                <div className="text-sm">{msg.content}</div>
              )}
            </CardContent>
          </Card>
        ))}
        {loading && (
          <Card className="mr-12">
            <CardContent className="py-4">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <div className="flex gap-1">
                  <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:0ms]" />
                  <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:150ms]" />
                  <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:300ms]" />
                </div>
                {toolStatus || "Thinking..."}
              </div>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Input area */}
      <div className="border-t px-4 py-3">
        <div className="mx-auto flex max-w-3xl gap-2">
          <Textarea
            ref={textareaRef}
            rows={2}
            placeholder="Ask a question, journal an entry, check in on a goal..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            className="flex-1"
          />
          <div className="flex flex-col gap-1">
            <Button onClick={handleSend} disabled={loading || !input.trim()}>
              <Send className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="icon" onClick={handleNewChat} title="New chat">
              <Plus className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
