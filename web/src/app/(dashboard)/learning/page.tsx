"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import ReactMarkdown from "react-markdown";
import { GraduationCap, Plus, ChevronDown, ChevronUp } from "lucide-react";
import { useToken } from "@/hooks/useToken";
import { apiFetch } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import type { LearningPath } from "@/types/learning";

function PathSkeleton() {
  return (
    <Card>
      <CardHeader className="pb-2">
        <div className="h-5 w-1/3 animate-pulse rounded bg-muted" />
        <div className="h-3 w-1/4 animate-pulse rounded bg-muted" />
      </CardHeader>
      <CardContent>
        <div className="h-2 w-full animate-pulse rounded bg-muted" />
      </CardContent>
    </Card>
  );
}

function statusBadge(status: string) {
  const variant =
    status === "completed"
      ? "default"
      : status === "active"
        ? "secondary"
        : "outline";
  return <Badge variant={variant}>{status}</Badge>;
}

export default function LearningPage() {
  const token = useToken();
  const [paths, setPaths] = useState<LearningPath[]>([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<string | null>(null);
  const [expandedContent, setExpandedContent] = useState<Record<string, string>>({});
  const [generating, setGenerating] = useState(false);
  const [sheetOpen, setSheetOpen] = useState(false);
  const [hasKey, setHasKey] = useState(true);

  // Generate form
  const [skill, setSkill] = useState("");
  const [currentLevel, setCurrentLevel] = useState("1");
  const [targetLevel, setTargetLevel] = useState("4");

  const loadPaths = () => {
    if (!token) {
      setLoading(false);
      return;
    }
    apiFetch<LearningPath[]>("/api/learning", {}, token)
      .then(setPaths)
      .catch((e) => toast.error(e.message))
      .finally(() => setLoading(false));
  };

  useEffect(loadPaths, [token]);

  // Check if LLM key configured
  useEffect(() => {
    if (!token) return;
    apiFetch<{ llm_api_key_set: boolean }>("/api/settings", {}, token)
      .then((s) => setHasKey(s.llm_api_key_set))
      .catch(() => {});
  }, [token]);

  const toggleExpand = async (id: string) => {
    if (expanded === id) {
      setExpanded(null);
      return;
    }
    setExpanded(id);
    if (!expandedContent[id] && token) {
      try {
        const detail = await apiFetch<LearningPath>(
          `/api/learning/${id}`,
          {},
          token
        );
        if (detail.content) {
          setExpandedContent((prev) => ({ ...prev, [id]: detail.content! }));
        }
      } catch (e) {
        toast.error((e as Error).message);
      }
    }
  };

  const handleProgressUpdate = async (id: string, current: number, total: number) => {
    if (!token) return;
    const next = Math.min(current + 1, total);
    try {
      await apiFetch(`/api/learning/${id}/progress`, {
        method: "POST",
        body: JSON.stringify({ completed_modules: next }),
      }, token);
      toast.success(`Module ${next}/${total} completed`);
      loadPaths();
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  const handleGenerate = async () => {
    if (!token || !skill.trim()) return;
    setGenerating(true);
    try {
      await apiFetch("/api/learning/generate", {
        method: "POST",
        body: JSON.stringify({
          skill: skill.trim(),
          current_level: parseInt(currentLevel),
          target_level: parseInt(targetLevel),
        }),
      }, token);
      toast.success("Learning path generated");
      setSheetOpen(false);
      setSkill("");
      setCurrentLevel("1");
      setTargetLevel("4");
      setLoading(true);
      loadPaths();
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Learning Paths</h1>
        <Sheet open={sheetOpen} onOpenChange={setSheetOpen}>
          <SheetTrigger asChild>
            <Button disabled={!hasKey}>
              <Plus className="mr-2 h-4 w-4" />
              Generate Path
            </Button>
          </SheetTrigger>
          <SheetContent className="sm:max-w-lg overflow-y-auto">
            <SheetHeader>
              <SheetTitle>Generate Learning Path</SheetTitle>
            </SheetHeader>
            <div className="mt-6 space-y-4">
              <div>
                <Label htmlFor="skill">Skill</Label>
                <Input
                  id="skill"
                  placeholder="e.g. Kubernetes, Rust, System Design"
                  value={skill}
                  onChange={(e) => setSkill(e.target.value)}
                />
              </div>
              <div className="flex gap-4">
                <div className="flex-1">
                  <Label>Current Level</Label>
                  <Select value={currentLevel} onValueChange={setCurrentLevel}>
                    <SelectTrigger className="w-full">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {[1, 2, 3, 4, 5].map((l) => (
                        <SelectItem key={l} value={String(l)}>
                          {l} — {["Beginner", "Novice", "Intermediate", "Advanced", "Expert"][l - 1]}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="flex-1">
                  <Label>Target Level</Label>
                  <Select value={targetLevel} onValueChange={setTargetLevel}>
                    <SelectTrigger className="w-full">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {[1, 2, 3, 4, 5].map((l) => (
                        <SelectItem key={l} value={String(l)}>
                          {l} — {["Beginner", "Novice", "Intermediate", "Advanced", "Expert"][l - 1]}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <Button
                onClick={handleGenerate}
                disabled={generating || !skill.trim()}
                className="w-full"
              >
                {generating ? "Generating..." : "Generate"}
              </Button>
            </div>
          </SheetContent>
        </Sheet>
      </div>

      {!hasKey && (
        <p className="text-sm text-muted-foreground">
          Set an LLM API key in Settings to generate new paths.
        </p>
      )}

      {loading && (
        <div className="space-y-3">
          {Array.from({ length: 3 }).map((_, i) => (
            <PathSkeleton key={i} />
          ))}
        </div>
      )}

      {!loading && paths.length === 0 && (
        <div className="flex flex-col items-center justify-center py-16 text-center">
          <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-muted">
            <GraduationCap className="h-7 w-7 text-muted-foreground" />
          </div>
          <h3 className="text-lg font-medium">No learning paths yet</h3>
          <p className="mt-1 max-w-sm text-sm text-muted-foreground">
            Generate one to get a structured curriculum for any skill.
          </p>
        </div>
      )}

      {!loading && paths.length > 0 && (
        <div className="space-y-3">
          {paths.map((p) => (
            <Card key={p.id}>
              <CardHeader
                className="cursor-pointer pb-2"
                onClick={() => toggleExpand(p.id)}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-base">{p.skill}</CardTitle>
                    <CardDescription>
                      {p.completed_modules}/{p.total_modules} modules ·{" "}
                      {new Date(p.updated_at).toLocaleDateString()}
                    </CardDescription>
                  </div>
                  <div className="flex items-center gap-2">
                    {statusBadge(p.status)}
                    {expanded === p.id ? (
                      <ChevronUp className="h-4 w-4 text-muted-foreground" />
                    ) : (
                      <ChevronDown className="h-4 w-4 text-muted-foreground" />
                    )}
                  </div>
                </div>
                {/* Progress bar */}
                <div className="mt-2 h-2 w-full rounded-full bg-muted">
                  <div
                    className="h-2 rounded-full bg-primary transition-all"
                    style={{ width: `${p.progress}%` }}
                  />
                </div>
              </CardHeader>

              {expanded === p.id && (
                <CardContent className="space-y-4">
                  {p.status !== "completed" && (
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleProgressUpdate(p.id, p.completed_modules, p.total_modules);
                      }}
                      disabled={p.completed_modules >= p.total_modules}
                    >
                      Complete Next Module
                    </Button>
                  )}
                  {expandedContent[p.id] ? (
                    <div className="prose prose-sm dark:prose-invert max-w-none">
                      <ReactMarkdown>{expandedContent[p.id]}</ReactMarkdown>
                    </div>
                  ) : (
                    <div className="h-20 animate-pulse rounded bg-muted" />
                  )}
                </CardContent>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
