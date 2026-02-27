"use client";

import { useRef, useEffect, useState, useCallback } from "react";
import { toast } from "sonner";
import ReactMarkdown from "react-markdown";
import {
  AlertTriangle,
  ArrowRight,
  Brain,
  Check,
  ChevronDown,
  ChevronUp,
  Clock,
  Lightbulb,
  PenLine,
  Plus,
  Rss,
  Send,
  Sparkles,
  Target,
  ThumbsDown,
  ThumbsUp,
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

const STATIC_CHIPS = [
  "What should I focus on today?",
  "Help me think through a decision",
  "How are my goals progressing?",
];

function getGreeting(): string {
  const h = new Date().getHours();
  if (h < 12) return "Good morning";
  if (h < 17) return "Good afternoon";
  return "Good evening";
}

function buildSuggestionChips(briefing: BriefingResponse | null): string[] {
  if (!briefing) return STATIC_CHIPS;

  // Prefer daily brief actions as chips
  if (briefing.daily_brief?.items?.length) {
    const chips = briefing.daily_brief.items.slice(0, 4).map((item) => item.action);
    return chips;
  }

  const chips: string[] = [];
  for (const g of briefing.stale_goals) {
    if (chips.length >= 4) break;
    chips.push(`Check in on: ${g.title}`);
  }
  if (chips.length === 0 && briefing.goals?.length > 0) {
    for (const g of briefing.goals) {
      if (chips.length >= 3) break;
      chips.push(`Help me think through: ${g.title}`);
    }
  }
  if (chips.length < 4 && briefing.recommendations.length > 0) {
    chips.push(`Tell me more about: ${briefing.recommendations[0].title}`);
  }
  while (chips.length < 4 && chips.length < STATIC_CHIPS.length) {
    const fallback = STATIC_CHIPS[chips.length];
    if (!chips.includes(fallback)) chips.push(fallback);
    else break;
  }
  return chips.slice(0, 4);
}

interface TopPriority {
  kind: "recommendation" | "goal" | "signal";
  title: string;
  description: string;
  action: string;
}

function getTopPriority(briefing: BriefingResponse): TopPriority | null {
  // Daily brief card replaces the top priority callout
  if (briefing.daily_brief?.items?.length) return null;

  if (briefing.recommendations.length > 0) {
    const top = [...briefing.recommendations].sort((a, b) => b.score - a.score)[0];
    return { kind: "recommendation", title: top.title, description: top.description, action: `Tell me more about: ${top.title}` };
  }
  if (briefing.stale_goals.length > 0) {
    const g = briefing.stale_goals[0];
    return { kind: "goal", title: g.title, description: `Last check-in ${g.days_since_check} days ago`, action: `Help me with my goal: ${g.title}` };
  }
  if (briefing.signals.length > 0) {
    const s = briefing.signals[0];
    return { kind: "signal", title: s.title, description: s.detail, action: `Tell me more about: ${s.title}` };
  }
  if (briefing.goals?.length > 0) {
    const g = briefing.goals[0];
    return { kind: "goal", title: g.title, description: "Newly set \u2014 start building momentum", action: `Help me think through my goal: ${g.title}` };
  }
  return null;
}

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

function BriefingPanel({ briefing, onChipClick, token, userName }: { briefing: BriefingResponse; onChipClick: (text: string) => void; token: string; userName?: string | null }) {
  const [expandedRecs, setExpandedRecs] = useState<Set<string>>(new Set());
  const [expandedCritic, setExpandedCritic] = useState<Set<string>>(new Set());
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

  const topPriority = getTopPriority(briefing);
  const chips = buildSuggestionChips(briefing);

  // Dedup: skip top priority item from its section
  const filteredRecommendations = topPriority?.kind === "recommendation"
    ? briefing.recommendations.filter((r) => r.title !== topPriority.title)
    : briefing.recommendations;
  const filteredStaleGoals = topPriority?.kind === "goal"
    ? briefing.stale_goals.filter((g) => g.title !== topPriority.title)
    : briefing.stale_goals;
  const filteredSignals = topPriority?.kind === "signal"
    ? briefing.signals.filter((s) => s.title !== topPriority.title)
    : briefing.signals;

  // Fresh goals: dedup against stale_goals by path
  const stalePaths = new Set(briefing.stale_goals.map((g) => g.path));
  const freshGoals = (briefing.goals || []).filter((g) => !stalePaths.has(g.path));
  const onlyGoals = !briefing.signals.length && !briefing.recommendations.length && !briefing.patterns.length && freshGoals.length > 0;

  const hasSignals = filteredSignals.length > 0;
  const hasRecommendations = filteredRecommendations.length > 0;
  const hasStaleGoals = filteredStaleGoals.length > 0;
  const hasPatterns = briefing.patterns.length > 0;

  const greeting = userName ? `${getGreeting()}, ${userName}` : getGreeting();

  return (
    <div className="mx-auto max-w-2xl space-y-4 py-4">
      <div className="px-1">
        <p className="text-base font-medium">{greeting}</p>
        <p className="text-sm text-muted-foreground">Here&apos;s your situation.</p>
      </div>

      {briefing.daily_brief?.items && briefing.daily_brief.items.length > 0 && (
        <div className="rounded-lg border bg-card">
          <div className="flex items-center gap-2 px-3 pt-3 pb-1">
            <Clock className="h-3.5 w-3.5 text-muted-foreground" />
            <span className="text-xs font-medium text-muted-foreground">Today&apos;s focus</span>
            <span className={`ml-auto text-[10px] ${briefing.daily_brief.used_minutes > briefing.daily_brief.budget_minutes ? "text-amber-500" : "text-muted-foreground"}`}>
              {briefing.daily_brief.used_minutes} of {briefing.daily_brief.budget_minutes} min
            </span>
          </div>
          <div className="divide-y">
            {briefing.daily_brief.items.map((item) => (
              <button
                key={`${item.kind}-${item.priority}`}
                onClick={() => onChipClick(item.action)}
                className="flex w-full items-start gap-3 px-3 py-2.5 text-left transition-colors hover:bg-accent"
              >
                <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-primary/10 text-[10px] font-bold text-primary">
                  {item.priority}
                </span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium">{item.title}</p>
                  <p className="text-xs text-muted-foreground truncate">{item.description}</p>
                </div>
                <span className="shrink-0 rounded bg-muted px-1.5 py-0.5 text-[10px] text-muted-foreground">
                  {item.time_minutes}m
                </span>
              </button>
            ))}
          </div>
        </div>
      )}

      {topPriority && (
        <div className="rounded-lg border-l-4 border-primary bg-primary/5 p-3">
          <p className="text-xs font-medium text-muted-foreground mb-1">Act on this today</p>
          <p className="text-sm font-medium">{topPriority.title}</p>
          <p className="mt-0.5 text-xs text-muted-foreground">{topPriority.description}</p>
          <button
            onClick={() => onChipClick(topPriority.action)}
            className="mt-2 text-xs font-medium text-primary hover:underline"
          >
            Discuss this &rarr;
          </button>
        </div>
      )}

      <QuickCaptureInput token={token} />

      {hasSignals && (
        <div className="space-y-2">
          <div className="flex items-center gap-2 px-1 text-xs font-medium text-muted-foreground">
            <AlertTriangle className="h-3.5 w-3.5" />
            Heads up
          </div>
          {filteredSignals.map((s) => (
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
          {filteredStaleGoals.map((g) => (
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

      {onlyGoals && (
        <div className="rounded-lg border bg-card p-3">
          <p className="text-sm font-medium">Your steward is getting to know you</p>
          <p className="mt-0.5 text-xs text-muted-foreground">
            Write journal entries to build context &mdash; the more you reflect, the better the guidance.
          </p>
        </div>
      )}

      {freshGoals.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center gap-2 px-1 text-xs font-medium text-muted-foreground">
            <Target className="h-3.5 w-3.5" />
            Your goals
          </div>
          {freshGoals.map((g) => (
            <button
              key={g.path}
              onClick={() => onChipClick(`Help me think through my goal: ${g.title}`)}
              className="w-full rounded-lg border bg-card p-3 text-left transition-colors hover:bg-accent"
            >
              <p className="text-sm font-medium">{g.title}</p>
              <p className="mt-0.5 text-xs text-muted-foreground capitalize">{g.status}</p>
            </button>
          ))}
        </div>
      )}

      {hasRecommendations && (
        <div className="space-y-2">
          <div className="flex items-center gap-2 px-1 text-xs font-medium text-muted-foreground">
            <Lightbulb className="h-3.5 w-3.5" />
            Suggestions
            <span className="text-[10px] font-normal ml-1">— hypotheses, not certainties</span>
          </div>
          {filteredRecommendations.map((r) => (
            <div key={r.id} className="rounded-lg border bg-card text-left">
              <button
                onClick={() => {
                  logEngagement(token, "opened", "recommendation", String(r.id));
                  onChipClick(`Tell me more about: ${r.title}`);
                }}
                className="w-full p-3 transition-colors hover:bg-accent rounded-lg text-left"
              >
                <div className="flex items-center gap-1.5">
                  <p className="text-sm font-medium flex-1">{r.title}</p>
                  {r.critic && (
                    <Badge
                      variant={r.critic.confidence === "High" ? "outline" : r.critic.confidence === "Low" ? "destructive" : "secondary"}
                      className="text-[10px] px-1.5 py-0 shrink-0"
                    >
                      {r.critic.confidence}
                    </Badge>
                  )}
                </div>
                <p className="mt-0.5 text-xs text-muted-foreground">{r.description}</p>
              </button>
              <div className="flex items-center gap-1 px-3 pb-2 flex-wrap">
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
                {r.critic?.critic_challenge && (
                  <button
                    onClick={() => {
                      setExpandedCritic((prev) => {
                        const next = new Set(prev);
                        if (next.has(r.id)) next.delete(r.id);
                        else next.add(r.id);
                        return next;
                      });
                    }}
                    className="text-[11px] text-muted-foreground hover:text-foreground flex items-center gap-0.5"
                  >
                    Why this might be wrong
                    {expandedCritic.has(r.id) ? (
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
                  {r.critic && (
                    <p>
                      <span className="font-medium text-foreground">Confidence:</span>{" "}
                      <Badge
                        variant={r.critic.confidence === "High" ? "outline" : r.critic.confidence === "Low" ? "destructive" : "secondary"}
                        className="text-[10px] px-1 py-0"
                      >
                        {r.critic.confidence}
                      </Badge>
                      {r.critic.confidence_rationale && (
                        <span className="ml-1">{r.critic.confidence_rationale}</span>
                      )}
                    </p>
                  )}
                  {!r.critic && (
                    <p>
                      <span className="font-medium text-foreground">Confidence:</span>{" "}
                      <Badge variant="secondary" className="text-[10px] px-1 py-0">
                        {Math.round(r.reasoning_trace.confidence * 100)}%
                      </Badge>
                    </p>
                  )}
                  {r.reasoning_trace.caveats && (
                    <p className="text-amber-600 dark:text-amber-400">
                      <span className="font-medium">Caveats:</span> {r.reasoning_trace.caveats}
                    </p>
                  )}
                </div>
              )}
              {r.critic && expandedCritic.has(r.id) && (
                <div className="mx-3 mb-2 rounded-md border border-amber-200 dark:border-amber-800 bg-amber-50/50 dark:bg-amber-950/20 p-2 text-xs space-y-1">
                  {r.critic.critic_challenge && (
                    <p><span className="font-medium">Challenge:</span> {r.critic.critic_challenge}</p>
                  )}
                  {r.critic.missing_context && (
                    <p className="text-muted-foreground">
                      <span className="font-medium text-foreground">Missing context:</span> {r.critic.missing_context}
                    </p>
                  )}
                  {r.critic.intel_contradictions && (
                    <p className="text-amber-700 dark:text-amber-400">
                      <span className="font-medium">Signals that complicate this:</span> {r.critic.intel_contradictions}
                    </p>
                  )}
                  {r.critic.alternative && (
                    <div className="mt-1 pt-1 border-t border-amber-200 dark:border-amber-800">
                      <p className="font-medium">Contrarian take:</p>
                      <p className="text-muted-foreground">{r.critic.alternative}</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {briefing.goal_intel_matches?.length > 0 && (() => {
        const grouped = briefing.goal_intel_matches.reduce<Record<string, typeof briefing.goal_intel_matches>>((acc, m) => {
          const key = m.goal_title || "Other";
          if (!acc[key]) acc[key] = [];
          if (acc[key].length < 3) acc[key].push(m);
          return acc;
        }, {});
        return (
          <div className="space-y-2">
            <div className="flex items-center gap-2 px-1 text-xs font-medium text-muted-foreground">
              <Rss className="h-3.5 w-3.5" />
              Intel for your goals
            </div>
            {Object.entries(grouped).map(([goalTitle, matches]) => (
              <div key={goalTitle} className="rounded-lg border bg-card">
                <p className="px-3 pt-2 text-xs font-medium text-muted-foreground">{goalTitle}</p>
                <div className="divide-y">
                  {matches.map((m) => (
                    <button
                      key={m.id}
                      onClick={() => onChipClick(`Tell me about this and how it relates to my goal: ${m.title}`)}
                      className="flex w-full items-start gap-2 px-3 py-2 text-left transition-colors hover:bg-accent"
                    >
                      <span className={`mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full ${m.urgency === "high" ? "bg-amber-500" : m.urgency === "medium" ? "bg-blue-400" : "bg-gray-300"}`} />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium truncate">{m.title}</p>
                        {m.summary && <p className="text-xs text-muted-foreground truncate">{m.summary}</p>}
                      </div>
                      <ArrowRight className="mt-1 h-3.5 w-3.5 shrink-0 text-muted-foreground" />
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        );
      })()}

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
        {chips.map((chip) => (
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
  userName,
}: {
  token: string;
  briefing: BriefingResponse | null;
  onRefresh: () => void;
  onboardingMode?: boolean;
  userName?: string | null;
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
              Connect your LLM API key to activate your steward. Your key is
              encrypted and stored only for your account.
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
          <p className="text-sm font-medium">Getting to know you</p>
          <p className="text-xs text-muted-foreground">
            A few quick questions so I can hit the ground running
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
                  {msg.role === "user" ? "You" : "Steward"}
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
              All set. Taking you to your brief...
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
          <BriefingPanel briefing={briefing} onChipClick={handleChipClick} token={token} userName={userName} />
        )}
        {messages.length === 0 && !showBriefing && (
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-muted">
              <Brain className="h-7 w-7 text-muted-foreground" />
            </div>
            <h3 className="text-lg font-medium">What do you need to work through?</h3>
            <p className="mt-1 max-w-md text-sm text-muted-foreground">
              Ask me anything — a decision, a priority, a goal, or what to do next.
              I&apos;ll draw on your journal and radar to give you a grounded answer.
            </p>
            <div className="mx-auto mt-5 w-full max-w-md">
              <QuickCaptureInput token={token} />
            </div>
            <div className="mt-6 flex flex-wrap justify-center gap-2">
              {buildSuggestionChips(briefing).map((chip) => (
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
            placeholder="Ask me anything..."
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
