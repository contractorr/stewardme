"use client";

import Link from "next/link";
import { Check, CheckCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PopoverContent } from "@/components/ui/popover";

interface Notification {
  id: string;
  type: string;
  title: string;
  body: string;
  action_url: string;
  read: boolean;
}

export function NotificationPanel({
  notifications,
  loading,
  onMarkRead,
  onMarkAllRead,
}: {
  notifications: Notification[];
  loading: boolean;
  onMarkRead: (id: string) => void;
  onMarkAllRead: () => void;
}) {
  return (
    <PopoverContent align="end" className="w-80 p-0">
      <div className="flex items-center justify-between border-b px-3 py-2">
        <span className="text-sm font-medium">Notifications</span>
        {notifications.some((n) => !n.read) && (
          <Button
            variant="ghost"
            size="sm"
            onClick={onMarkAllRead}
            className="h-7 text-xs"
          >
            <CheckCheck className="mr-1 h-3 w-3" />
            Mark all read
          </Button>
        )}
      </div>
      <div className="max-h-72 overflow-y-auto">
        {loading && (
          <div className="px-3 py-4 text-center text-xs text-muted-foreground">
            Loading...
          </div>
        )}
        {!loading && notifications.length === 0 && (
          <div className="px-3 py-4 text-center text-xs text-muted-foreground">
            No notifications
          </div>
        )}
        {notifications.map((n) => (
          <div
            key={n.id}
            className={`flex items-start gap-2 border-b px-3 py-2 last:border-0 ${
              n.read ? "opacity-60" : ""
            }`}
          >
            <div className="flex-1 min-w-0">
              <Link
                href={n.action_url}
                className="text-sm font-medium hover:underline"
                onClick={() => !n.read && onMarkRead(n.id)}
              >
                {n.title}
              </Link>
              <p className="text-xs text-muted-foreground truncate">{n.body}</p>
            </div>
            {!n.read && (
              <Button
                variant="ghost"
                size="icon"
                className="h-6 w-6 shrink-0"
                onClick={() => onMarkRead(n.id)}
              >
                <Check className="h-3 w-3" />
              </Button>
            )}
          </div>
        ))}
      </div>
    </PopoverContent>
  );
}
