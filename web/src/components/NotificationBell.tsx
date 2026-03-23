"use client";

import { Bell } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Popover,
  PopoverTrigger,
} from "@/components/ui/popover";
import { NotificationPanel } from "@/components/NotificationPanel";
import { useNotifications } from "@/hooks/useNotifications";

export function NotificationBell({ token }: { token: string }) {
  const { unreadCount, notifications, loading, fetchAll, markRead, markAllRead } =
    useNotifications(token);

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="ghost" size="icon" onClick={fetchAll} title="Notifications" className="relative">
          <Bell className="h-4 w-4" />
          {unreadCount > 0 && (
            <span className="absolute -right-0.5 -top-0.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-red-500 px-1 text-[10px] font-bold text-white">
              {unreadCount > 99 ? "99+" : unreadCount}
            </span>
          )}
        </Button>
      </PopoverTrigger>
      <NotificationPanel
        notifications={notifications}
        loading={loading}
        onOpen={fetchAll}
        onMarkRead={markRead}
        onMarkAllRead={markAllRead}
      />
    </Popover>
  );
}
