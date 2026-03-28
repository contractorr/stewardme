"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import { useToken } from "@/hooks/useToken";
import type { LearningStats, LearningToday } from "@/types/curriculum";

interface JournalEntryStub {
  path: string;
  created: string | null;
}

interface GoalStub {
  path: string;
  status: string;
}

export interface HomeStats {
  journalEntries: JournalEntryStub[];
  activeGoals: number;
  learningStats: LearningStats | null;
  learningToday: LearningToday | null;
  loading: boolean;
}

export function useHomeStats(): HomeStats {
  const token = useToken();
  const [journalEntries, setJournalEntries] = useState<JournalEntryStub[]>([]);
  const [activeGoals, setActiveGoals] = useState(0);
  const [learningStats, setLearningStats] = useState<LearningStats | null>(null);
  const [learningToday, setLearningToday] = useState<LearningToday | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) return;
    let cancelled = false;

    const fetchAll = async () => {
      try {
        const [entries, goals, curriculumStats, curriculumToday] = await Promise.all([
          apiFetch<JournalEntryStub[]>("/api/v1/journal?limit=200", {}, token).catch(() => []),
          apiFetch<GoalStub[]>("/api/v1/goals", {}, token).catch(() => []),
          apiFetch<LearningStats>("/api/v1/curriculum/stats", {}, token).catch(() => null),
          apiFetch<LearningToday>("/api/v1/curriculum/today", {}, token).catch(() => null),
        ]);
        if (cancelled) return;
        setJournalEntries(entries);
        setActiveGoals(goals.filter((g) => g.status === "active").length);
        setLearningStats(curriculumStats);
        setLearningToday(curriculumToday);
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    void fetchAll();
    return () => { cancelled = true; };
  }, [token]);

  return { journalEntries, activeGoals, learningStats, learningToday, loading };
}
