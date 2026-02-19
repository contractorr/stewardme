"use client";

import { useSession } from "next-auth/react";

export function useToken(): string | undefined {
  const { data: session } = useSession();
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  return (session as any)?.accessToken as string | undefined;
}
