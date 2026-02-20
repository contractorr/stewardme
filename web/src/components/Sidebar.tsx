"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BookOpen,
  Brain,
  Home,
  Menu,
  Newspaper,
  Settings,
  Target,
  X,
  LogOut,
} from "lucide-react";
import { signOut } from "next-auth/react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

const navItems = [
  { href: "/", label: "Dashboard", icon: Home },
  { href: "/journal", label: "Journal", icon: BookOpen },
  { href: "/advisor", label: "Advisor", icon: Brain },
  { href: "/goals", label: "Goals", icon: Target },
  { href: "/intel", label: "Intel", icon: Newspaper },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  const navContent = (
    <>
      <div className="mb-6 flex items-center justify-between px-2">
        <h1 className="text-lg font-semibold">AI Coach</h1>
        <Button
          variant="ghost"
          size="icon"
          className="md:hidden"
          onClick={() => setOpen(false)}
        >
          <X className="h-4 w-4" />
        </Button>
      </div>
      <nav className="flex flex-1 flex-col gap-1">
        {navItems.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            onClick={() => setOpen(false)}
            className={cn(
              "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-accent",
              pathname === href
                ? "bg-accent text-accent-foreground"
                : "text-muted-foreground"
            )}
          >
            <Icon className="h-4 w-4" />
            {label}
          </Link>
        ))}
      </nav>
      <div className="border-t pt-3">
        <button
          onClick={() => signOut({ callbackUrl: "/login" })}
          className="flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-accent"
        >
          <LogOut className="h-4 w-4" />
          Sign Out
        </button>
      </div>
    </>
  );

  return (
    <>
      {/* Mobile hamburger */}
      <div className="fixed left-4 top-4 z-50 md:hidden">
        {!open && (
          <Button variant="outline" size="icon" onClick={() => setOpen(true)}>
            <Menu className="h-4 w-4" />
          </Button>
        )}
      </div>

      {/* Mobile overlay */}
      {open && (
        <div
          className="fixed inset-0 z-40 bg-black/50 md:hidden"
          onClick={() => setOpen(false)}
        />
      )}

      {/* Mobile sidebar */}
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-50 flex w-56 flex-col border-r bg-background px-3 py-4 transition-transform md:hidden",
          open ? "translate-x-0" : "-translate-x-full"
        )}
      >
        {navContent}
      </aside>

      {/* Desktop sidebar */}
      <aside className="hidden h-screen w-56 flex-col border-r bg-muted/40 px-3 py-4 md:flex">
        {navContent}
      </aside>
    </>
  );
}
