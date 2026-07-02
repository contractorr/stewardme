"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { toast } from "sonner";
import { ArrowRight, CheckCircle2 } from "lucide-react";

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
import { useToken } from "@/hooks/useToken";
import { apiFetch } from "@/lib/api";
import type { Flashcard, FlashcardRating } from "@/types/decks";

const SESSION_LIMIT = 20;

const ratingButtons: { rating: FlashcardRating; label: string; hint: string }[] = [
  { rating: "again", label: "Again", hint: "Didn’t recall" },
  { rating: "hard", label: "Hard", hint: "Barely recalled" },
  { rating: "good", label: "Good", hint: "Recalled with effort" },
  { rating: "easy", label: "Easy", hint: "Instant recall" },
];

export default function FlashcardReviewPage() {
  const token = useToken();
  const searchParams = useSearchParams();
  const deckId = searchParams.get("deck");

  const [queue, setQueue] = useState<Flashcard[]>([]);
  const [index, setIndex] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [reviewed, setReviewed] = useState(0);
  const [loading, setLoading] = useState(true);
  const [grading, setGrading] = useState(false);

  useEffect(() => {
    if (!token) return;
    const load = async () => {
      setLoading(true);
      try {
        const params = new URLSearchParams({ limit: String(SESSION_LIMIT) });
        if (deckId) params.set("deck_id", deckId);
        const cards = await apiFetch<Flashcard[]>(
          `/api/v1/curriculum/review/flashcards/due?${params.toString()}`,
          {},
          token,
        );
        setQueue(cards);
        setIndex(0);
        setRevealed(false);
        setReviewed(0);
      } catch (e) {
        toast.error((e as Error).message);
      } finally {
        setLoading(false);
      }
    };
    void load();
  }, [token, deckId]);

  const current = queue[index] ?? null;
  const done = !loading && (queue.length === 0 || index >= queue.length);

  const handleGrade = async (rating: FlashcardRating) => {
    if (!token || !current || grading) return;
    setGrading(true);
    try {
      await apiFetch(
        `/api/v1/curriculum/review/flashcards/${current.id}/grade`,
        { method: "POST", body: JSON.stringify({ rating }) },
        token,
      );
      setReviewed((count) => count + 1);
      setIndex((value) => value + 1);
      setRevealed(false);
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setGrading(false);
    }
  };

  return (
    <DashboardPageContainer className="space-y-6 py-4 md:py-6">
      <WorkspacePageHeader
        title="Flashcard review"
        description="Reveal the answer, then grade how well you recalled it. Grading schedules the next review."
        eyebrow="Learn"
        actions={
          <Button size="sm" variant="outline" asChild>
            <Link href="/learn/decks">Back to decks</Link>
          </Button>
        }
      />

      {loading ? (
        <Card className="animate-pulse">
          <CardContent className="p-6">
            <div className="h-4 w-1/2 rounded bg-muted" />
          </CardContent>
        </Card>
      ) : done ? (
        <Card>
          <CardHeader className="space-y-2">
            <div className="flex items-center gap-2 text-muted-foreground">
              <CheckCircle2 className="h-4 w-4" />
              <p className="text-[11px] font-semibold uppercase tracking-[0.18em]">
                Session complete
              </p>
            </div>
            <CardTitle>
              {reviewed > 0
                ? `Nice — ${reviewed} card${reviewed === 1 ? "" : "s"} reviewed`
                : "Nothing due right now"}
            </CardTitle>
            <CardDescription>
              {reviewed > 0
                ? "Cards you struggled with will come back sooner."
                : "Come back once cards fall due again, or add new cards to a deck."}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild>
              <Link href="/learn/decks">
                Back to decks
                <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
              </Link>
            </Button>
          </CardContent>
        </Card>
      ) : current ? (
        <Card>
          <CardHeader className="space-y-2">
            <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-muted-foreground">
              Card {index + 1} of {queue.length}
            </p>
            <CardTitle className="whitespace-pre-wrap text-xl leading-relaxed">
              {current.front}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {revealed ? (
              <>
                <div className="rounded-lg border bg-muted/40 p-4">
                  <p className="whitespace-pre-wrap text-sm leading-relaxed">
                    {current.back || "(no back side)"}
                  </p>
                </div>
                <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
                  {ratingButtons.map(({ rating, label, hint }) => (
                    <Button
                      key={rating}
                      variant={rating === "again" ? "outline" : "default"}
                      disabled={grading}
                      onClick={() => handleGrade(rating)}
                      className="flex h-auto flex-col gap-0.5 py-2"
                    >
                      <span>{label}</span>
                      <span className="text-[10px] font-normal opacity-70">{hint}</span>
                    </Button>
                  ))}
                </div>
              </>
            ) : (
              <Button onClick={() => setRevealed(true)}>Show answer</Button>
            )}
          </CardContent>
        </Card>
      ) : null}
    </DashboardPageContainer>
  );
}
