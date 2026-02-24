"use client";

import { useRef, useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import ReactMarkdown from "react-markdown";
import {
  Brain,
  BookOpen,
  Newspaper,
  Target,
  Sparkles,
  Send,
  FlaskConical,
  ArrowRight,
} from "lucide-react";
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
import { useToken } from "@/hooks/useToken";
import { apiFetch } from "@/lib/api";
import { toast } from "sonner";

type Phase = "intro" | "welcome" | "chat" | "done";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

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

export default function OnboardingPage() {
  const token = useToken();
  const router = useRouter();
  const [phase, setPhase] = useState<Phase>("intro");
  const [provider, setProvider] = useState("auto");
  const [apiKey, setApiKey] = useState("");
  const [saving, setSaving] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [goalsCreated, setGoalsCreated] = useState(0);
  const [turn, setTurn] = useState(0);
  const [hasApiKey, setHasApiKey] = useState<boolean | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Check if user already has API key to skip welcome phase
  useEffect(() => {
    if (!token) return;
    apiFetch<{ llm_api_key_set: boolean }>("/api/settings", {}, token)
      .then((s) => {
        setHasApiKey(s.llm_api_key_set);
        if (s.llm_api_key_set) setPhase("chat");
      })
      .catch(() => setHasApiKey(false));
  }, [token]);

  // Auto-start chat when entering chat phase
  useEffect(() => {
    if (phase !== "chat" || !token || messages.length > 0) return;
    (async () => {
      setSending(true);
      try {
        const res = await apiFetch<{ message: string; done: boolean; turn: number }>(
          "/api/onboarding/start",
          { method: "POST" },
          token
        );
        setMessages([{ role: "assistant", content: res.message }]);
        setTurn(res.turn);
      } catch (e) {
        toast.error((e as Error).message);
      } finally {
        setSending(false);
      }
    })();
  }, [phase, token, messages.length]);

  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages, sending]);

  const handleDone = useCallback(() => {
    router.replace("/");
  }, [router]);

  // Auto-redirect after done
  useEffect(() => {
    if (phase === "done") {
      const timer = setTimeout(handleDone, 3000);
      return () => clearTimeout(timer);
    }
  }, [phase, handleDone]);

  const [testing, setTesting] = useState(false);

  const handleSaveKey = async () => {
    if (!apiKey.trim()) {
      toast.error("Please enter an API key");
      return;
    }
    if (!token) return;
    setSaving(true);
    try {
      const payload: Record<string, string> = { llm_api_key: apiKey };
      if (provider !== "auto") payload.llm_provider = provider;
      await apiFetch(
        "/api/settings",
        { method: "PUT", body: JSON.stringify(payload) },
        token
      );

      // Connectivity test
      setTesting(true);
      try {
        await apiFetch<{ ok: boolean; provider: string }>(
          "/api/settings/test-llm",
          { method: "POST" },
          token
        );
        toast.success("Connected to LLM");
      } catch (e) {
        toast.error(`Key saved but LLM test failed: ${(e as Error).message}`);
      } finally {
        setTesting(false);
      }

      setPhase("chat");
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setSaving(false);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || sending || !token) return;
    const text = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setSending(true);

    try {
      const res = await apiFetch<{
        message: string;
        done: boolean;
        goals_created: number;
        turn: number;
      }>(
        "/api/onboarding/chat",
        { method: "POST", body: JSON.stringify({ message: text }) },
        token
      );
      setMessages((prev) => [...prev, { role: "assistant", content: res.message }]);
      setTurn(res.turn);
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

  if (!token || hasApiKey === null) return null;

  return (
    <div className="flex h-full items-center justify-center p-4">
      <div className="flex w-full max-w-2xl flex-col rounded-xl border bg-card shadow-sm"
        style={{ height: "min(85vh, 720px)" }}>

        {phase === "intro" && (
          <div className="flex flex-1 flex-col overflow-hidden">
            <div className="px-6 pt-6 pb-2 text-center">
              <div className="mx-auto mb-2 flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
                <Brain className="h-6 w-6 text-primary" />
              </div>
              <h1 className="text-xl font-semibold text-primary">StewardMe</h1>
              <p className="text-sm text-muted-foreground">
                Your AI steward for navigating rapid change
              </p>
            </div>

            <div className="flex-1 space-y-4 overflow-y-auto px-6 py-4">
              {introSections.map(({ icon: Icon, title, description }) => (
                <div key={title} className="flex gap-3">
                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-muted">
                    <Icon className="h-4 w-4 text-muted-foreground" />
                  </div>
                  <div>
                    <p className="text-sm font-medium">{title}</p>
                    <p className="text-xs text-muted-foreground leading-relaxed">
                      {description}
                    </p>
                  </div>
                </div>
              ))}
              <div className="rounded-lg border bg-muted/50 p-3 text-xs text-muted-foreground leading-relaxed">
                <span className="font-medium text-foreground">How it connects:</span>{" "}
                your journal and intel radar feed your steward. Goals shape what
                surfaces. The more context you provide, the sharper the guidance.
              </div>
            </div>

            <div className="space-y-2 px-6 pb-6">
              <Button
                onClick={() => setPhase(hasApiKey ? "chat" : "welcome")}
                className="w-full"
              >
                Continue
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
              <Button
                variant="ghost"
                onClick={() => router.replace("/")}
                className="w-full text-muted-foreground"
              >
                Skip for Now
              </Button>
            </div>
          </div>
        )}

        {phase === "welcome" && (
          <div className="flex flex-1 flex-col overflow-hidden">
            <div className="px-6 pt-6 pb-2 text-center">
              <div className="mx-auto mb-2 flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
                <Brain className="h-6 w-6 text-primary" />
              </div>
              <h1 className="text-xl font-semibold">
                <span className="text-primary">StewardMe</span>
              </h1>
              <p className="text-sm text-muted-foreground">
                Let&apos;s set up your AI steward
              </p>
            </div>

            <div className="flex-1 space-y-6 overflow-y-auto px-6 py-4">
              <div className="rounded-lg border bg-muted/50 p-3 text-xs text-muted-foreground">
                An LLM API key is required for the Advisor. Your key is encrypted and
                stored per-user.
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

            <div className="space-y-2 px-6 pb-6">
              <Button
                onClick={handleSaveKey}
                disabled={saving || testing}
                className="w-full"
              >
                {testing ? "Testing connection..." : saving ? "Saving..." : "Get Started"}
              </Button>
              <Button
                variant="ghost"
                onClick={() => router.replace("/")}
                className="w-full text-muted-foreground"
              >
                Skip for Now
              </Button>
            </div>
          </div>
        )}

        {phase === "chat" && (
          <div className="flex flex-1 flex-col overflow-hidden">
            <div className="px-6 pt-5 pb-3 border-b">
              <h2 className="text-base font-semibold">
                Let&apos;s set up your profile
              </h2>
              <p className="text-sm text-muted-foreground">
                Answer a few questions so we can personalize your experience
              </p>
            </div>

            <div className="px-6 pt-2">
              <div className="flex items-center justify-between text-xs text-muted-foreground mb-1">
                <span>Question {turn} of ~8</span>
                <span>{Math.min(100, Math.round((turn / 8) * 100))}%</span>
              </div>
              <div className="h-1.5 w-full rounded-full bg-muted overflow-hidden">
                <div
                  className="h-full rounded-full bg-primary transition-all duration-500"
                  style={{ width: `${Math.min(100, (turn / 8) * 100)}%` }}
                />
              </div>
            </div>

            <div
              ref={scrollRef}
              className="flex-1 space-y-3 overflow-y-auto px-6 py-4"
            >
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

            <div className="border-t px-6 py-3">
              <div className="flex gap-2">
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
                <Button
                  size="icon"
                  onClick={handleSend}
                  disabled={sending || !input.trim()}
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
              <Button
                variant="ghost"
                onClick={() => router.replace("/")}
                className="mt-1 w-full text-xs text-muted-foreground"
              >
                Skip — I&apos;ll set up my profile later
              </Button>
            </div>
          </div>
        )}

        {phase === "done" && (
          <div className="flex flex-1 flex-col items-center justify-center px-6">
            <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/30">
              <Sparkles className="h-6 w-6 text-green-600 dark:text-green-400" />
            </div>
            <h2 className="text-xl font-semibold">You&apos;re all set!</h2>
            <p className="mt-1 text-sm text-muted-foreground text-center">
              Profile created
              {goalsCreated > 0
                ? ` and ${goalsCreated} goal${goalsCreated > 1 ? "s" : ""} set up`
                : ""}{" "}
              — your steward is ready.
            </p>
            <Button onClick={handleDone} className="mt-6">
              Go to Dashboard
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
