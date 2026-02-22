"use client";

import { useSession } from "next-auth/react";

export function useToken(): string | undefined {
  const { data: session } = useSession();
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const token = (session as any)?.accessToken as string | undefined;
  if (session && !token) {
    console.warn("[useToken] session exists but accessToken missing — token may not have been minted");
  }
  return token;
}
