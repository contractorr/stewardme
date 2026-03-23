"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { apiFetch } from "@/lib/api";

interface Notification {
  id: string;
  type: string;
  title: string;
  body: string;
  action_url: string;
  read: boolean;
}

export function useNotifications(token: string | undefined) {
  const [unreadCount, setUnreadCount] = useState(0);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(false);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const fetchCount = useCallback(async () => {
    if (!token) return;
    try {
      const data = await apiFetch<{ unread: number }>(
        "/api/v1/notifications/count",
        {},
        token
      );
      setUnreadCount(data.unread);
    } catch {
      // silent
    }
  }, [token]);

  const fetchAll = useCallback(async () => {
    if (!token) return;
    setLoading(true);
    try {
      const data = await apiFetch<Notification[]>(
        "/api/v1/notifications?limit=20",
        {},
        token
      );
      setNotifications(data);
      setUnreadCount(data.filter((n) => !n.read).length);
    } catch {
      // silent
    } finally {
      setLoading(false);
    }
  }, [token]);

  const markRead = useCallback(
    async (id: string) => {
      if (!token) return;
      try {
        await apiFetch(`/api/v1/notifications/${id}/read`, { method: "POST" }, token);
        setNotifications((prev) =>
          prev.map((n) => (n.id === id ? { ...n, read: true } : n))
        );
        setUnreadCount((prev) => Math.max(0, prev - 1));
      } catch {
        // silent
      }
    },
    [token]
  );

  const markAllRead = useCallback(async () => {
    if (!token) return;
    try {
      await apiFetch("/api/v1/notifications/read-all", { method: "POST" }, token);
      setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
      setUnreadCount(0);
    } catch {
      // silent
    }
  }, [token]);

  // Poll count every 60s
  useEffect(() => {
    fetchCount();
    intervalRef.current = setInterval(fetchCount, 60_000);
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [fetchCount]);

  return { unreadCount, notifications, loading, fetchAll, markRead, markAllRead };
}
