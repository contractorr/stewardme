"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import type { ReviewItem } from "@/types/curriculum";

const gradeLabels = [
  "Blackout",
  "Incorrect",
  "Hard",
  "Okay",
  "Good",
  "Perfect",
];

const gradeColors = [
  "bg-red-500",
  "bg-red-400",
  "bg-orange-400",
  "bg-yellow-400",
  "bg-green-400",
  "bg-green-500",
];

interface ReviewCardProps {
  item: ReviewItem;
  onGrade: (reviewId: string, answer: string, selfGrade?: number) => Promise<void>;
  showAnswer?: boolean;
}

export function ReviewCard({ item, onGrade, showAnswer = false }: ReviewCardProps) {
  const [answer, setAnswer] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [grading, setGrading] = useState(false);
  const [showSelfGrade, setShowSelfGrade] = useState(false);

  const handleSubmit = async () => {
    setGrading(true);
    try {
      await onGrade(item.id, answer);
      setSubmitted(true);
    } finally {
      setGrading(false);
    }
  };

  const handleSelfGrade = async (grade: number) => {
    setGrading(true);
    try {
      await onGrade(item.id, answer, grade);
      setSubmitted(true);
    } finally {
      setGrading(false);
    }
  };

  return (
    <div className="space-y-4 rounded-lg border bg-card p-4">
      <div className="flex items-start justify-between gap-2">
        <p className="text-sm font-medium leading-relaxed">{item.question}</p>
        <Badge variant="outline" className="shrink-0 text-[10px] capitalize">
          {item.bloom_level}
        </Badge>
      </div>

      {!submitted ? (
        <div className="space-y-3">
          <Textarea
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="Type your answer..."
            rows={3}
            className="text-sm"
          />
          <div className="flex items-center gap-2">
            <Button size="sm" onClick={handleSubmit} disabled={!answer.trim() || grading}>
              {grading ? "Grading..." : "Submit"}
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => setShowSelfGrade(!showSelfGrade)}
            >
              Self-grade
            </Button>
          </div>
          {showSelfGrade && (
            <div className="flex flex-wrap gap-1.5">
              {gradeLabels.map((label, i) => (
                <Button
                  key={i}
                  size="sm"
                  variant="outline"
                  className="text-xs"
                  onClick={() => handleSelfGrade(i)}
                  disabled={grading}
                >
                  <span className={`mr-1.5 h-2 w-2 rounded-full ${gradeColors[i]}`} />
                  {i} — {label}
                </Button>
              ))}
            </div>
          )}
        </div>
      ) : (
        <div className="rounded-md bg-muted/50 p-3">
          <p className="text-xs text-muted-foreground">Answer submitted — moving to next question.</p>
        </div>
      )}

      {showAnswer && submitted && (
        <div className="rounded-md border-l-2 border-primary/40 bg-primary/5 p-3">
          <p className="text-xs font-medium text-muted-foreground mb-1">Expected answer:</p>
          <p className="text-sm">{item.expected_answer}</p>
        </div>
      )}
    </div>
  );
}
