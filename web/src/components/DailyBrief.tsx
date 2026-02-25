"use client";

import { useState } from "react";
import {
  AlertTriangle,
  Brain,
  ChevronDown,
  ChevronUp,
  Clock,
  Lightbulb,
  Target,
  ThumbsDown,
  ThumbsUp,
  TrendingUp,
  X,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { logEngagement } from "@/lib/engagement";
import type {
  BriefingSignal,
  BriefingPattern,
  BriefingRecommendation,
  BriefingGoal,
} from "@/types/briefing";

function severityColor(severity: number) {
  if (severity >= 7) return "destructive";
  if (severity >= 4) return "secondary";
  return "outline";
}

function confidenceColor(confidence: number) {
  if (confidence >= 0.7) return "destructive";
  if (confidence >= 0.4) return "secondary";
  return "outline";
}

function signalIcon(type: string) {
  switch (type) {
    case "sentiment_alert":
      return <AlertTriangle className="h-4 w-4" />;
    case "goal_stale":
    case "goal_complete":
      return <Target className="h-4 w-4" />;
    case "topic_emergence":
    case "research_trigger":
      return <Lightbulb className="h-4 w-4" />;
    case "journal_gap":
      return <Clock className="h-4 w-4" />;
    case "learning_stalled":
      return <Brain className="h-4 w-4" />;
    default:
      return <AlertTriangle className="h-4 w-4" />;
  }
}

function patternIcon(type: string) {
  switch (type) {
    case "burnout":
      return <AlertTriangle className="h-4 w-4" />;
    case "momentum":
      return <TrendingUp className="h-4 w-4" />;
    case "blind_spot":
      return <Target className="h-4 w-4" />;
    default:
      return <Brain className="h-4 w-4" />;
  }
}

export function SignalsCard({
  signals,
  onAskAbout,
  onDismiss,
}: {
  signals: BriefingSignal[];
  onAskAbout: (q: string) => void;
  onDismiss: (id: number) => void;
}) {
  if (signals.length === 0) return null;
  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-base">
          <AlertTriangle className="h-4 w-4" />
          Attention Needed
          <Badge variant="destructive" className="ml-auto text-xs">
            {signals.length}
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {signals.map((s) => (
          <div
            key={s.id}
            className="flex items-start gap-2 rounded-md border p-2 text-sm"
          >
            <div className="mt-0.5 shrink-0">{signalIcon(s.type)}</div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <span className="font-medium truncate">{s.title}</span>
                <Badge variant={severityColor(s.severity)} className="text-xs shrink-0">
                  {s.severity}
                </Badge>
              </div>
              <p className="mt-0.5 text-muted-foreground line-clamp-2">
                {s.detail}
              </p>
              <Button
                variant="link"
                size="sm"
                className="h-auto p-0 text-xs"
                onClick={() => onAskAbout(`Tell me more about: ${s.title}`)}
              >
                Ask about this
              </Button>
            </div>
            <Button
              variant="ghost"
              size="icon"
              className="h-6 w-6 shrink-0"
              onClick={() => onDismiss(s.id)}
            >
              <X className="h-3 w-3" />
            </Button>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

export function PatternsCard({
  patterns,
  onAskAbout,
}: {
  patterns: BriefingPattern[];
  onAskAbout: (q: string) => void;
}) {
  if (patterns.length === 0) return null;
  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-base">
          <Brain className="h-4 w-4" />
          Patterns
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {patterns.map((p, i) => (
          <div
            key={i}
            className="flex items-start gap-2 rounded-md border p-2 text-sm"
          >
            <div className="mt-0.5 shrink-0">{patternIcon(p.type)}</div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <span className="font-medium truncate">{p.summary}</span>
                <Badge variant={confidenceColor(p.confidence)} className="text-xs shrink-0">
                  {Math.round(p.confidence * 100)}%
                </Badge>
              </div>
              {p.evidence.length > 0 && (
                <p className="mt-0.5 text-muted-foreground line-clamp-1">
                  {p.evidence[0]}
                </p>
              )}
              <Button
                variant="link"
                size="sm"
                className="h-auto p-0 text-xs"
                onClick={() => onAskAbout(p.coaching_prompt || `Tell me about the ${p.type} pattern`)}
              >
                Ask about this
              </Button>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

function confidenceBadge(level: string) {
  const lower = level.toLowerCase();
  const variant = lower === "high" ? "outline" : lower === "low" ? "destructive" : "secondary";
  return (
    <Badge variant={variant} className="text-[10px] px-1.5 py-0 shrink-0">
      {level}
    </Badge>
  );
}

export function RecommendationsCard({
  recommendations,
  onAskAbout,
  token,
}: {
  recommendations: BriefingRecommendation[];
  onAskAbout: (q: string) => void;
  token?: string;
}) {
  const [expandedRecs, setExpandedRecs] = useState<Set<string>>(new Set());
  const [expandedCritic, setExpandedCritic] = useState<Set<string>>(new Set());
  const [feedbackGiven, setFeedbackGiven] = useState<Record<string, "useful" | "irrelevant">>({});

  const handleFeedback = (id: string, category: string, type: "useful" | "irrelevant") => {
    setFeedbackGiven((prev) => ({ ...prev, [id]: type }));
    if (token) {
      logEngagement(
        token,
        type === "useful" ? "feedback_useful" : "feedback_irrelevant",
        "recommendation",
        id,
        { category },
      );
    }
  };

  const toggleReasoning = (id: string) => {
    setExpandedRecs((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const toggleCritic = (id: string) => {
    setExpandedCritic((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  if (recommendations.length === 0) return null;
  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-base">
          <Lightbulb className="h-4 w-4" />
          Recommendations
        </CardTitle>
        <p className="text-[11px] text-muted-foreground mt-1">
          Informed hypotheses, not certainties. Each includes an adversarial challenge.
        </p>
      </CardHeader>
      <CardContent className="space-y-3">
        {recommendations.map((r) => (
          <div
            key={r.id}
            className="flex flex-col gap-1 rounded-md border p-2 text-sm"
          >
            <div className="flex items-start gap-2">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="font-medium truncate">{r.title}</span>
                  <Badge variant="outline" className="text-xs shrink-0">
                    {r.category}
                  </Badge>
                  {r.critic ? confidenceBadge(r.critic.confidence) : (
                    <Badge variant="secondary" className="text-xs shrink-0">
                      {r.score.toFixed(1)}
                    </Badge>
                  )}
                </div>
                {r.description && (
                  <p className="mt-0.5 text-muted-foreground line-clamp-2">
                    {r.description}
                  </p>
                )}
                <div className="flex items-center gap-2 mt-0.5 flex-wrap">
                  <Button
                    variant="link"
                    size="sm"
                    className="h-auto p-0 text-xs"
                    onClick={() => onAskAbout(`Create an action plan for: ${r.title}`)}
                  >
                    Ask about this
                  </Button>
                  {r.reasoning_trace && (
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-auto px-1 py-0 text-xs text-muted-foreground"
                      onClick={() => toggleReasoning(r.id)}
                    >
                      Why this?
                      {expandedRecs.has(r.id) ? (
                        <ChevronUp className="ml-0.5 h-3 w-3" />
                      ) : (
                        <ChevronDown className="ml-0.5 h-3 w-3" />
                      )}
                    </Button>
                  )}
                  {r.critic?.critic_challenge && (
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-auto px-1 py-0 text-xs text-muted-foreground"
                      onClick={() => toggleCritic(r.id)}
                    >
                      Why this might be wrong
                      {expandedCritic.has(r.id) ? (
                        <ChevronUp className="ml-0.5 h-3 w-3" />
                      ) : (
                        <ChevronDown className="ml-0.5 h-3 w-3" />
                      )}
                    </Button>
                  )}
                  <span className="ml-auto flex items-center gap-1">
                    {feedbackGiven[r.id] ? (
                      <span className="text-[10px] text-muted-foreground">
                        {feedbackGiven[r.id] === "useful" ? "Marked useful" : "Marked irrelevant"}
                      </span>
                    ) : (
                      <>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-6 w-6 text-muted-foreground hover:text-green-600"
                          onClick={() => handleFeedback(r.id, r.category, "useful")}
                          title="Useful"
                        >
                          <ThumbsUp className="h-3 w-3" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-6 w-6 text-muted-foreground hover:text-red-500"
                          onClick={() => handleFeedback(r.id, r.category, "irrelevant")}
                          title="Not relevant"
                        >
                          <ThumbsDown className="h-3 w-3" />
                        </Button>
                      </>
                    )}
                  </span>
                </div>
              </div>
            </div>
            {r.reasoning_trace && expandedRecs.has(r.id) && (
              <div className="mt-1 rounded-md bg-muted/50 p-2 text-xs space-y-1">
                {r.reasoning_trace.source_signal && (
                  <p><span className="font-medium">Source:</span> {r.reasoning_trace.source_signal}</p>
                )}
                {r.reasoning_trace.profile_match && (
                  <p><span className="font-medium">Match:</span> {r.reasoning_trace.profile_match}</p>
                )}
                {r.critic && (
                  <p>
                    <span className="font-medium">Confidence:</span>{" "}
                    {confidenceBadge(r.critic.confidence)}
                    {r.critic.confidence_rationale && (
                      <span className="ml-1 text-muted-foreground">{r.critic.confidence_rationale}</span>
                    )}
                  </p>
                )}
                {!r.critic && (
                  <p>
                    <span className="font-medium">Confidence:</span>{" "}
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
              <div className="mt-1 rounded-md border border-amber-200 dark:border-amber-800 bg-amber-50/50 dark:bg-amber-950/20 p-2 text-xs space-y-1.5">
                {r.critic.critic_challenge && (
                  <p>
                    <span className="font-medium">Challenge:</span> {r.critic.critic_challenge}
                  </p>
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
      </CardContent>
    </Card>
  );
}

export function StaleGoalsCard({
  goals,
  onAskAbout,
}: {
  goals: BriefingGoal[];
  onAskAbout: (q: string) => void;
}) {
  if (goals.length === 0) return null;
  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-base">
          <Target className="h-4 w-4" />
          Stale Goals
          <Badge variant="secondary" className="ml-auto text-xs">
            {goals.length}
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {goals.map((g) => (
          <div
            key={g.path}
            className="flex items-start gap-2 rounded-md border p-2 text-sm"
          >
            <Clock className="mt-0.5 h-4 w-4 shrink-0 text-muted-foreground" />
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <span className="font-medium truncate">{g.title}</span>
                <Badge variant="outline" className="text-xs shrink-0">
                  {g.days_since_check}d ago
                </Badge>
              </div>
              <Button
                variant="link"
                size="sm"
                className="h-auto p-0 text-xs"
                onClick={() => onAskAbout(`Help me make progress on: ${g.title}`)}
              >
                Ask about this
              </Button>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
