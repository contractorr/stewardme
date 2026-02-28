"use client";

import { useState, type ReactNode } from "react";
import { toast } from "sonner";
import { Collapsible } from "radix-ui";
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
  Send,
  Sparkles,
  Target,
  ThumbsDown,
  ThumbsUp,
  Zap,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { apiFetch } from "@/lib/api";
import { logEngagement } from "@/lib/engagement";
import type { BriefingResponse, GoalIntelMatch } from "@/types/briefing";

const STATIC_CHIPS = [
  "What should I focus on today?",
  "Help me think through a decision",
  "How are my goals progressing?",
];

export function getGreeting(): string {
  const h = new Date().getHours();
  if (h < 12) return "Good morning";
  if (h < 17) return "Good afternoon";
  return "Good evening";
}

export function buildSuggestionChips(briefing: BriefingResponse | null): string[] {
  if (!briefing) return STATIC_CHIPS;

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

/* ------------------------------------------------------------------ */
/*  CollapsibleSection                                                 */
/* ------------------------------------------------------------------ */

function CollapsibleSection({
  icon,
  label,
  count,
  defaultOpen = false,
  suffix,
  children,
}: {
  icon: ReactNode;
  label: string;
  count: number;
  defaultOpen?: boolean;
  suffix?: ReactNode;
  children: ReactNode;
}) {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <Collapsible.Root open={open} onOpenChange={setOpen} className="space-y-2">
      <Collapsible.Trigger className="flex w-full items-center gap-2 px-1 text-xs font-medium text-muted-foreground hover:text-foreground transition-colors">
        {icon}
        <span>{label}</span>
        <Badge variant="secondary" className="text-[10px] px-1.5 py-0 min-w-[1.25rem] justify-center">
          {count}
        </Badge>
        {suffix && <span className="ml-auto mr-1 text-[10px] font-normal">{suffix}</span>}
        <ChevronDown
          className={`h-3.5 w-3.5 shrink-0 transition-transform duration-150 ${suffix ? "" : "ml-auto"} ${open ? "rotate-180" : ""}`}
        />
      </Collapsible.Trigger>
      <Collapsible.Content className="overflow-hidden data-[state=open]:animate-[collapsible-down_150ms_ease-out] data-[state=closed]:animate-[collapsible-up_150ms_ease-out]">
        {children}
      </Collapsible.Content>
    </Collapsible.Root>
  );
}

/* ------------------------------------------------------------------ */
/*  Helpers                                                            */
/* ------------------------------------------------------------------ */

interface TopPriority {
  kind: "recommendation" | "goal" | "signal";
  title: string;
  description: string;
  action: string;
}

