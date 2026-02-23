"use client";

import { useRef, useEffect, useState, useCallback } from "react";
import { toast } from "sonner";
import ReactMarkdown from "react-markdown";
import {
  Brain,
  Plus,
  Send,
  ArrowRight,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
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
  isBriefing?: boolean;
}

const CONV_KEY = "main_chat_conv_id";

const SUGGESTION_CHIPS = [
  "What should I focus on?",
  "Show me opportunities",
  "What's trending in my field?",
  "Suggest a learning path",
  "Help me prioritize",
  "Review my progress",
];

function buildBriefingMessage(briefing: BriefingResponse): string {
  const hour = new Date().getHours();
  const greeting =
    hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";

  const parts: string[] = [`${greeting}! Here's your daily brief:\n`];

  if (briefing.signals.length > 0) {
    parts.push("### Signals");
    for (const s of briefing.signals) {
      parts.push(`- **${s.title}** (severity ${s.severity}) — ${s.detail}`);
    }
    parts.push("");
  }

  if (briefing.patterns.length > 0) {
    parts.push("### Patterns");
    for (const p of briefing.patterns) {
      parts.push(
        `- **${p.summary}** (${Math.round(p.confidence * 100)}% confidence)${p.evidence.length > 0 ? ` — ${p.evidence[0]}` : ""}`
      );
    }
    parts.push("");
  }

  if (briefing.recommendations.length > 0) {
    parts.push("### Recommendations");
    for (const r of briefing.recommendations) {
      parts.push(`- **${r.title}** [${r.category}] — ${r.description}`);
    }
    parts.push("");
  }

  if (briefing.stale_goals.length > 0) {
    parts.push("### Stale Goals");
    for (const g of briefing.stale_goals) {
      parts.push(`- **${g.title}** — last check-in ${g.days_since_check}d ago`);
    }
    parts.push("");
  }

  parts.push("Ask me about any of these, or tell me what's on your mind.");

  return parts.join("\n");
}

