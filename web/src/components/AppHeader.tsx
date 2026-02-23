"use client";

import { Settings, LogOut, Info } from "lucide-react";
import { signOut } from "next-auth/react";
import { Button } from "@/components/ui/button";

export function AppHeader({ onOpenSettings }: { onOpenSettings: () => void }) {
  return (
    <header className="fixed inset-x-0 top-0 z-40 flex h-12 items-center justify-between border-b bg-background px-4">
      <div className="flex items-center gap-1.5">
        <span className="text-sm font-semibold">StewardMe</span>
        <span title="Your AI steward for navigating rapid change — intelligence, opportunities, and focus">
          <Info className="h-3.5 w-3.5 text-muted-foreground/60 cursor-help" />
        </span>
      </div>
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
