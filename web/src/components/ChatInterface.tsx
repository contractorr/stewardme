"use client";

import { useRef, useEffect, useState, useCallback } from "react";
import { toast } from "sonner";
import ReactMarkdown from "react-markdown";
import {
  AlertTriangle,
  Brain,
  Check,
  ChevronDown,
  ChevronUp,
  Lightbulb,
  PenLine,
  Plus,
  Send,
  Sparkles,
  Target,
  ThumbsDown,
  ThumbsUp,
  ArrowRight,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
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
import { logEngagement } from "@/lib/engagement";
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

function QuickCaptureInput({ token }: { token: string }) {
  const [text, setText] = useState("");
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const handleSubmit = async () => {
    if (!text.trim() || saving) return;
    setSaving(true);
    try {
      await apiFetch(
        "/api/journal/quick",
        { method: "POST", body: JSON.stringify({ content: text.trim() }) },
        token,
      );
      setText("");
      setSaved(true);
      toast.success("Captured");
      setTimeout(() => setSaved(false), 2000);
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="flex items-center gap-2 rounded-lg border bg-card px-3 py-2">
      <PenLine className="h-4 w-4 shrink-0 text-muted-foreground" />
      <input
        type="text"
        placeholder="What's on your mind today?"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            handleSubmit();
          }
        }}
        disabled={saving}
        className="flex-1 bg-transparent text-sm outline-none placeholder:text-muted-foreground"
      />
      {saved ? (
        <Check className="h-4 w-4 text-green-500" />
      ) : (
        <Button
          variant="ghost"
          size="icon"
          className="h-7 w-7 shrink-0"
          onClick={handleSubmit}
          disabled={saving || !text.trim()}
        >
          <Send className="h-3.5 w-3.5" />
        </Button>
      )}
    </div>
  );
}

