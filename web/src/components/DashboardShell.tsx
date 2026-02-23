"use client";

import { useState } from "react";
import { useToken } from "@/hooks/useToken";
import { AppHeader } from "@/components/AppHeader";
import { SettingsSheet } from "@/components/SettingsSheet";

export function DashboardShell({ children }: { children: React.ReactNode }) {
  const token = useToken();
  const [settingsOpen, setSettingsOpen] = useState(false);

  return (
    <div className="h-screen">
      <AppHeader onOpenSettings={() => setSettingsOpen(true)} />
      {token && (
        <SettingsSheet
          open={settingsOpen}
          onOpenChange={setSettingsOpen}
          token={token}
        />
      )}
      <main className="h-full overflow-y-auto pt-12">{children}</main>
    </div>
  );
}
