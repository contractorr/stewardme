"use client";

import { useEffect, useMemo, useState } from "react";
import { toast } from "sonner";
import { Check, FileText, Sparkles, Trash2, X } from "lucide-react";

import { DashboardPageContainer } from "@/components/DashboardPageContainer";
import { WorkspacePageHeader } from "@/components/WorkspacePageHeader";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { useToken } from "@/hooks/useToken";
import { apiFetch } from "@/lib/api";
import type { CorrectionType, Note, NoteSummary } from "@/types/notes";

const correctionLabels: Record<CorrectionType, string> = {
  spelling: "Spelling",
  grammar: "Grammar",
  factual: "Factual",
  rewording: "Rewording",
  removal: "Removed",
};

const correctionOrder: CorrectionType[] = [
  "factual",
  "spelling",
  "grammar",
  "rewording",
  "removal",
];

function DiffView({ diff }: { diff: string }) {
  const lines = diff.split("\n");
  return (
    <pre className="max-h-96 overflow-auto rounded-lg border bg-muted/30 p-3 text-xs leading-relaxed">
      {lines.map((line, index) => {
        let className = "text-muted-foreground";
        if (line.startsWith("+") && !line.startsWith("+++")) {
          className = "bg-emerald-500/10 text-emerald-700 dark:text-emerald-400";
        } else if (line.startsWith("-") && !line.startsWith("---")) {
          className = "bg-red-500/10 text-red-700 dark:text-red-400";
        } else if (line.startsWith("@@")) {
          className = "text-blue-600 dark:text-blue-400";
        }
        return (
          <div key={index} className={`whitespace-pre-wrap px-1 ${className}`}>
            {line || " "}
          </div>
        );
      })}
    </pre>
  );
}

