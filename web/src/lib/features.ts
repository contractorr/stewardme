import { Database, Search, Target, Wrench } from "lucide-react";
import type { LucideIcon } from "lucide-react";

export interface Feature {
  icon: LucideIcon;
  title: string;
  description: string;
}

export const FEATURES: Feature[] = [
  {
    icon: Target,
    title: "Goal tracking",
    description:
      "Set objectives with milestones. Get nudged when priorities should shift.",
  },
  {
    icon: Search,
    title: "Deep research",
    description:
      "Multi-source research reports synthesised and cited by AI on any topic.",
  },
  {
    icon: Database,
    title: "Memory",
    description:
      "Remembers your context across conversations — advice gets sharper over time.",
  },
  {
    icon: Wrench,
    title: "MCP server",
    description:
      "52 tools for Claude Code and other AI agents. Your data, programmable.",
  },
];
