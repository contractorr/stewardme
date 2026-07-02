"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { toast } from "sonner";
import {
  Download,
  Layers,
  Plus,
  Trash2,
  Upload,
} from "lucide-react";

import { DashboardPageContainer } from "@/components/DashboardPageContainer";
import { WorkspacePageHeader } from "@/components/WorkspacePageHeader";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { Textarea } from "@/components/ui/textarea";
import { useToken } from "@/hooks/useToken";
import { apiFetch, apiUrl } from "@/lib/api";
import type { Deck, DeckDetail, DeckImportResult } from "@/types/decks";

async function downloadFile(path: string, filename: string, token: string) {
  const res = await fetch(apiUrl(path), {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error(`Export failed (${res.status})`);
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
}

export default function DecksPage() {
  const token = useToken();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [decks, setDecks] = useState<Deck[]>([]);
  const [loading, setLoading] = useState(true);
  const [importing, setImporting] = useState(false);
  const [createOpen, setCreateOpen] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [openDeck, setOpenDeck] = useState<DeckDetail | null>(null);
  const [newFront, setNewFront] = useState("");
  const [newBack, setNewBack] = useState("");

  const loadDecks = async () => {
    if (!token) return;
    setLoading(true);
    try {
      setDecks(await apiFetch<Deck[]>("/api/v1/curriculum/decks", {}, token));
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadDecks();
  }, [token]); // eslint-disable-line react-hooks/exhaustive-deps

  const totalDue = decks.reduce((sum, deck) => sum + deck.due_count, 0);

  const handleImport = async (file: File) => {
    if (!token) return;
    setImporting(true);
    try {
      const form = new FormData();
      form.append("file", file);
      const result = await apiFetch<DeckImportResult>(
        "/api/v1/curriculum/decks/import",
        { method: "POST", body: form },
        token,
      );
      const skipped =
        result.skipped_media > 0
          ? ` (${result.skipped_media} media reference${result.skipped_media === 1 ? "" : "s"} skipped)`
          : "";
      toast.success(`Imported ${result.card_count} cards into “${result.title}”${skipped}`);
      await loadDecks();
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setImporting(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  const handleCreate = async () => {
    if (!token || !newTitle.trim()) return;
    try {
      await apiFetch<Deck>(
        "/api/v1/curriculum/decks",
        { method: "POST", body: JSON.stringify({ title: newTitle.trim() }) },
        token,
      );
      setNewTitle("");
      setCreateOpen(false);
      await loadDecks();
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  const handleDelete = async (deck: Deck) => {
    if (!token) return;
    if (!window.confirm(`Delete “${deck.title}” and its ${deck.card_count} cards?`)) return;
    try {
      await apiFetch(`/api/v1/curriculum/decks/${deck.id}`, { method: "DELETE" }, token);
      toast.success("Deck deleted");
      await loadDecks();
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  const handleExport = async (deck: Deck) => {
    if (!token) return;
    try {
      await downloadFile(
        `/api/v1/curriculum/decks/${deck.id}/export`,
        `${deck.title.toLowerCase().replace(/[^a-z0-9]+/g, "-")}.apkg`,
        token,
      );
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  const openDeckDetail = async (deck: Deck) => {
    if (!token) return;
    try {
      setOpenDeck(
        await apiFetch<DeckDetail>(`/api/v1/curriculum/decks/${deck.id}`, {}, token),
      );
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  const handleAddCard = async () => {
    if (!token || !openDeck || !newFront.trim()) return;
    try {
      await apiFetch(
        `/api/v1/curriculum/decks/${openDeck.id}/cards`,
        {
          method: "POST",
          body: JSON.stringify({ front: newFront.trim(), back: newBack.trim() }),
        },
        token,
      );
      setNewFront("");
      setNewBack("");
      await openDeckDetail(openDeck);
      await loadDecks();
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  const handleDeleteCard = async (cardId: string) => {
    if (!token || !openDeck) return;
    try {
      await apiFetch(
        `/api/v1/curriculum/decks/${openDeck.id}/cards/${cardId}`,
        { method: "DELETE" },
        token,
      );
      await openDeckDetail(openDeck);
      await loadDecks();
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  return (
    <DashboardPageContainer className="space-y-6 py-4 md:py-6">
      <WorkspacePageHeader
        title="Flashcard decks"
        description="Import Anki decks, review cards on a spaced-repetition schedule, and export decks back to Anki."
        eyebrow="Learn"
        actions={
          <div className="flex flex-wrap gap-2">
            <input
              ref={fileInputRef}
              type="file"
              accept=".apkg"
              className="hidden"
              onChange={(event) => {
                const file = event.target.files?.[0];
                if (file) void handleImport(file);
              }}
            />
            <Button
              size="sm"
              variant="outline"
              disabled={importing}
              onClick={() => fileInputRef.current?.click()}
            >
              <Upload className="mr-1.5 h-3.5 w-3.5" />
              {importing ? "Importing…" : "Import .apkg"}
            </Button>
            <Button size="sm" variant="outline" onClick={() => setCreateOpen(true)}>
              <Plus className="mr-1.5 h-3.5 w-3.5" />
              New deck
            </Button>
          </div>
        }
      />

      <Card>
        <CardHeader className="space-y-1">
          <CardTitle>
            {totalDue > 0
              ? `${totalDue} card${totalDue === 1 ? "" : "s"} due for review`
              : "No cards due right now"}
          </CardTitle>
          <CardDescription>
            {totalDue > 0
              ? "One short session keeps your decks fresh."
              : "Cards become due again as their review intervals lapse."}
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-2">
          {totalDue > 0 ? (
            <Button asChild>
              <Link href="/learn/decks/review">Start flashcard review</Link>
            </Button>
          ) : null}
          <Button variant="outline" asChild>
            <Link href="/learn">Back to Learn</Link>
          </Button>
        </CardContent>
      </Card>

      {loading ? (
        <Card className="animate-pulse">
          <CardContent className="p-6">
            <div className="h-4 w-1/3 rounded bg-muted" />
          </CardContent>
        </Card>
      ) : decks.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-start gap-3 p-6">
            <div className="flex items-center gap-2 text-muted-foreground">
              <Layers className="h-4 w-4" />
              <p className="text-sm">No decks yet.</p>
            </div>
            <p className="text-sm text-muted-foreground">
              Import an Anki .apkg file or create an empty deck to start collecting
              flashcards.
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {decks.map((deck) => (
            <Card key={deck.id}>
              <CardHeader className="pb-2">
                <CardTitle className="text-base">{deck.title}</CardTitle>
                <CardDescription>
                  {deck.card_count} card{deck.card_count === 1 ? "" : "s"}
                  {deck.due_count > 0 ? ` · ${deck.due_count} due` : ""}
                  {deck.source === "imported" ? " · imported" : ""}
                </CardDescription>
              </CardHeader>
              <CardContent className="flex flex-wrap gap-2">
                <Button size="sm" variant="outline" onClick={() => openDeckDetail(deck)}>
                  Manage cards
                </Button>
                {deck.due_count > 0 ? (
                  <Button size="sm" asChild>
                    <Link href={`/learn/decks/review?deck=${deck.id}`}>Review</Link>
                  </Button>
                ) : null}
                <Button size="sm" variant="ghost" onClick={() => handleExport(deck)}>
                  <Download className="h-3.5 w-3.5" />
                </Button>
                <Button size="sm" variant="ghost" onClick={() => handleDelete(deck)}>
                  <Trash2 className="h-3.5 w-3.5" />
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <Dialog open={createOpen} onOpenChange={setCreateOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>New deck</DialogTitle>
            <DialogDescription>
              Create an empty deck and add front/back cards to it.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-3">
            <div className="space-y-1.5">
              <Label htmlFor="deck-title">Title</Label>
              <Input
                id="deck-title"
                value={newTitle}
                onChange={(event) => setNewTitle(event.target.value)}
                placeholder="e.g. Spanish vocabulary"
              />
            </div>
            <Button onClick={handleCreate} disabled={!newTitle.trim()}>
              Create deck
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      <Sheet open={openDeck !== null} onOpenChange={(open) => !open && setOpenDeck(null)}>
        <SheetContent className="w-full overflow-y-auto sm:max-w-lg">
          <SheetHeader>
            <SheetTitle>{openDeck?.title}</SheetTitle>
            <SheetDescription>
              {openDeck?.card_count} card{openDeck?.card_count === 1 ? "" : "s"} in this
              deck.
            </SheetDescription>
          </SheetHeader>
          {openDeck ? (
            <div className="space-y-4 px-4 pb-6">
              <div className="space-y-2 rounded-lg border p-3">
                <Label htmlFor="card-front">New card</Label>
                <Textarea
                  id="card-front"
                  value={newFront}
                  onChange={(event) => setNewFront(event.target.value)}
                  placeholder="Front"
                  rows={2}
                />
                <Textarea
                  value={newBack}
                  onChange={(event) => setNewBack(event.target.value)}
                  placeholder="Back"
                  rows={2}
                />
                <Button size="sm" onClick={handleAddCard} disabled={!newFront.trim()}>
                  Add card
                </Button>
              </div>
              <div className="space-y-2">
                {openDeck.cards.map((card) => (
                  <div
                    key={card.id}
                    className="flex items-start justify-between gap-2 rounded-lg border p-3"
                  >
                    <div className="min-w-0 space-y-1">
                      <p className="whitespace-pre-wrap text-sm font-medium">{card.front}</p>
                      {card.back ? (
                        <p className="whitespace-pre-wrap text-sm text-muted-foreground">
                          {card.back}
                        </p>
                      ) : null}
                    </div>
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => handleDeleteCard(card.id)}
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                ))}
                {openDeck.cards.length === 0 ? (
                  <p className="text-sm text-muted-foreground">No cards yet.</p>
                ) : null}
              </div>
            </div>
          ) : null}
        </SheetContent>
      </Sheet>
    </DashboardPageContainer>
  );
}