export default function NotesPage() {
  const token = useToken();
  const [notes, setNotes] = useState<NoteSummary[]>([]);
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const [polishing, setPolishing] = useState(false);
  const [reviewNote, setReviewNote] = useState<Note | null>(null);
  const [viewNote, setViewNote] = useState<Note | null>(null);
  const [deciding, setDeciding] = useState(false);

  const loadNotes = async () => {
    if (!token) return;
    try {
      setNotes(await apiFetch<NoteSummary[]>("/api/v1/notes", {}, token));
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  useEffect(() => {
    void loadNotes();
  }, [token]); // eslint-disable-line react-hooks/exhaustive-deps

  const groupedCorrections = useMemo(() => {
    if (!reviewNote) return [];
    return correctionOrder
      .map((type) => ({
        type,
        items: reviewNote.corrections.filter((c) => c.type === type),
      }))
      .filter((group) => group.items.length > 0);
  }, [reviewNote]);

  const handlePolish = async () => {
    if (!token || !text.trim()) return;
    setPolishing(true);
    try {
      const note = await apiFetch<Note>(
        "/api/v1/notes/polish",
        {
          method: "POST",
          body: JSON.stringify({ text: text.trim(), title: title.trim() }),
        },
        token,
      );
      setReviewNote(note);
      setViewNote(null);
      await loadNotes();
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setPolishing(false);
    }
  };

  const handleAccept = async () => {
    if (!token || !reviewNote) return;
    setDeciding(true);
    try {
      const accepted = await apiFetch<Note>(
        `/api/v1/notes/${reviewNote.id}/accept`,
        { method: "POST" },
        token,
      );
      toast.success("Polished note saved. The original text has been discarded.");
      setReviewNote(null);
      setViewNote(accepted);
      setTitle("");
      setText("");
      await loadNotes();
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setDeciding(false);
    }
  };

  const handleDiscard = async (noteId: string, isReview: boolean) => {
    if (!token) return;
    setDeciding(true);
    try {
      await apiFetch(`/api/v1/notes/${noteId}/discard`, { method: "POST" }, token);
      if (isReview) {
        setReviewNote(null);
        toast.success("Polish discarded — nothing was stored.");
      } else {
        setViewNote(null);
        toast.success("Note deleted.");
      }
      await loadNotes();
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setDeciding(false);
    }
  };

  const openNote = async (summary: NoteSummary) => {
    if (!token) return;
    try {
      const note = await apiFetch<Note>(`/api/v1/notes/${summary.id}`, {}, token);
      if (note.status === "pending") {
        setReviewNote(note);
        setViewNote(null);
      } else {
        setViewNote(note);
        setReviewNote(null);
      }
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  return (
    <DashboardPageContainer className="space-y-6 py-4 md:py-6">
      <WorkspacePageHeader
        title="Notes"
        description="Paste a messy note and get a polished version back. Review every correction, then accept to keep the clean copy."
        eyebrow="Notes"
      />

      {reviewNote ? (
        <Card>
          <CardHeader className="space-y-2">
            <div className="flex items-center justify-between gap-2">
              <div className="space-y-1">
                <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-muted-foreground">
                  Review the polish
                </p>
                <CardTitle>{reviewNote.title || "Untitled note"}</CardTitle>
                <CardDescription>
                  Accept to store the polished note and permanently discard the original
                  text, or discard to keep nothing.
                </CardDescription>
              </div>
              <div className="flex shrink-0 gap-2">
                <Button onClick={handleAccept} disabled={deciding}>
                  <Check className="mr-1.5 h-3.5 w-3.5" />
                  Accept
                </Button>
                <Button
                  variant="outline"
                  disabled={deciding}
                  onClick={() => handleDiscard(reviewNote.id, true)}
                >
                  <X className="mr-1.5 h-3.5 w-3.5" />
                  Discard
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-5">
            {groupedCorrections.length > 0 ? (
              <div className="space-y-3">
                <h3 className="text-sm font-semibold">
                  {reviewNote.corrections.length} correction
                  {reviewNote.corrections.length === 1 ? "" : "s"}
                </h3>
                {groupedCorrections.map((group) => (
                  <div key={group.type} className="space-y-2">
                    <Badge variant="secondary">{correctionLabels[group.type]}</Badge>
                    <div className="space-y-1.5">
                      {group.items.map((item, index) => (
                        <div
                          key={index}
                          className="rounded-lg border p-2.5 text-sm"
                        >
                          <p>
                            <span className="text-red-700 line-through dark:text-red-400">
                              {item.original}
                            </span>
                            {item.corrected ? (
                              <>
                                {" "}
                                <span className="text-emerald-700 dark:text-emerald-400">
                                  {item.corrected}
                                </span>
                              </>
                            ) : null}
                          </p>
                          {item.reason ? (
                            <p className="mt-1 text-xs text-muted-foreground">
                              {item.reason}
                            </p>
                          ) : null}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">
                No itemized corrections were reported — check the full diff below.
              </p>
            )}

            <div className="space-y-2">
              <h3 className="text-sm font-semibold">Full diff</h3>
              {reviewNote.diff ? (
                <DiffView diff={reviewNote.diff} />
              ) : (
                <p className="text-sm text-muted-foreground">
                  The polished note is identical to the original.
                </p>
              )}
            </div>

            <div className="space-y-2">
              <h3 className="text-sm font-semibold">Preview</h3>
              <div
                className="note-html max-w-none rounded-lg border p-4"
                dangerouslySetInnerHTML={{ __html: reviewNote.polished_html }}
              />
            </div>
          </CardContent>
        </Card>
      ) : viewNote ? (
        <Card>
          <CardHeader className="space-y-2">
            <div className="flex items-center justify-between gap-2">
              <div className="space-y-1">
                <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-muted-foreground">
                  Polished note
                </p>
                <CardTitle>{viewNote.title || "Untitled note"}</CardTitle>
              </div>
              <div className="flex shrink-0 gap-2">
                <Button variant="outline" onClick={() => setViewNote(null)}>
                  Close
                </Button>
                <Button
                  variant="ghost"
                  disabled={deciding}
                  onClick={() => handleDiscard(viewNote.id, false)}
                >
                  <Trash2 className="h-3.5 w-3.5" />
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div
              className="note-html max-w-none"
              dangerouslySetInnerHTML={{ __html: viewNote.polished_html }}
            />
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardHeader className="space-y-1">
            <CardTitle>Polish a note</CardTitle>
            <CardDescription>
              Spelling, grammar, and clear factual errors are fixed; awkward sections are
              reworded and duplicate content is removed. Nothing is stored until you accept.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <Input
              placeholder="Title (optional)"
              value={title}
              onChange={(event) => setTitle(event.target.value)}
            />
            <Textarea
              placeholder="Paste messy markdown or plain text…"
              value={text}
              onChange={(event) => setText(event.target.value)}
              rows={10}
            />
            <Button onClick={handlePolish} disabled={polishing || !text.trim()}>
              <Sparkles className="mr-1.5 h-3.5 w-3.5" />
              {polishing ? "Polishing…" : "Polish note"}
            </Button>
          </CardContent>
        </Card>
      )}

      <section className="space-y-3">
        <h2 className="text-lg font-semibold">My notes</h2>
        {notes.length === 0 ? (
          <Card>
            <CardContent className="flex items-center gap-2 p-6 text-sm text-muted-foreground">
              <FileText className="h-4 w-4" />
              Polished notes will appear here after you accept them.
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {notes.map((note) => (
              <button
                key={note.id}
                onClick={() => openNote(note)}
                className="rounded-xl border bg-card p-4 text-left transition-colors hover:bg-accent/50"
              >
                <div className="flex items-center justify-between gap-2">
                  <p className="truncate text-sm font-medium">
                    {note.title || "Untitled note"}
                  </p>
                  {note.status === "pending" ? (
                    <Badge variant="outline">Needs review</Badge>
                  ) : null}
                </div>
                <p className="mt-1 text-xs text-muted-foreground">
                  {note.created_at
                    ? new Date(note.created_at).toLocaleDateString()
                    : ""}
                </p>
              </button>
            ))}
          </div>
        )}
      </section>
    </DashboardPageContainer>
  );
}
