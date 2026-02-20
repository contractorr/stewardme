"use client";

import { useRef, useEffect, useState } from "react";
import { toast } from "sonner";
import ReactMarkdown from "react-markdown";
import { Brain, Send } from "lucide-react";
import { useToken } from "@/hooks/useToken";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { apiFetch } from "@/lib/api";

interface Message {
  role: "user" | "assistant";
  content: string;
  advice_type?: string;
}

export default function AdvisorPage() {
  const token = useToken();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [adviceType, setAdviceType] = useState("general");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = async () => {
    if (!token || !input.trim()) return;
    const question = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setLoading(true);

    try {
      const res = await apiFetch<{ answer: string; advice_type: string }>(
        "/api/advisor/ask",
        {
          method: "POST",
          body: JSON.stringify({ question, advice_type: adviceType }),
        },
        token
      );
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: res.answer, advice_type: res.advice_type },
      ]);
    } catch (e) {
      toast.error((e as Error).message);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Error: " + (e as Error).message },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Advisor</h1>
        <Select value={adviceType} onValueChange={setAdviceType}>
          <SelectTrigger className="w-40">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="general">General</SelectItem>
            <SelectItem value="career">Career</SelectItem>
            <SelectItem value="goals">Goals</SelectItem>
            <SelectItem value="opportunities">Opportunities</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Chat messages */}
      <div ref={scrollRef} className="mt-4 flex-1 space-y-4 overflow-y-auto">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-muted">
              <Brain className="h-7 w-7 text-muted-foreground" />
            </div>
            <h3 className="text-lg font-medium">Ask your AI advisor</h3>
            <p className="mt-1 max-w-md text-sm text-muted-foreground">
              Get personalized advice powered by your journal entries and
              intelligence data. Try asking about career moves, goal strategies,
              or emerging opportunities.
            </p>
          </div>
        )}
        {messages.map((msg, i) => (
          <Card
            key={i}
            className={
              msg.role === "user" ? "ml-12 bg-primary/5" : "mr-12"
            }
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
                Thinking...
              </div>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Input */}
      <div className="mt-4 flex gap-2">
        <Textarea
          rows={2}
          placeholder="Ask a question..."
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
        <Button onClick={handleSend} disabled={loading || !input.trim()}>
          <Send className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
