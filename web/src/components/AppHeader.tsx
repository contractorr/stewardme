"use client";

import { Settings, LogOut } from "lucide-react";
import { signOut } from "next-auth/react";
import { Button } from "@/components/ui/button";

export function AppHeader({ onOpenSettings }: { onOpenSettings: () => void }) {
  return (
    <header className="fixed inset-x-0 top-0 z-40 flex h-12 items-center justify-between border-b bg-background px-4">
      <span className="text-sm font-semibold">Journal Assistant</span>
      <div className="flex items-center gap-1">
        <Button variant="ghost" size="icon" onClick={onOpenSettings} title="Settings">
          <Settings className="h-4 w-4" />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          onClick={() => signOut({ callbackUrl: "/login" })}
          title="Sign out"
        >
          <LogOut className="h-4 w-4" />
        </Button>
      </div>
    </header>
  );
}
