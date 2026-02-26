"use client";

import { useState } from "react";
import { useToken } from "@/hooks/useToken";
import { usePageView } from "@/hooks/usePageView";
import { AppHeader } from "@/components/AppHeader";
import { Sidebar } from "@/components/Sidebar";
import { SettingsSheet } from "@/components/SettingsSheet";

export function DashboardShell({ children }: { children: React.ReactNode }) {
  const token = useToken();
  usePageView();
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="h-screen">
      <AppHeader
        onOpenSettings={() => setSettingsOpen(true)}
        onToggleSidebar={() => setSidebarOpen((v) => !v)}
      />
      <Sidebar open={sidebarOpen} onOpenChange={setSidebarOpen} />
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