function getTopPriority(briefing: BriefingResponse): TopPriority | null {
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
    return { kind: "goal", title: g.title, description: "Newly set — start building momentum", action: `Help me think through my goal: ${g.title}` };
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
    <div className="flex items-center gap-2 rounded-xl border bg-card px-3 py-2">
      <PenLine className="h-4 w-4 shrink-0 text-muted-foreground" />
      <Input
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
        className="flex-1 border-0 shadow-none h-auto p-0 focus-visible:ring-0 text-sm"
      />
      {saved ? (
        <Check className="h-4 w-4 text-success" />
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

/* ------------------------------------------------------------------ */
/*  GoalsSection                                                       */
/* ------------------------------------------------------------------ */

interface UnifiedGoal {
  path: string;
  title: string;
  status: string;
  days_since_check: number;
  isStale: boolean;
}

function GoalsSection({
  allGoals,
  goalIntelMatches,
  onlyGoals,
  onChipClick,
}: {
  allGoals: UnifiedGoal[];
  goalIntelMatches: GoalIntelMatch[];
  onlyGoals: boolean;
  onChipClick: (text: string) => void;
}) {
  const [expandedIntel, setExpandedIntel] = useState<Set<string>>(new Set());

  // Group intel by goal_path, max 3 per goal
  const intelByGoal = goalIntelMatches.reduce<Record<string, GoalIntelMatch[]>>((acc, m) => {
    const key = m.goal_path || m.goal_title || "other";
    if (!acc[key]) acc[key] = [];
    if (acc[key].length < 3) acc[key].push(m);
    return acc;
  }, {});

  const toggleIntel = (goalPath: string) => {
    setExpandedIntel((prev) => {
      const next = new Set(prev);
      if (next.has(goalPath)) next.delete(goalPath);
      else next.add(goalPath);
      return next;
    });
  };

  return (
    <div className="space-y-2">
      {onlyGoals && (
        <div className="rounded-xl border bg-card p-3">
          <p className="text-sm font-medium">Your steward is getting to know you</p>
          <p className="mt-0.5 text-xs text-muted-foreground">
            Write journal entries to build context &mdash; the more you reflect, the better the guidance.
          </p>
        </div>
      )}
      {allGoals.map((g) => {
        const matches = intelByGoal[g.path] || [];
        const hasMatches = matches.length > 0;
        const isExpanded = expandedIntel.has(g.path);

        return (
          <div key={g.path} className="rounded-xl border bg-card">
            <button
              onClick={() => onChipClick(g.isStale ? `Help me with my goal: ${g.title}` : `Help me think through my goal: ${g.title}`)}
              className="w-full p-3 text-left transition-colors hover:bg-accent rounded-t-xl"
            >
              <div className="flex items-center gap-2">
                <p className="text-sm font-medium flex-1">{g.title}</p>
                <Badge variant="outline" className="text-[10px] px-1.5 py-0 capitalize shrink-0">
                  {g.status}
                </Badge>
              </div>
              {g.isStale && (
                <p className="mt-0.5 text-xs text-amber-600 dark:text-amber-400">
                  {g.days_since_check}d since check-in
                </p>
              )}
            </button>
            {hasMatches && (
              <>
                <div className="border-t mx-3" />
                <button
                  onClick={() => toggleIntel(g.path)}
                  className="flex w-full items-center gap-1.5 px-3 py-1.5 text-[11px] text-muted-foreground hover:text-foreground transition-colors"
                >
                  {matches.length} intel match{matches.length !== 1 ? "es" : ""}
                  {isExpanded ? (
                    <ChevronUp className="h-3 w-3" />
                  ) : (
                    <ChevronDown className="h-3 w-3" />
                  )}
                </button>
                {isExpanded && (
                  <div className="divide-y">
                    {matches.map((m) => (
                      <button
                        key={m.id}
                        onClick={() => onChipClick(`Tell me about this and how it relates to my goal: ${m.title}`)}
                        className="flex w-full items-start gap-2 px-3 py-2 text-left transition-colors hover:bg-accent"
                      >
                        <span className={`mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full ${m.urgency === "high" ? "bg-warning" : m.urgency === "medium" ? "bg-info" : "bg-muted-foreground/30"}`} />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium truncate">{m.title}</p>
                          {m.summary && <p className="text-xs text-muted-foreground truncate">{m.summary}</p>}
                        </div>
                        <ArrowRight className="mt-1 h-3.5 w-3.5 shrink-0 text-muted-foreground" />
                      </button>
                    ))}
                  </div>
                )}
              </>
            )}
          </div>
        );
      })}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  BriefingPanel                                                      */
/* ------------------------------------------------------------------ */

export function BriefingPanel({ briefing, onChipClick, token, userName }: { briefing: BriefingResponse; onChipClick: (text: string) => void; token: string; userName?: string | null }) {
  const [expandedRecs, setExpandedRecs] = useState<Set<string>>(new Set());
  const [expandedCritic, setExpandedCritic] = useState<Set<string>>(new Set());
  const [feedbackGiven, setFeedbackGiven] = useState<Record<string, "useful" | "irrelevant">>({});
  const [completedItems, setCompletedItems] = useState<Set<string>>(new Set());

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

  const toggleComplete = (itemKey: string) => {
    setCompletedItems((prev) => {
      const next = new Set(prev);
      if (next.has(itemKey)) next.delete(itemKey);
      else next.add(itemKey);
      return next;
    });
  };

  const topPriority = getTopPriority(briefing);
  const chips = buildSuggestionChips(briefing);

  const filteredRecommendations = topPriority?.kind === "recommendation"
    ? briefing.recommendations.filter((r) => r.title !== topPriority.title)
    : briefing.recommendations;
  const filteredStaleGoals = topPriority?.kind === "goal"
    ? briefing.stale_goals.filter((g) => g.title !== topPriority.title)
    : briefing.stale_goals;
  const filteredSignals = topPriority?.kind === "signal"
    ? briefing.signals.filter((s) => s.title !== topPriority.title)
    : briefing.signals;

  const stalePaths = new Set(briefing.stale_goals.map((g) => g.path));
  const freshGoals = (briefing.goals || []).filter((g) => !stalePaths.has(g.path));
  const onlyGoals = !briefing.signals.length && !briefing.recommendations.length && !briefing.patterns.length && freshGoals.length > 0;

  // Unified goals: stale first (sorted by days desc), then fresh
  const allGoals: UnifiedGoal[] = [
    ...filteredStaleGoals.map((g) => ({ ...g, isStale: true })),
    ...freshGoals.map((g) => ({ ...g, isStale: false })),
  ].sort((a, b) => {
    if (a.isStale && !b.isStale) return -1;
    if (!a.isStale && b.isStale) return 1;
    return b.days_since_check - a.days_since_check;
  });

  const hasSignals = filteredSignals.length > 0;
  const hasRecommendations = filteredRecommendations.length > 0;
  const hasGoals = allGoals.length > 0 || onlyGoals;
  const hasPatterns = briefing.patterns.length > 0;

  const greeting = userName ? `${getGreeting()}, ${userName}` : getGreeting();

  // Daily brief completion stats
  const dailyItems = briefing.daily_brief?.items || [];
  const completedCount = dailyItems.filter((item) => completedItems.has(`${item.kind}-${item.priority}`)).length;

  return (
    <div className="mx-auto max-w-2xl space-y-4 py-4">
      <div className="px-1">
        <p className="text-base font-medium">{greeting}</p>
        <p className="text-sm text-muted-foreground">Here&apos;s your situation.</p>
      </div>

      {dailyItems.length > 0 && (
        <CollapsibleSection
          icon={<Clock className="h-3.5 w-3.5 text-primary" />}
          label="Today's focus"
          count={dailyItems.length}
          defaultOpen={true}
          suffix={
            <span className={briefing.daily_brief!.used_minutes > briefing.daily_brief!.budget_minutes ? "text-amber-500" : undefined}>
              {completedCount}/{dailyItems.length} done &middot; {briefing.daily_brief!.used_minutes}m of {briefing.daily_brief!.budget_minutes}m
            </span>
          }
        >
          <div className="rounded-xl border border-t-2 border-t-primary bg-card">
            <div className="divide-y">
              {dailyItems.map((item) => {
                const itemKey = `${item.kind}-${item.priority}`;
                const isDone = completedItems.has(itemKey);
                return (
                  <div key={itemKey} className="flex items-start gap-3 px-3 py-2.5">
                    <button
                      onClick={() => toggleComplete(itemKey)}
                      className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full border-2 transition-colors ${
                        isDone
                          ? "border-primary bg-primary text-primary-foreground"
                          : "border-muted-foreground/30 hover:border-primary"
                      }`}
                    >
                      {isDone && <Check className="h-3 w-3" />}
                    </button>
                    <button
                      onClick={() => onChipClick(item.action)}
                      className={`flex flex-1 items-start gap-3 text-left transition-colors hover:opacity-80 ${isDone ? "opacity-50" : ""}`}
                    >
                      <div className="flex-1 min-w-0">
                        <p className={`text-sm font-medium ${isDone ? "line-through" : ""}`}>{item.title}</p>
                        <p className="text-xs text-muted-foreground truncate">{item.description}</p>
                      </div>
                      <span className="shrink-0 rounded bg-muted px-1.5 py-0.5 text-[10px] text-muted-foreground">
                        {item.time_minutes}m
                      </span>
                    </button>
                  </div>
                );
              })}
            </div>
            <button
              onClick={() => onChipClick("What's new in my space that I should know about?")}
              className="flex w-full items-center justify-center gap-1.5 border-t px-3 py-2 text-xs text-muted-foreground hover:text-foreground hover:bg-accent transition-colors rounded-b-xl"
            >
              <Zap className="h-3 w-3" />
              Summarize what&apos;s new
            </button>
          </div>
        </CollapsibleSection>
      )}

      {topPriority && (
        <div className="rounded-xl border-l-4 border-primary bg-primary/5 p-3">
          <p className="text-xs font-medium text-muted-foreground mb-1">Act on this today</p>
          <p className="text-sm font-medium">{topPriority.title}</p>
          <p className="mt-0.5 text-xs text-muted-foreground">{topPriority.description}</p>
          <Button
            variant="link"
            size="xs"
            onClick={() => onChipClick(topPriority.action)}
            className="mt-2 px-0 h-auto"
          >
            Discuss this &rarr;
          </Button>
        </div>
      )}

      <QuickCaptureInput token={token} />

      {hasSignals && (
        <CollapsibleSection
          icon={<AlertTriangle className="h-3.5 w-3.5" />}
          label="Heads up"
          count={filteredSignals.length}
        >
          <div className="space-y-2">
            {filteredSignals.map((s) => (
              <button
                key={s.id}
                onClick={() => {
                  logEngagement(token, "opened", "signal", String(s.id));
                  onChipClick(`Tell me more about: ${s.title}`);
                }}
                className="w-full rounded-xl border bg-card p-3 text-left transition-colors hover:bg-accent"
              >
                <p className="text-sm font-medium">{s.title}</p>
                <p className="mt-0.5 text-xs text-muted-foreground">{s.detail}</p>
              </button>
            ))}
          </div>
        </CollapsibleSection>
      )}

      {hasGoals && (
        <CollapsibleSection
          icon={<Target className="h-3.5 w-3.5" />}
          label="Goals"
          count={allGoals.length}
        >
          <GoalsSection
            allGoals={allGoals}
            goalIntelMatches={briefing.goal_intel_matches || []}
            onlyGoals={onlyGoals}
            onChipClick={onChipClick}
          />
        </CollapsibleSection>
      )}

      {hasRecommendations && (
        <CollapsibleSection
          icon={<Lightbulb className="h-3.5 w-3.5" />}
          label="Suggestions"
          count={filteredRecommendations.length}
        >
          <div className="space-y-2">
            {filteredRecommendations.map((r) => (
              <div key={r.id} className="rounded-xl border bg-card text-left">
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
        </CollapsibleSection>
      )}

      {hasPatterns && (
        <CollapsibleSection
          icon={<Brain className="h-3.5 w-3.5 text-info" />}
          label="Observations"
          count={briefing.patterns.length}
        >
          <div className="space-y-2">
            {briefing.patterns.map((p, i) => (
              <button
                key={i}
                onClick={() => {
                  logEngagement(token, "opened", "pattern", String(i));
                  onChipClick(`Tell me more about: ${p.summary}`);
                }}
                className="w-full rounded-xl border border-l-2 border-l-info bg-info/5 p-3 text-left transition-colors hover:bg-accent"
              >
                <p className="text-sm font-medium">{p.summary}</p>
                {p.evidence.length > 0 && (
                  <p className="mt-0.5 text-xs text-muted-foreground">{p.evidence[0]}</p>
                )}
              </button>
            ))}
          </div>
        </CollapsibleSection>
      )}

      {briefing.adaptation_count > 0 && (
        <div className="flex items-center justify-center gap-1.5 text-[11px] text-muted-foreground">
          <Sparkles className="h-3 w-3" />
          Your profile is learning — {briefing.adaptation_count} signal{briefing.adaptation_count !== 1 ? "s" : ""} absorbed
        </div>
      )}

      <div className="space-y-2 border-t pt-4">
        <p className="text-center text-[11px] text-muted-foreground">Try asking...</p>
        <div className="flex flex-wrap justify-center gap-2">
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
    </div>
  );
}