function BriefingPanel({ briefing, onChipClick, token }: { briefing: BriefingResponse; onChipClick: (text: string) => void; token: string }) {
  const [expandedRecs, setExpandedRecs] = useState<Set<string>>(new Set());
  const [feedbackGiven, setFeedbackGiven] = useState<Record<string, "useful" | "irrelevant">>({});

  const toggleReasoning = (id: string) => {
    setExpandedRecs((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const handleFeedback = (id: string, category: string, type: "useful" | "irrelevant") => {
    setFeedbackGiven((prev) => ({ ...prev, [id]: type }));
    logEngagement(
      token,
      type === "useful" ? "feedback_useful" : "feedback_irrelevant",
      "recommendation",
      id,
      { category },
    );
  };

  const hour = new Date().getHours();
  const greeting =
    hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";

  const hasSignals = briefing.signals.length > 0;
  const hasRecommendations = briefing.recommendations.length > 0;
  const hasStaleGoals = briefing.stale_goals.length > 0;
  const hasPatterns = briefing.patterns.length > 0;

  return (
    <div className="mx-auto max-w-2xl space-y-4 py-6">
      <div className="text-center">
        <h2 className="text-lg font-medium">{greeting}</h2>
        <p className="text-sm text-muted-foreground">Here&apos;s what needs your attention.</p>
      </div>

      <QuickCaptureInput token={token} />

      {hasSignals && (
        <div className="space-y-2">
          <div className="flex items-center gap-2 px-1 text-xs font-medium text-muted-foreground">
            <AlertTriangle className="h-3.5 w-3.5" />
            Heads up
          </div>
          {briefing.signals.map((s) => (
            <button
              key={s.id}
              onClick={() => {
                logEngagement(token, "opened", "signal", String(s.id));
                onChipClick(`Tell me more about: ${s.title}`);
              }}
              className="w-full rounded-lg border bg-card p-3 text-left transition-colors hover:bg-accent"
            >
              <p className="text-sm font-medium">{s.title}</p>
              <p className="mt-0.5 text-xs text-muted-foreground">{s.detail}</p>
            </button>
          ))}
        </div>
      )}

      {hasStaleGoals && (
        <div className="space-y-2">
          <div className="flex items-center gap-2 px-1 text-xs font-medium text-muted-foreground">
            <Target className="h-3.5 w-3.5" />
            Goals that need attention
          </div>
          {briefing.stale_goals.map((g) => (
            <button
              key={g.path}
              onClick={() => onChipClick(`Help me with my goal: ${g.title}`)}
              className="w-full rounded-lg border bg-card p-3 text-left transition-colors hover:bg-accent"
            >
              <p className="text-sm font-medium">{g.title}</p>
              <p className="mt-0.5 text-xs text-muted-foreground">
                Last check-in {g.days_since_check} days ago
              </p>
            </button>
          ))}
        </div>
      )}

      {hasRecommendations && (
        <div className="space-y-2">
          <div className="flex items-center gap-2 px-1 text-xs font-medium text-muted-foreground">
            <Lightbulb className="h-3.5 w-3.5" />
            Suggestions
          </div>
          {briefing.recommendations.map((r) => (
            <div key={r.id} className="rounded-lg border bg-card text-left">
              <button
                onClick={() => {
                  logEngagement(token, "opened", "recommendation", String(r.id));
                  onChipClick(`Tell me more about: ${r.title}`);
                }}
                className="w-full p-3 transition-colors hover:bg-accent rounded-lg text-left"
              >
                <p className="text-sm font-medium">{r.title}</p>
                <p className="mt-0.5 text-xs text-muted-foreground">{r.description}</p>
              </button>
              <div className="flex items-center gap-1 px-3 pb-2">
                {r.reasoning_trace && (
                  <button
                    onClick={() => toggleReasoning(r.id)}
                    className="text-[11px] text-muted-foreground hover:text-foreground flex items-center gap-0.5"
                  >
                    Why this?
                    {expandedRecs.has(r.id) ? (
                      <ChevronUp className="h-3 w-3" />
                    ) : (
                      <ChevronDown className="h-3 w-3" />
                    )}
                  </button>
                )}
                <span className="ml-auto flex items-center gap-1">
                  {feedbackGiven[r.id] ? (
                    <span className="text-[10px] text-muted-foreground">
                      {feedbackGiven[r.id] === "useful" ? "Marked useful" : "Marked irrelevant"}
                    </span>
                  ) : (
                    <>
                      <button
                        onClick={() => handleFeedback(r.id, r.category, "useful")}
                        className="p-1 text-muted-foreground hover:text-green-600 transition-colors"
                        title="Useful"
                      >
                        <ThumbsUp className="h-3 w-3" />
                      </button>
                      <button
                        onClick={() => handleFeedback(r.id, r.category, "irrelevant")}
                        className="p-1 text-muted-foreground hover:text-red-500 transition-colors"
                        title="Not relevant"
                      >
                        <ThumbsDown className="h-3 w-3" />
                      </button>
                    </>
                  )}
                </span>
              </div>
              {r.reasoning_trace && expandedRecs.has(r.id) && (
                <div className="mx-3 mb-2 text-xs text-muted-foreground space-y-0.5">
                  {r.reasoning_trace.source_signal && (
                    <p><span className="font-medium text-foreground">Source:</span> {r.reasoning_trace.source_signal}</p>
                  )}
                  {r.reasoning_trace.profile_match && (
                    <p><span className="font-medium text-foreground">Match:</span> {r.reasoning_trace.profile_match}</p>
                  )}
                  <p>
                    <span className="font-medium text-foreground">Confidence:</span>{" "}
                    <Badge variant="secondary" className="text-[10px] px-1 py-0">
                      {Math.round(r.reasoning_trace.confidence * 100)}%
                    </Badge>
                  </p>
                  {r.reasoning_trace.caveats && (
                    <p className="text-amber-600 dark:text-amber-400">
                      <span className="font-medium">Caveats:</span> {r.reasoning_trace.caveats}
                    </p>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {hasPatterns && (
        <div className="space-y-2">
          <div className="flex items-center gap-2 px-1 text-xs font-medium text-muted-foreground">
            <Brain className="h-3.5 w-3.5" />
            Observations
          </div>
          {briefing.patterns.map((p, i) => (
            <button
              key={i}
              onClick={() => {
                logEngagement(token, "opened", "pattern", String(i));
                onChipClick(`Tell me more about: ${p.summary}`);
              }}
              className="w-full rounded-lg border bg-card p-3 text-left transition-colors hover:bg-accent"
            >
              <p className="text-sm font-medium">{p.summary}</p>
              {p.evidence.length > 0 && (
                <p className="mt-0.5 text-xs text-muted-foreground">{p.evidence[0]}</p>
              )}
            </button>
          ))}
        </div>
      )}

      {briefing.adaptation_count > 0 && (
        <div className="flex items-center justify-center gap-1.5 text-[11px] text-muted-foreground">
          <Sparkles className="h-3 w-3" />
          Your profile is learning — {briefing.adaptation_count} signal{briefing.adaptation_count !== 1 ? "s" : ""} absorbed
        </div>
      )}

      <div className="flex flex-wrap justify-center gap-2 pt-2">
        {SUGGESTION_CHIPS.slice(0, 3).map((chip) => (
          <button
            key={chip}
            onClick={() => onChipClick(chip)}
            className="rounded-full border px-3 py-1.5 text-xs hover:bg-accent transition-colors"
          >
            {chip}
          </button>
        ))}
      </div>
    </div>
  );
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

  const showBriefing =
    !onboardingMode && messages.length === 0 && !restoredConv && briefing?.has_data;

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
    setMessages((prev) => [...prev, { role: "user", content: question }]);
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
            <h2 className="text-xl font-semibold">Welcome to <span className="text-primary">StewardMe</span></h2>
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
      <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-4">
        {showBriefing && briefing && (
          <BriefingPanel briefing={briefing} onChipClick={handleChipClick} token={token} />
        )}
        {messages.length === 0 && !showBriefing && (
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-muted">
              <Brain className="h-7 w-7 text-muted-foreground" />
            </div>
            <h3 className="text-lg font-medium">What should we navigate?</h3>
            <p className="mt-1 max-w-md text-sm text-muted-foreground">
              Ask about opportunities, trends, goals, or journal your thoughts — your steward handles the rest.
            </p>
            <div className="mx-auto mt-5 w-full max-w-md">
              <QuickCaptureInput token={token} />
            </div>
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
        <div className="mx-auto max-w-3xl space-y-3">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={
                msg.role === "user"
                  ? "ml-12 rounded-2xl rounded-br-sm bg-primary/10 px-4 py-2.5"
                  : "mr-12 rounded-2xl rounded-bl-sm bg-card border px-4 py-2.5"
              }
            >
              {msg.role === "assistant" ? (
                <div className="prose prose-sm max-w-none dark:prose-invert">
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
              ) : (
                <p className="text-sm">{msg.content}</p>
              )}
            </div>
          ))}
          {loading && (
            <div className="mr-12 rounded-2xl rounded-bl-sm border bg-card px-4 py-3">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <div className="flex gap-1">
                  <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:0ms]" />
                  <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:150ms]" />
                  <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:300ms]" />
                </div>
                {toolStatus || "Thinking..."}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Input area */}
      <div className="border-t px-4 py-3">
        <div className="mx-auto flex max-w-3xl gap-2">
          <Textarea
            ref={textareaRef}
            rows={1}
            placeholder="Ask anything..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            className="flex-1 resize-none"
          />
          <div className="flex items-end gap-1">
            <Button onClick={handleSend} disabled={loading || !input.trim()}>
              <Send className="h-4 w-4" />
            </Button>
            {messages.length > 0 && (
              <Button variant="ghost" size="icon" onClick={handleNewChat} title="New chat">
                <Plus className="h-4 w-4" />
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