export function ChatInterface({
  token,
  briefing,
  onRefresh,
  onboardingMode,
}: {
  token: string;
  briefing: BriefingResponse | null;
  onRefresh: () => void;
  onboardingMode?: boolean;
}) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [toolStatus, setToolStatus] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [restoredConv, setRestoredConv] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Onboarding state
  const [onboardingPhase, setOnboardingPhase] = useState<"key" | "chat" | null>(
    onboardingMode ? "key" : null
  );
  const [provider, setProvider] = useState("auto");
  const [apiKey, setApiKey] = useState("");
  const [savingKey, setSavingKey] = useState(false);
  const [onboardingSending, setOnboardingSending] = useState(false);
  const [onboardingDone, setOnboardingDone] = useState(false);

  // Restore conversation on mount (skip in onboarding)
  useEffect(() => {
    if (onboardingMode) return;
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
  }, [token, onboardingMode]);

  // Proactive briefing as first message
  useEffect(() => {
    if (onboardingMode) return;
    if (messages.length > 0 || restoredConv) return;
    if (!briefing?.has_data) return;

    setMessages([
      { role: "assistant", content: buildBriefingMessage(briefing), isBriefing: true },
    ]);
  }, [briefing, messages.length, restoredConv, onboardingMode]);

  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages, loading, onboardingSending]);

  const handleNewChat = () => {
    setConversationId(null);
    setMessages([]);
    setRestoredConv(false);
    localStorage.removeItem(CONV_KEY);
  };

  const handleChipClick = (text: string) => {
    setInput(text);
    setTimeout(() => textareaRef.current?.focus(), 100);
  };

  const handleSend = useCallback(async () => {
    if (!input.trim() || loading) return;
    const question = input.trim();
    setInput("");
    // Filter out briefing messages before adding user message
    setMessages((prev) => [
      ...prev.filter((m) => !m.isBriefing),
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

  // --- Onboarding handlers ---
  const handleSaveKey = async () => {
    if (!apiKey.trim()) {
      toast.error("Please enter an API key");
      return;
    }
    setSavingKey(true);
    try {
      const payload: Record<string, string> = { llm_api_key: apiKey };
      if (provider !== "auto") payload.llm_provider = provider;
      await apiFetch("/api/settings", { method: "PUT", body: JSON.stringify(payload) }, token);

      // Start onboarding chat
      setOnboardingPhase("chat");
      setOnboardingSending(true);
      const res = await apiFetch<{ message: string; done: boolean }>(
        "/api/onboarding/start",
        { method: "POST" },
        token
      );
      setMessages([{ role: "assistant", content: res.message }]);
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setSavingKey(false);
      setOnboardingSending(false);
    }
  };

  const handleOnboardingSend = async () => {
    if (!input.trim() || onboardingSending) return;
    const text = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setOnboardingSending(true);

    try {
      const res = await apiFetch<{ message: string; done: boolean; goals_created: number }>(
        "/api/onboarding/chat",
        { method: "POST", body: JSON.stringify({ message: text }) },
        token
      );
      setMessages((prev) => [...prev, { role: "assistant", content: res.message }]);
      if (res.done) {
        setOnboardingDone(true);
        onRefresh();
      }
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setOnboardingSending(false);
    }
  };

  // --- Onboarding: API key phase ---
  if (onboardingPhase === "key") {
    return (
      <div className="flex h-full flex-col items-center justify-center px-4">
        <div className="w-full max-w-md space-y-6">
          <div className="flex flex-col items-center text-center">
            <div className="mb-3 flex h-14 w-14 items-center justify-center rounded-full bg-primary/10">
              <Brain className="h-7 w-7 text-primary" />
            </div>
            <h2 className="text-xl font-semibold">Welcome to StewardMe</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              Enter your LLM API key to get started. Your key is encrypted and stored per-user.
            </p>
          </div>

          <div className="space-y-4 rounded-lg border p-4">
            <div className="space-y-1.5">
              <Label>Provider</Label>
              <Select value={provider} onValueChange={setProvider}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="auto">Auto-detect</SelectItem>
                  <SelectItem value="claude">Claude</SelectItem>
                  <SelectItem value="openai">OpenAI</SelectItem>
                  <SelectItem value="gemini">Gemini</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-1.5">
              <Label>API Key</Label>
              <Input
                type="password"
                placeholder="sk-... or your provider key"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") handleSaveKey();
                }}
              />
            </div>
            <Button onClick={handleSaveKey} disabled={savingKey} className="w-full">
              {savingKey ? "Setting up..." : "Get Started"}
              {!savingKey && <ArrowRight className="ml-2 h-4 w-4" />}
            </Button>
          </div>
        </div>
      </div>
    );
  }

  // --- Onboarding: chat phase ---
  if (onboardingPhase === "chat") {
    return (
      <div className="flex h-full flex-col">
        <div className="border-b px-4 py-2">
          <p className="text-sm font-medium">Setting up your profile</p>
          <p className="text-xs text-muted-foreground">
            Answer a few questions to personalize your experience
          </p>
        </div>

        <div ref={scrollRef} className="flex-1 space-y-4 overflow-y-auto px-4 py-4">
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
          {onboardingSending && (
            <Card className="mr-12">
              <CardContent className="py-4">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <div className="flex gap-1">
                    <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:0ms]" />
                    <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:150ms]" />
                    <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:300ms]" />
                  </div>
                  Thinking...
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {onboardingDone ? (
          <div className="border-t px-4 py-3 text-center">
            <p className="text-sm text-muted-foreground">
              Profile set up! Reloading...
            </p>
          </div>
        ) : (
          <div className="border-t px-4 py-3">
            <div className="mx-auto flex max-w-3xl gap-2">
              <Textarea
                ref={textareaRef}
                rows={2}
                placeholder="Type your answer..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleOnboardingSend();
                  }
                }}
                disabled={onboardingSending}
                className="flex-1"
              />
              <Button
                onClick={handleOnboardingSend}
                disabled={onboardingSending || !input.trim()}
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </div>
        )}
      </div>
    );
  }

  // --- Normal chat ---
  return (
    <div className="flex h-full flex-col">
      {/* Chat messages */}
      <div ref={scrollRef} className="flex-1 space-y-4 overflow-y-auto px-4 py-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-muted">
              <Brain className="h-7 w-7 text-muted-foreground" />
            </div>
            <h3 className="text-lg font-medium">What should we navigate?</h3>
            <p className="mt-1 max-w-md text-sm text-muted-foreground">
              Ask about opportunities, trends, goals, or journal your thoughts — your steward handles the rest.
            </p>
            <div className="mt-6 flex flex-wrap justify-center gap-2">
              {SUGGESTION_CHIPS.map((chip) => (
                <button
                  key={chip}
                  onClick={() => handleChipClick(chip)}
                  className="rounded-full border px-3 py-1.5 text-sm hover:bg-accent transition-colors"
                >
                  {chip}
                </button>
              ))}
            </div>
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
            placeholder="Ask about opportunities, trends, goals, or journal a thought..."
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
