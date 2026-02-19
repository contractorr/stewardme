"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { useToken } from "@/hooks/useToken";
import { Plus } from "lucide-react";
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
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { apiFetch } from "@/lib/api";

interface JournalEntry {
  path: string;
  title: string;
  type: string;
  created: string | null;
  tags: string[];
  preview: string;
  content?: string;
}

export default function JournalPage() {
  const token = useToken();
  const [entries, setEntries] = useState<JournalEntry[]>([]);
  const [selected, setSelected] = useState<JournalEntry | null>(null);
  const [creating, setCreating] = useState(false);
  const [form, setForm] = useState({
    title: "",
    content: "",
    entry_type: "daily",
    tags: "",
  });

  const loadEntries = () => {
    if (!token) return;
    apiFetch<JournalEntry[]>("/api/journal?limit=100", {}, token)
      .then(setEntries)
      .catch((e) => toast.error(e.message));
  };

  useEffect(loadEntries, [token]);

  const handleCreate = async () => {
    if (!token || !form.content) return;
    setCreating(true);
    try {
      await apiFetch(
        "/api/journal",
        {
          method: "POST",
          body: JSON.stringify({
            ...form,
            tags: form.tags
              ? form.tags.split(",").map((t) => t.trim())
              : undefined,
          }),
        },
        token
      );
      setForm({ title: "", content: "", entry_type: "daily", tags: "" });
      toast.success("Entry created");
      loadEntries();
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setCreating(false);
    }
  };

  const handleDelete = async (path: string) => {
    if (!token || !confirm("Delete this entry?")) return;
    try {
      await apiFetch(`/api/journal/${encodeURIComponent(path)}`, { method: "DELETE" }, token);
      toast.success("Deleted");
      setSelected(null);
      loadEntries();
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  const viewEntry = async (path: string) => {
    if (!token) return;
    try {
      const entry = await apiFetch<JournalEntry>(
        `/api/journal/${encodeURIComponent(path)}`,
        {},
        token
      );
      setSelected(entry);
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Journal</h1>
        <Sheet>
          <SheetTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" /> New Entry
            </Button>
          </SheetTrigger>
          <SheetContent className="w-[500px] overflow-y-auto">
            <SheetHeader>
              <SheetTitle>New Journal Entry</SheetTitle>
            </SheetHeader>
            <div className="mt-6 space-y-4">
              <div className="space-y-1.5">
                <Label>Title</Label>
                <Input
                  value={form.title}
                  onChange={(e) =>
                    setForm({ ...form, title: e.target.value })
                  }
                  placeholder="Optional title"
                />
              </div>
              <div className="space-y-1.5">
                <Label>Type</Label>
                <Select
                  value={form.entry_type}
                  onValueChange={(v) => setForm({ ...form, entry_type: v })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="daily">Daily</SelectItem>
                    <SelectItem value="project">Project</SelectItem>
                    <SelectItem value="goal">Goal</SelectItem>
                    <SelectItem value="reflection">Reflection</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-1.5">
                <Label>Tags (comma-separated)</Label>
                <Input
                  value={form.tags}
                  onChange={(e) =>
                    setForm({ ...form, tags: e.target.value })
                  }
                  placeholder="e.g. work, ideas"
                />
              </div>
              <div className="space-y-1.5">
                <Label>Content</Label>
                <Textarea
                  rows={12}
                  value={form.content}
                  onChange={(e) =>
                    setForm({ ...form, content: e.target.value })
                  }
                  placeholder="Write your journal entry..."
                />
              </div>
              <Button onClick={handleCreate} disabled={creating || !form.content}>
                {creating ? "Creating..." : "Create Entry"}
              </Button>
            </div>
          </SheetContent>
        </Sheet>
      </div>

      {/* Entry list */}
      <div className="grid gap-4 md:grid-cols-2">
        {entries.map((e) => (
          <Card
            key={e.path}
            className="cursor-pointer transition-shadow hover:shadow-md"
            onClick={() => viewEntry(e.path)}
          >
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <CardTitle className="text-base">{e.title}</CardTitle>
                <Badge variant="outline">{e.type}</Badge>
              </div>
              {e.created && (
                <CardDescription>
                  {new Date(e.created).toLocaleDateString()}
                </CardDescription>
              )}
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground line-clamp-3">
                {e.preview}
              </p>
              {e.tags.length > 0 && (
                <div className="mt-2 flex gap-1">
                  {e.tags.map((t) => (
                    <Badge key={t} variant="secondary" className="text-xs">
                      {t}
                    </Badge>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Selected entry detail */}
      {selected && (
        <Sheet open={!!selected} onOpenChange={() => setSelected(null)}>
          <SheetContent className="w-[600px] overflow-y-auto">
            <SheetHeader>
              <SheetTitle>{selected.title}</SheetTitle>
            </SheetHeader>
            <div className="mt-4 space-y-4">
              <div className="flex gap-2">
                <Badge>{selected.type}</Badge>
                {selected.tags?.map((t) => (
                  <Badge key={t} variant="secondary">
                    {t}
                  </Badge>
                ))}
              </div>
              <pre className="whitespace-pre-wrap text-sm">
                {selected.content}
              </pre>
              <Button
                variant="destructive"
                size="sm"
                onClick={() => handleDelete(selected.path)}
              >
                Delete
              </Button>
            </div>
          </SheetContent>
        </Sheet>
      )}
    </div>
  );
}
