"use client";

import { AlertTriangle } from "lucide-react";

interface Degradation {
  component: string;
  message: string;
}

export function DegradationBanner({
  degradations,
}: {
  degradations?: Degradation[];
}) {
  if (!degradations || degradations.length === 0) return null;

  const messages = [...new Set(degradations.map((d) => d.message))];

  return (
    <div className="flex items-center gap-2 rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-xs text-amber-800 dark:border-amber-800 dark:bg-amber-950/30 dark:text-amber-300">
      <AlertTriangle className="h-3.5 w-3.5 shrink-0" />
      <span>Partial data — {messages.join("; ")}</span>
    </div>
  );
}
