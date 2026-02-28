"use client";

import { useMemo, type ReactNode } from "react";
import ReactMarkdown, { type Components } from "react-markdown";
import remarkGfm from "remark-gfm";
import { ArrowRight, X } from "lucide-react";
import { Button } from "@/components/ui/button";

// --- Utilities ---

/** Walk React children tree to extract plain text */
function extractTextFromChildren(children: ReactNode): string {
  if (typeof children === "string") return children;
  if (typeof children === "number") return String(children);
  if (!children) return "";
  if (Array.isArray(children)) return children.map(extractTextFromChildren).join("");
  if (typeof children === "object" && "props" in children) {
    return extractTextFromChildren((children as { props: { children?: ReactNode } }).props.children);
  }
  return "";
}

/** CTA patterns — questions offering to do something */
const CTA_RE = /(?:^|\. )((?:Want me to|Would you like me to|Shall I|Should I|I can also|I could)\s[^.?!]*\??)/gi;

/** Extract CTA sentences from paragraph text */
function extractCTAs(text: string): { remainder: string; ctas: string[] } {
  const ctas: string[] = [];
  const remainder = text.replace(CTA_RE, (match, cta: string) => {
    ctas.push(cta.trim().replace(/^\.\s*/, ""));
    return "";
  }).replace(/\s{2,}/g, " ").trim();
  return { remainder, ctas };
}

/** Regex for signal-style list items: **Bold Title** — description */
const SIGNAL_ITEM_RE = /^\*\*(.+?)\*\*\s*[—–-]\s*(.+)$/;

/** Headings that indicate action items follow */
const ACTION_HEADING_RE = /^(next steps|actions|action items|suggestions|recommendations|to.?do|try this|things to try)/i;

