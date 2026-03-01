"use client";

import { useEffect, useState } from "react";
import { useToken } from "./useToken";
import { apiFetch } from "@/lib/api";

/** Returns true if user is on shared key (lite mode). Cached per mount. */
export function useLiteMode(): boolean | null {
  const token = useToken();
  const [lite, setLite] = useState<boolean | null>(null);

  useEffect(() => {
    if (!token) return;
    apiFetch<{ using_shared_key: boolean }>("/api/settings", {}, token)
      .then((s) => setLite(s.using_shared_key))
      .catch(() => setLite(false));
  }, [token]);

  return lite;
}
