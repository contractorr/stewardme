"use client";

import { useEffect, useState } from "react";
import { Sparkles, RefreshCcw, Network, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { apiFetch } from "@/lib/api";

interface JournalEntry {
  path: string;
  title: string;
  type: string;
  created: string | null;
  tags: string[];
  preview: string;
  content?: string;
}

interface JournalMindMapNode {
  id: string;
  label: string;
  kind: string;
  weight: number;
  confidence: number;
  is_root: boolean;
  source_type?: string | null;
  source_label?: string;
  source_ref?: string;
}

interface JournalMindMapEdge {
  source: string;
  target: string;
  label: string;
  strength: number;
}

interface JournalMindMap {
  map_id: string;
  entry_path: string;
  entry_title: string;
  summary: string;
  rationale: string;
  generator: string;
  nodes: JournalMindMapNode[];
  edges: JournalMindMapEdge[];
  created_at: string;
  updated_at: string;
}

interface JournalMindMapEnvelope {
  status: "ready" | "not_available" | "insufficient_signal";
  mind_map: JournalMindMap | null;
}

const NODE_COLORS: Record<string, string> = {
  entry: "var(--primary)",
  theme: "var(--info)",
  action: "var(--success)",
  memory: "var(--warning)",
  thread: "var(--chart-2)",
  research: "var(--chart-4)",
  intel: "var(--chart-3)",
  conversation: "var(--chart-5)",
  tag: "var(--accent-foreground)",
};

async function requestMindMap(
  entryPath: string,
  token: string,
  method: "GET" | "POST" = "GET"
): Promise<JournalMindMapEnvelope> {
  return apiFetch<JournalMindMapEnvelope>(
    `/api/journal/${encodeURIComponent(entryPath)}/mind-map`,
    { method },
    token
  );
}

function wrapLabel(label: string): string[] {
  const words = label.split(/\s+/).filter(Boolean);
  const lines: string[] = [];
  let current = "";

  for (const word of words) {
    const next = current ? `${current} ${word}` : word;
    if (next.length <= 16) {
      current = next;
      continue;
    }
    if (current) {
      lines.push(current);
      current = word;
    } else {
      lines.push(word.slice(0, 16));
    }
    if (lines.length === 2) break;
  }

  if (current && lines.length < 2) lines.push(current);
  if (lines.length === 2 && words.join(" ").length > lines.join(" ").length) {
    lines[1] = `${lines[1].slice(0, 13)}...`;
  }

  return lines.slice(0, 2);
}

function getNodeRadius(node: JournalMindMapNode): number {
  if (node.is_root) return 42;
  return Math.max(26, Math.min(36, 22 + node.weight * 16));
}

function buildLayout(map: JournalMindMap) {
  const width = 640;
  const height = 420;
  const centerX = width / 2;
  const centerY = height / 2;
  const root = map.nodes.find((node) => node.is_root) ?? map.nodes[0];
  const others = map.nodes.filter((node) => node.id !== root.id);
  const radius = others.length > 5 ? 150 : 130;

  const positions = new Map<string, { x: number; y: number }>();
  positions.set(root.id, { x: centerX, y: centerY });

  others.forEach((node, index) => {
    const angle = (-Math.PI / 2) + (index * (Math.PI * 2)) / Math.max(others.length, 1);
    const ring = radius + (node.kind === "tag" ? 24 : 0);
    positions.set(node.id, {
      x: centerX + Math.cos(angle) * ring,
      y: centerY + Math.sin(angle) * ring,
    });
  });

  return { width, height, positions };
}

function MindMapGraph({ map }: { map: JournalMindMap }) {
  const { width, height, positions } = buildLayout(map);

  return (
    <div className="overflow-hidden rounded-xl border bg-muted/20">
      <svg viewBox={`0 0 ${width} ${height}`} className="h-auto w-full">
        <rect x="0" y="0" width={width} height={height} fill="var(--card)" />

        {map.edges.map((edge) => {
          const source = positions.get(edge.source);
          const target = positions.get(edge.target);
          if (!source || !target) return null;
          const midX = (source.x + target.x) / 2;
          const midY = (source.y + target.y) / 2;

          return (
            <g key={`${edge.source}-${edge.target}-${edge.label}`}>
              <line
                x1={source.x}
                y1={source.y}
                x2={target.x}
                y2={target.y}
                stroke="var(--border)"
                strokeWidth={Math.max(1.2, edge.strength * 2.2)}
                opacity={0.85}
              />
              <text
                x={midX}
                y={midY - 4}
                textAnchor="middle"
                fontSize="11"
                fill="var(--muted-foreground)"
              >
                {edge.label}
              </text>
            </g>
          );
        })}

        {map.nodes.map((node) => {
          const position = positions.get(node.id);
          if (!position) return null;
          const radius = getNodeRadius(node);
          const lines = wrapLabel(node.label);
          const color = NODE_COLORS[node.kind] ?? "var(--foreground)";

          return (
            <g key={node.id}>
              <circle
                cx={position.x}
                cy={position.y}
                r={radius}
                fill={node.is_root ? color : "var(--card)"}
                stroke={color}
                strokeWidth={node.is_root ? 0 : 2}
              />
              <text
                x={position.x}
                y={position.y - (lines.length - 1) * 8}
                textAnchor="middle"
                fontSize={node.is_root ? 13 : 12}
                fontWeight={node.is_root ? 600 : 500}
                fill={node.is_root ? "var(--primary-foreground)" : "var(--foreground)"}
              >
                {lines.map((line, index) => (
                  <tspan key={`${node.id}-${index}`} x={position.x} dy={index === 0 ? 0 : 16}>
                    {line}
                  </tspan>
                ))}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

function MindMapSkeleton() {
  return (
    <div className="space-y-3">
      <div className="h-4 w-44 animate-pulse rounded bg-muted" />
      <div className="h-[260px] animate-pulse rounded-xl border bg-muted/50" />
      <div className="h-3 w-3/4 animate-pulse rounded bg-muted" />
    </div>
  );
}

export function MindMapCard({
  entry,
  token,
}: {
  entry: JournalEntry;
  token: string | null | undefined;
}) {
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [envelope, setEnvelope] = useState<JournalMindMapEnvelope | null>(null);

  useEffect(() => {
    setEnvelope(null);
    if (!token) {
      setLoading(false);
      return;
    }

    let cancelled = false;

    const run = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await requestMindMap(entry.path, token, "GET");
        if (!cancelled) {
          setEnvelope(response);
        }
      } catch (err) {
        if (!cancelled) {
          setError((err as Error).message);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    void run();
    return () => {
      cancelled = true;
    };
  }, [entry.path, token]);

  const handleGenerate = async () => {
    if (!token) return;
    setGenerating(true);
    setError(null);
    try {
      const response = await requestMindMap(entry.path, token, "POST");
      setEnvelope(response);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setGenerating(false);
    }
  };

  const handleRetry = async () => {
    if (!token) return;
    setLoading(true);
    setError(null);
    try {
      const response = await requestMindMap(entry.path, token, "GET");
      setEnvelope(response);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const mindMap = envelope?.mind_map ?? null;
  const hasMap = envelope?.status === "ready" && !!mindMap;
  const isLowSignal = envelope?.status === "insufficient_signal";
  const externalNodes = (mindMap?.nodes ?? []).filter((node) =>
    ["research", "intel", "conversation"].includes(node.kind)
  );
  const externalFamilies = Array.from(new Set(externalNodes.map((node) => node.kind)));

  return (
    <Card className="border-dashed">
      <CardHeader className="gap-3">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="gap-1">
                <Sparkles className="h-3 w-3" /> Generated
              </Badge>
              {hasMap ? (
                <Badge variant="outline">{mindMap?.nodes.length ?? 0} nodes</Badge>
              ) : null}
            </div>
            <CardTitle className="text-base">Mind map</CardTitle>
            <CardDescription>
              Turn this entry into a compact visual structure, then augment it with matched
              research, RSS intel, and prior advisor conversations when they are relevant.
            </CardDescription>
          </div>

          <Button
            variant={hasMap ? "outline" : "default"}
            size="sm"
            onClick={handleGenerate}
            disabled={generating || !token}
          >
            {hasMap ? <RefreshCcw className="h-4 w-4" /> : <Network className="h-4 w-4" />}
            {generating ? "Generating..." : hasMap ? "Regenerate" : "Generate mind map"}
          </Button>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {loading ? <MindMapSkeleton /> : null}

        {!loading && error ? (
          <div className="rounded-lg border border-destructive/30 bg-destructive/5 p-3 text-sm">
            <div className="flex items-start gap-2">
              <AlertCircle className="mt-0.5 h-4 w-4 text-destructive" />
              <div className="space-y-2">
                <p>Mind map generation failed: {error}</p>
                <Button variant="outline" size="sm" onClick={handleRetry}>
                  Retry
                </Button>
              </div>
            </div>
          </div>
        ) : null}

        {!loading && !error && !hasMap ? (
          <div className="rounded-xl border bg-muted/20 p-4">
            {isLowSignal ? (
              <>
                <p className="text-sm text-foreground">
                  This entry does not have enough structure to map yet.
                </p>
                <p className="mt-1 text-sm text-muted-foreground">
                  Try again after the note includes clearer themes, constraints, or next steps.
                </p>
              </>
            ) : (
              <>
                <p className="text-sm text-foreground">
                  No map has been generated for this entry yet.
                </p>
                <p className="mt-1 text-sm text-muted-foreground">
                  StewardMe will only create a graph when the note has enough structure to surface
                  useful themes, actions, or recurring context.
                </p>
              </>
            )}
          </div>
        ) : null}

        {!loading && !error && hasMap && mindMap ? (
          <>
            <div className="space-y-2">
              <p className="text-sm text-foreground">{mindMap.summary}</p>
              <p className="text-xs text-muted-foreground">{mindMap.rationale}</p>
            </div>
            {externalFamilies.length > 0 ? (
              <div className="space-y-2 rounded-xl border bg-muted/20 p-3">
                <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                  Augmented with
                </p>
                <div className="flex flex-wrap gap-2">
                  {externalFamilies.map((family) => (
                    <Badge key={family} variant="outline">
                      {family === "intel" ? "RSS intel" : family}
                    </Badge>
                  ))}
                </div>
                <div className="flex flex-wrap gap-2">
                  {externalNodes.slice(0, 4).map((node) => (
                    <Badge key={node.id} variant="secondary" className="max-w-full truncate">
                      {node.source_label || node.label}
                    </Badge>
                  ))}
                </div>
              </div>
            ) : null}
            <MindMapGraph map={mindMap} />
          </>
        ) : null}
      </CardContent>
    </Card>
  );
}
