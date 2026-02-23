"use client";

import { useRef, useCallback, useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { Brain, BookOpen, Newspaper, Target, Sparkles, Send, FlaskConical, ArrowRight } from "lucide-react";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
  SheetFooter,
} from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { apiFetch } from "@/lib/api";
import { toast } from "sonner";

interface OnboardingDialogProps {
  open: boolean;
  onClose: () => void;
  onComplete?: () => void;
  token: string;
  startPhase?: Phase;
}

type Phase = "intro" | "welcome" | "chat" | "done";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

const features = [
  { icon: Newspaper, text: "Surface what matters from HN, GitHub, arXiv, Reddit & RSS" },
  { icon: Sparkles, text: "Proactive advice grounded in your context + world intel" },
  { icon: Target, text: "Align goals against market trends and opportunities" },
  { icon: BookOpen, text: "Journal reflections that train your personal AI" },
];

const introSections = [
  {
    icon: Newspaper,
    title: "Intelligence Radar",
    description:
      "Continuously scans Hacker News, GitHub trending, arXiv, Reddit, and RSS feeds. Surfaces what matters to you without the noise.",
  },
  {
    icon: Brain,
    title: "AI Steward",
    description:
      "Proactive advice grounded in your context and world intel. Helps you navigate change, spot opportunities, and stay ahead.",
  },
  {
    icon: Target,
    title: "Goal Alignment",
    description:
      "Tracks your objectives against market trends and emerging opportunities. Flags when priorities should shift.",
  },
  {
    icon: BookOpen,
    title: "Journal",
    description:
      "Capture reflections, decisions, and observations. Every entry trains your personal AI to give sharper, more relevant guidance.",
  },
  {
    icon: FlaskConical,
    title: "Deep Research",
    description:
      "On-demand analysis of emerging opportunities, technologies, or trends drawn from your goals and interests.",
  },
];

