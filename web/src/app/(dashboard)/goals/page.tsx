"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { useToken } from "@/hooks/useToken";
import { CheckCircle2, Circle, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { apiFetch } from "@/lib/api";

interface Milestone {
  title: string;
  completed: boolean;
  completed_at?: string;
}

interface Goal {
  path: string;
  title: string;
  status: string;
  created: string;
  last_checked: string;
  check_in_days: number;
  days_since_check: number;
  is_stale: boolean;
  milestones?: Milestone[];
}

interface Progress {
  percent: number;
  completed: number;
  total: number;
  milestones: Milestone[];
}

export default function GoalsPage() {
  const token = useToken();
  const [goals, setGoals] = useState<Goal[]>([]);
  const [form, setForm] = useState({ title: "", content: "", tags: "" });
  const [creating, setCreating] = useState(false);
  const [selectedGoal, setSelectedGoal] = useState<string | null>(null);
  const [progress, setProgress] = useState<Progress | null>(null);
  const [milestoneTitle, setMilestoneTitle] = useState("");
  const [checkInNotes, setCheckInNotes] = useState("");

  const loadGoals = () => {
    if (!token) return;
    apiFetch<Goal[]>("/api/goals?include_inactive=true", {}, token)
      .then(setGoals)
      .catch((e) => toast.error(e.message));
  };

  useEffect(loadGoals, [token]);

  const loadProgress = async (path: string) => {
    if (!token) return;
    try {
      const p = await apiFetch<Progress>(
        `/api/goals/${encodeURIComponent(path)}/progress`,
        {},
        token
      );
      setProgress(p);
    } catch {
      setProgress(null);
    }
  };

  const handleCreate = async () => {
    if (!token || !form.title) return;
    setCreating(true);
    try {
      await apiFetch(
        "/api/goals",
        {
          method: "POST",
          body: JSON.stringify({
            ...form,
            tags: form.tags ? form.tags.split(",").map((t) => t.trim()) : undefined,
          }),
        },
        token
      );
      setForm({ title: "", content: "", tags: "" });
      toast.success("Goal created");
      loadGoals();
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setCreating(false);
    }
  };

  const handleCheckIn = async (path: string) => {
    if (!token) return;
    try {
      await apiFetch(
        `/api/goals/${encodeURIComponent(path)}/check-in`,
        { method: "POST", body: JSON.stringify({ notes: checkInNotes || null }) },
        token
      );
      setCheckInNotes("");
      toast.success("Checked in");
      loadGoals();
      loadProgress(path);
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  const handleStatusChange = async (path: string, status: string) => {
    if (!token) return;
    try {
      await apiFetch(
        `/api/goals/${encodeURIComponent(path)}/status`,
        { method: "PUT", body: JSON.stringify({ status }) },
        token
      );
      toast.success(`Status: ${status}`);
      loadGoals();
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  const handleAddMilestone = async (path: string) => {
    if (!token || !milestoneTitle) return;
    try {
      await apiFetch(
        `/api/goals/${encodeURIComponent(path)}/milestones`,
        { method: "POST", body: JSON.stringify({ title: milestoneTitle }) },
        token
      );
      setMilestoneTitle("");
      toast.success("Milestone added");
      loadProgress(path);
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  const handleCompleteMilestone = async (path: string, index: number) => {
    if (!token) return;
    try {
      await apiFetch(
        `/api/goals/${encodeURIComponent(path)}/milestones/complete`,
        { method: "POST", body: JSON.stringify({ milestone_index: index }) },
        token
      );
      toast.success("Milestone completed");
      loadProgress(path);
      loadGoals();
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  const statusColor: Record<string, string> = {
    active: "default",
    paused: "secondary",
    completed: "outline",
    abandoned: "destructive",
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Goals</h1>
        <Sheet>
          <SheetTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" /> New Goal
            </Button>
          </SheetTrigger>
          <SheetContent>
            <SheetHeader>
              <SheetTitle>New Goal</SheetTitle>
            </SheetHeader>
            <div className="mt-6 space-y-4">
              <div className="space-y-1.5">
                <Label>Title</Label>
                <Input
                  value={form.title}
                  onChange={(e) => setForm({ ...form, title: e.target.value })}
                />
              </div>
              <div className="space-y-1.5">
                <Label>Description</Label>
                <Textarea
                  rows={6}
                  value={form.content}
                  onChange={(e) => setForm({ ...form, content: e.target.value })}
                />
              </div>
              <div className="space-y-1.5">
                <Label>Tags (comma-separated)</Label>
                <Input
                  value={form.tags}
                  onChange={(e) => setForm({ ...form, tags: e.target.value })}
                />
              </div>
              <Button onClick={handleCreate} disabled={creating || !form.title}>
                {creating ? "Creating..." : "Create Goal"}
              </Button>
            </div>
          </SheetContent>
        </Sheet>
      </div>

      {/* Goals list */}
      <div className="space-y-4">
        {goals.map((g) => (
          <Card key={g.path}>
            <CardHeader
              className="cursor-pointer pb-2"
              onClick={() => {
                setSelectedGoal(selectedGoal === g.path ? null : g.path);
                if (selectedGoal !== g.path) loadProgress(g.path);
              }}
            >
              <div className="flex items-center justify-between">
                <CardTitle className="text-base">{g.title}</CardTitle>
                <div className="flex gap-2">
                  {g.is_stale && (
                    <Badge variant="destructive">Stale</Badge>
                  )}
                  <Badge variant={statusColor[g.status] as "default" | "secondary" | "outline" | "destructive"}>
                    {g.status}
                  </Badge>
                </div>
              </div>
              <CardDescription>
                Last check-in: {g.days_since_check}d ago
              </CardDescription>
            </CardHeader>

            {selectedGoal === g.path && (
              <CardContent className="space-y-4">
                {/* Progress */}
                {progress && progress.total > 0 && (
                  <div>
                    <div className="mb-2 text-sm font-medium">
                      Progress: {progress.percent}% ({progress.completed}/{progress.total})
                    </div>
                    <div className="h-2 w-full rounded-full bg-muted">
                      <div
                        className="h-full rounded-full bg-primary transition-all"
                        style={{ width: `${progress.percent}%` }}
                      />
                    </div>
                  </div>
                )}

                {/* Milestones */}
                {progress?.milestones && (
                  <div className="space-y-2">
                    <h4 className="text-sm font-medium">Milestones</h4>
                    {progress.milestones.map((m, i) => (
                      <div
                        key={i}
                        className="flex items-center gap-2 text-sm"
                      >
                        {m.completed ? (
                          <CheckCircle2 className="h-4 w-4 text-green-500" />
                        ) : (
                          <button onClick={() => handleCompleteMilestone(g.path, i)}>
                            <Circle className="h-4 w-4 text-muted-foreground hover:text-primary" />
                          </button>
                        )}
                        <span className={m.completed ? "line-through text-muted-foreground" : ""}>
                          {m.title}
                        </span>
                      </div>
                    ))}
                    <div className="flex gap-2">
                      <Input
                        placeholder="New milestone"
                        value={milestoneTitle}
                        onChange={(e) => setMilestoneTitle(e.target.value)}
                        className="text-sm"
                      />
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleAddMilestone(g.path)}
                        disabled={!milestoneTitle}
                      >
                        Add
                      </Button>
                    </div>
                  </div>
                )}

                {/* Check-in */}
                <div className="space-y-2">
                  <h4 className="text-sm font-medium">Check In</h4>
                  <Textarea
                    rows={2}
                    placeholder="Progress notes..."
                    value={checkInNotes}
                    onChange={(e) => setCheckInNotes(e.target.value)}
                  />
                  <Button
                    size="sm"
                    onClick={() => handleCheckIn(g.path)}
                  >
                    Check In
                  </Button>
                </div>

                {/* Status actions */}
                <div className="flex gap-2">
                  {g.status !== "completed" && (
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleStatusChange(g.path, "completed")}
                    >
                      Complete
                    </Button>
                  )}
                  {g.status === "active" && (
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleStatusChange(g.path, "paused")}
                    >
                      Pause
                    </Button>
                  )}
                  {g.status === "paused" && (
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleStatusChange(g.path, "active")}
                    >
                      Resume
                    </Button>
                  )}
                </div>
              </CardContent>
            )}
          </Card>
        ))}
        {goals.length === 0 && (
          <p className="text-muted-foreground">No goals yet. Create one to get started.</p>
        )}
      </div>
    </div>
  );
}