/** Pre-scan markdown to collect action items under action-oriented headings */
function collectActionItems(content: string): Set<string> {
  const items = new Set<string>();
  const lines = content.split("\n");
  let inActionSection = false;

  for (const line of lines) {
    const headingMatch = line.match(/^#{1,3}\s+(.+)/);
    if (headingMatch) {
      inActionSection = ACTION_HEADING_RE.test(headingMatch[1]);
      continue;
    }
    if (inActionSection) {
      const listMatch = line.match(/^[-*]\s+(.+)/);
      if (listMatch) {
        items.add(listMatch[1].replace(/\*\*/g, "").trim());
      }
      // Blank line ends section
      if (line.trim() === "") inActionSection = false;
    }
  }
  return items;
}

// --- Component ---

interface MessageRendererProps {
  content: string;
  onAction: (text: string) => void;
  compact?: boolean;
}

export function MessageRenderer({ content, onAction, compact }: MessageRendererProps) {
  const actionItems = useMemo(() => collectActionItems(content), [content]);

  const components: Components = useMemo(() => ({
    // --- Section dividers for h2 ---
    h2({ children }) {
      const text = extractTextFromChildren(children);
      // Status lines: leading emoji like ✅ ❌ ⚠️ 🎯
      const statusMatch = text.match(/^([✅❌⚠️🎯ℹ️])\s*(.+)$/);
      if (statusMatch) {
        const [, emoji, message] = statusMatch;
        const bg = emoji === "✅" ? "bg-green-500/10 text-green-700 dark:text-green-400"
          : emoji === "❌" ? "bg-red-500/10 text-red-700 dark:text-red-400"
          : emoji === "⚠️" ? "bg-yellow-500/10 text-yellow-700 dark:text-yellow-400"
          : "bg-primary/5 text-foreground";
        return (
          <div className={`my-3 rounded-md px-3 py-2 text-sm font-medium ${bg}`}>
            {emoji} {message}
          </div>
        );
      }
      return (
        <div className="my-5 flex items-center gap-3">
          <div className="h-px flex-1 bg-border" />
          <span className="text-xs font-bold uppercase tracking-wider text-foreground/70">
            {text}
          </span>
          <div className="h-px flex-1 bg-border" />
        </div>
      );
    },

    // --- Signal cards for li items matching **Bold** — desc ---
    li({ children }) {
      const text = extractTextFromChildren(children);
      const signalMatch = text.match(SIGNAL_ITEM_RE);

      if (signalMatch) {
        const [, title, description] = signalMatch;
        return (
          <li className="list-none -ml-4 my-1.5">
            <div className="rounded-md border bg-card px-3 py-2">
              <span className="font-medium text-sm">{title}</span>
              <span className="text-muted-foreground text-sm"> — {description}</span>
            </div>
          </li>
        );
      }

      // Action items: render as clickable buttons
      if (actionItems.has(text.trim())) {
        return (
          <li className="list-none -ml-4 my-1">
            <button
              onClick={() => onAction(text.trim())}
              className="flex w-full items-center gap-2 rounded-md px-3 py-1.5 text-left text-sm hover:bg-accent transition-colors group"
            >
              <ArrowRight className="h-3.5 w-3.5 shrink-0 text-muted-foreground group-hover:text-primary transition-colors" />
              <span>{children}</span>
            </button>
          </li>
        );
      }

      return <li>{children}</li>;
    },

    // --- CTA buttons extracted from paragraphs ---
    p({ children }) {
      const text = extractTextFromChildren(children);
      const { remainder, ctas } = extractCTAs(text);

      return (
        <>
          {remainder && <p>{remainder}</p>}
          {ctas.length > 0 && (
            <div className="mt-3 rounded-lg border bg-muted/30 px-4 py-3 not-prose overflow-hidden">
              <p className="text-xs font-medium text-muted-foreground mb-2">What would you like to do next?</p>
              <div className="flex flex-col gap-2">
                {ctas.map((cta) => (
                  <Button
                    key={cta}
                    variant="outline"
                    size="sm"
                    onClick={() => onAction(cta)}
                    className="text-xs h-auto py-1.5 px-3 bg-background whitespace-normal text-left justify-start"
                  >
                    {cta}
                  </Button>
                ))}
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => {}}
                  className="text-xs h-auto py-1.5 px-2 text-muted-foreground"
                >
                  <X className="h-3 w-3 mr-1" />
                  Dismiss
                </Button>
              </div>
            </div>
          )}
        </>
      );
    },

    // --- Styled tables ---
    table({ children }) {
      return (
        <div className="my-4 overflow-x-auto rounded-lg border not-prose">
          <table className="w-full text-sm table-fixed">{children}</table>
        </div>
      );
    },
    thead({ children }) {
      return <thead className="bg-muted/60">{children}</thead>;
    },
    th({ children }) {
      return (
        <th className="px-4 py-2.5 text-left text-xs font-bold text-foreground/80 first:w-[40%]">
          {children}
        </th>
      );
    },
    td({ children }) {
      return <td className="border-t border-border/50 px-4 py-2.5 align-top">{children}</td>;
    },

    // --- Lists: ensure bullets on regular items ---
    ul({ children }) {
      return <ul className="my-2 ml-1 list-disc space-y-1 pl-4 marker:text-muted-foreground">{children}</ul>;
    },
    ol({ children }) {
      return <ol className="my-2 ml-1 list-decimal space-y-1 pl-4 marker:text-muted-foreground">{children}</ol>;
    },

    // --- Horizontal rules: more breathing room ---
    hr() {
      return <hr className="my-5 border-border/60" />;
    },

    // --- Styled blockquotes ---
    blockquote({ children }) {
      return (
        <blockquote className="border-l-2 border-primary/40 pl-3 my-2 text-muted-foreground italic">
          {children}
        </blockquote>
      );
    },

    // --- Code blocks ---
    code({ children, className }) {
      const isBlock = className?.includes("language-");
      if (isBlock) {
        return (
          <code className={`${className} block overflow-x-auto rounded-md bg-muted p-3 text-xs`}>
            {children}
          </code>
        );
      }
      return (
        <code className="rounded bg-muted px-1.5 py-0.5 text-xs font-mono">
          {children}
        </code>
      );
    },

    // --- Strong emphasis ---
    strong({ children }) {
      return <strong className="font-semibold text-foreground">{children}</strong>;
    },

    // --- Links ---
    a({ href, children }) {
      return (
        <a
          href={href}
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary underline underline-offset-2 hover:text-primary/80"
        >
          {children}
        </a>
      );
    },
  }), [actionItems, onAction]);

  return (
    <div className={`prose prose-sm max-w-none dark:prose-invert ${compact ? "prose-compact" : ""}`}>
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
        {content}
      </ReactMarkdown>
    </div>
  );
}
