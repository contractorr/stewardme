"use client";

import { useState } from "react";
import { toast } from "sonner";
import { Send } from "lucide-react";
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
      <div className="mt-4 flex-1 space-y-4 overflow-y-auto">
        {messages.length === 0 && (
          <p className="text-center text-muted-foreground">
            Ask your AI advisor anything. It uses your journal entries and
            intelligence data for context.
          </p>
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
              <div className="whitespace-pre-wrap text-sm">{msg.content}</div>
            </CardContent>
          </Card>
        ))}
        {loading && (
          <Card className="mr-12">
            <CardContent className="py-4">
              <div className="text-sm text-muted-foreground">Thinking...</div>
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
