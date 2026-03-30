import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

interface DashboardPageContainerProps {
  children: ReactNode;
  className?: string;
}

export function DashboardPageContainer({
  children,
  className,
}: DashboardPageContainerProps) {
  return (
    <div className={cn("mx-auto w-full max-w-7xl px-4 md:px-6", className)}>
      {children}
    </div>
  );
}
