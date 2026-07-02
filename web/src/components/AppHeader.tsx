"use client";

import { Brain, Menu, Settings } from "lucide-react";
import { Button } from "@/components/ui/button";
import { NotificationBell } from "@/components/NotificationBell";

export function AppHeader({
  onOpenSettings,
  onToggleSidebar,
  onOpenGuide,
  token,
}: {
  onOpenSettings: () => void;
  onToggleSidebar: () => void;
  onOpenGuide?: () => void;
  token?: string;
}) {
  return (
    <header className="fixed inset-x-0 top-0 z-40 flex h-12 items-center justify-between border-b border-border/60 bg-background/80 px-4 backdrop-blur lg:left-60">
      <div className="flex items-center gap-1.5">
        <Button variant="ghost" size="icon" onClick={onToggleSidebar} className="-ml-2 lg:hidden">
          <Menu className="h-4 w-4" />
        </Button>
        <button
          onClick={onOpenGuide}
          className="flex items-center gap-2 transition-opacity hover:opacity-80 lg:hidden"
        >
          <div className="flex h-6 w-6 items-center justify-center rounded-lg bg-primary">
            <Brain className="h-3.5 w-3.5 text-primary-foreground" />
          </div>
          <span className="font-display text-sm font-semibold text-foreground">StewardMe</span>
        </button>
      </div>
      <div className="flex items-center gap-1">
        {token && <NotificationBell token={token} />}
        <Button variant="ghost" size="icon" onClick={onOpenSettings} title="Settings">
          <Settings className="h-4 w-4" />
        </Button>
      </div>
    </header>
  );
}