export function OnboardingDialog({ open, onClose, onComplete, token, startPhase = "intro" }: OnboardingDialogProps) {
  const [phase, setPhase] = useState<Phase>(startPhase);
  const [provider, setProvider] = useState("auto");
  const [apiKey, setApiKey] = useState("");
  const [saving, setSaving] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [goalsCreated, setGoalsCreated] = useState(0);
  const scrollRef = useRef<HTMLDivElement>(null);

  const handleClose = useCallback((completed = false) => {
    if (completed && onComplete) onComplete();
    onClose();
  }, [onClose, onComplete]);

  // When opening in chat phase directly, start the interview
  useEffect(() => {
    if (!open) return;
    setPhase(startPhase);
    setMessages([]);
    setGoalsCreated(0);
    if (startPhase === "chat") {
      (async () => {
        setSending(true);
        try {
          const res = await apiFetch<{ message: string; done: boolean }>(
            "/api/onboarding/start",
            { method: "POST" },
            token
          );
          setMessages([{ role: "assistant", content: res.message }]);
        } catch (e) {
          toast.error((e as Error).message);
        } finally {
          setSending(false);
        }
      })();
    }
  }, [open, startPhase, token]);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, sending]);

  // Auto-close after done
  useEffect(() => {
    if (phase === "done") {
      const timer = setTimeout(() => {
        handleClose(true);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [phase, handleClose]);

  const handleSaveKey = async () => {
    if (!apiKey.trim()) {
      toast.error("Please enter an API key");
      return;
    }
    setSaving(true);
    try {
      const payload: Record<string, string> = { llm_api_key: apiKey };
      if (provider !== "auto") payload.llm_provider = provider;
      await apiFetch("/api/settings", { method: "PUT", body: JSON.stringify(payload) }, token);

      // Start onboarding chat
      setSending(true);
      const res = await apiFetch<{ message: string; done: boolean }>(
        "/api/onboarding/start",
        { method: "POST" },
        token
      );
      setMessages([{ role: "assistant", content: res.message }]);
      setPhase("chat");
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setSaving(false);
      setSending(false);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || sending) return;
    const text = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setSending(true);

    try {
      const res = await apiFetch<{ message: string; done: boolean; goals_created: number }>(
        "/api/onboarding/chat",
        { method: "POST", body: JSON.stringify({ message: text }) },
        token
      );
      setMessages((prev) => [...prev, { role: "assistant", content: res.message }]);
      if (res.done) {
        setGoalsCreated(res.goals_created);
        setPhase("done");
      }
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setSending(false);
    }
  };

  return (
    <Sheet open={open} onOpenChange={(v) => !v && handleClose()}>
      <SheetContent side="right" className="flex flex-col sm:max-w-lg overflow-hidden">
        {phase === "intro" && (
          <>
            <SheetHeader>
              <div className="mx-auto mb-1 flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
                <Brain className="h-6 w-6 text-primary" />
              </div>
              <SheetTitle className="text-center text-xl">StewardMe</SheetTitle>
              <SheetDescription className="text-center">
                Your AI steward for navigating rapid change
              </SheetDescription>
            </SheetHeader>

            <div className="flex-1 space-y-4 overflow-y-auto px-4 py-2">
              {introSections.map(({ icon: Icon, title, description }) => (
                <div key={title} className="flex gap-3">
                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-muted">
                    <Icon className="h-4 w-4 text-muted-foreground" />
                  </div>
                  <div>
                    <p className="text-sm font-medium">{title}</p>
                    <p className="text-xs text-muted-foreground leading-relaxed">{description}</p>
                  </div>
                </div>
              ))}

              <div className="rounded-lg border bg-muted/50 p-3 text-xs text-muted-foreground leading-relaxed">
                <span className="font-medium text-foreground">How it all connects:</span> your journal and intel radar feed into your steward. Goals shape what opportunities surface. Research fills knowledge gaps. The more context you provide, the sharper the guidance.
              </div>
            </div>

            <SheetFooter>
              <Button onClick={() => setPhase("welcome")} className="w-full">
                Continue
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
              <Button variant="ghost" onClick={() => handleClose()} className="w-full text-muted-foreground">
                Skip for Now
              </Button>
            </SheetFooter>
          </>
        )}

        {phase === "welcome" && (
          <>
            <SheetHeader>
              <div className="mx-auto mb-1 flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
                <Brain className="h-6 w-6 text-primary" />
              </div>
              <SheetTitle className="text-center text-xl">Welcome to StewardMe</SheetTitle>
              <SheetDescription className="text-center">
                Let&apos;s set up your AI steward for navigating what&apos;s next
              </SheetDescription>
            </SheetHeader>

            <div className="space-y-6 px-4 flex-1 overflow-y-auto">
              <div className="space-y-3">
                {features.map(({ icon: Icon, text }) => (
                  <div key={text} className="flex items-center gap-3 text-sm">
                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-muted">
                      <Icon className="h-4 w-4 text-muted-foreground" />
                    </div>
                    <span>{text}</span>
                  </div>
                ))}
              </div>

              <div className="rounded-lg border bg-muted/50 p-3 text-xs text-muted-foreground">
                An LLM API key is required for the Advisor. Your key is encrypted and stored per-user — it never leaves the server unencrypted.
              </div>

              <div className="space-y-4">
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
                  />
                </div>
              </div>
            </div>

            <SheetFooter>
              <Button onClick={handleSaveKey} disabled={saving} className="w-full">
                {saving ? "Setting up..." : "Get Started"}
              </Button>
              <Button variant="ghost" onClick={() => handleClose()} className="w-full text-muted-foreground">
                Skip for Now
              </Button>
            </SheetFooter>
          </>
        )}

        {phase === "chat" && (
          <>
            <SheetHeader>
              <SheetTitle className="text-base">Let&apos;s set up your profile</SheetTitle>
              <SheetDescription>
                Answer a few questions so we can personalize your experience
              </SheetDescription>
            </SheetHeader>

            <div ref={scrollRef} className="flex-1 space-y-3 overflow-y-auto px-4 py-2">
              {messages.map((msg, i) => (
                <div
                  key={i}
                  className={
                    msg.role === "user"
                      ? "ml-8 rounded-lg bg-primary/10 px-3 py-2 text-sm"
                      : "mr-8 rounded-lg bg-muted px-3 py-2 text-sm"
                  }
                >
                  {msg.role === "assistant" ? (
                    <div className="prose prose-sm max-w-none dark:prose-invert">
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    </div>
                  ) : (
                    msg.content
                  )}
                </div>
              ))}
              {sending && (
                <div className="mr-8 rounded-lg bg-muted px-3 py-3">
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <div className="flex gap-1">
                      <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:0ms]" />
                      <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:150ms]" />
                      <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:300ms]" />
                    </div>
                    Thinking...
                  </div>
                </div>
              )}
            </div>

            <div className="flex gap-2 px-4 pb-2">
              <Textarea
                placeholder="Type your answer..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSend();
                  }
                }}
                disabled={sending}
                rows={2}
                className="flex-1 max-h-32"
              />
              <Button size="icon" onClick={handleSend} disabled={sending || !input.trim()}>
                <Send className="h-4 w-4" />
              </Button>
            </div>
            <div className="px-4 pb-2">
              <Button variant="ghost" onClick={() => handleClose()} className="w-full text-xs text-muted-foreground">
                Skip — I&apos;ll set up my profile later
              </Button>
            </div>
          </>
        )}

        {phase === "done" && (
          <>
            <SheetHeader>
              <div className="mx-auto mb-1 flex h-12 w-12 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/30">
                <Sparkles className="h-6 w-6 text-green-600 dark:text-green-400" />
              </div>
              <SheetTitle className="text-center text-xl">You&apos;re all set!</SheetTitle>
              <SheetDescription className="text-center">
                Profile created{goalsCreated > 0 ? ` and ${goalsCreated} goal${goalsCreated > 1 ? "s" : ""} set up` : ""} — your steward is ready.
              </SheetDescription>
            </SheetHeader>

            <div className="flex-1" />

            <SheetFooter>
              <Button onClick={() => handleClose(true)} className="w-full">
                Go to Dashboard
              </Button>
            </SheetFooter>
          </>
        )}
      </SheetContent>
    </Sheet>
  );
}
