"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { toast } from "sonner";
import { Loader2 } from "lucide-react";
import { useToken } from "@/hooks/useToken";
import { apiFetch } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import type {
  SkillTreeResponse,
  SkillTreeNode,
  SkillTreeEdge,
  Track,
} from "@/types/curriculum";
import { SkillTreeNodeCard } from "./SkillTreeNode";
import { SkillTreeEdges } from "./SkillTreeEdges";

export function SkillTree() {
  const token = useToken();
  const [data, setData] = useState<SkillTreeResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedTracks, setSelectedTracks] = useState<Set<string>>(new Set());
  const containerRef = useRef<HTMLDivElement>(null);
  const nodeRefs = useRef<Map<string, HTMLDivElement>>(new Map());
  const [nodePositions, setNodePositions] = useState<Map<string, DOMRect>>(new Map());
  const [containerRect, setContainerRect] = useState<DOMRect | null>(null);
  const [measureTick, setMeasureTick] = useState(0);

  useEffect(() => {
    if (!token) return;
    setLoading(true);
    apiFetch<SkillTreeResponse>("/api/curriculum/tree", {}, token)
      .then(setData)
      .catch((e) => toast.error((e as Error).message))
      .finally(() => setLoading(false));
  }, [token]);

  // Measure node positions after render
  useEffect(() => {
    if (!data || !containerRef.current) return;
    const cRect = containerRef.current.getBoundingClientRect();
    const positions = new Map<string, DOMRect>();
    nodeRefs.current.forEach((el, id) => {
      positions.set(id, el.getBoundingClientRect());
    });
    setContainerRect(cRect);
    setNodePositions(positions);
  }, [data, selectedTracks, measureTick]);

  // ResizeObserver for re-measurement
  useEffect(() => {
    if (!containerRef.current) return;
    const observer = new ResizeObserver(() => setMeasureTick((t) => t + 1));
    observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, [data]);

  const toggleTrack = (trackId: string) => {
    setSelectedTracks((prev) => {
      const next = new Set(prev);
      if (next.has(trackId)) next.delete(trackId);
      else next.add(trackId);
      return next;
    });
  };

  const filteredNodes = useMemo((): SkillTreeNode[] => {
    if (!data) return [];
    if (selectedTracks.size === 0) return data.nodes;
    return data.nodes.filter((n) => selectedTracks.has(n.track));
  }, [data, selectedTracks]);

  const filteredEdges = useMemo((): SkillTreeEdge[] => {
    if (!data) return [];
    const nodeIds = new Set(filteredNodes.map((n) => n.id));
    return data.edges.filter((e) => nodeIds.has(e.source) && nodeIds.has(e.target));
  }, [data, filteredNodes]);

  const depthRows = useMemo(() => {
    const groups = new Map<number, SkillTreeNode[]>();
    for (const node of filteredNodes) {
      const d = node.position.depth;
      if (!groups.has(d)) groups.set(d, []);
      groups.get(d)!.push(node);
    }
    // Sort within each row by x position
    for (const row of groups.values()) {
      row.sort((a, b) => a.position.x - b.position.x);
    }
    return Array.from(groups.entries()).sort(([a], [b]) => a - b);
  }, [filteredNodes]);

  const getTrackColor = useCallback(
    (nodeId: string): string => {
      if (!data) return "#888";
      const node = data.nodes.find((n) => n.id === nodeId);
      if (!node) return "#888";
      return data.tracks[node.track]?.color ?? "#888";
    },
    [data],
  );

  const setNodeRef = useCallback((id: string, el: HTMLDivElement | null) => {
    if (el) nodeRefs.current.set(id, el);
    else nodeRefs.current.delete(id);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-16">
        <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (!data || data.nodes.length === 0) {
    return (
      <div className="rounded-lg border border-dashed p-8 text-center">
        <p className="text-sm text-muted-foreground">No skill tree data available</p>
      </div>
    );
  }

  const tracks = Object.values(data.tracks) as Track[];

  return (
    <div className="space-y-4">
      {/* Track filter bar */}
      <div className="flex flex-wrap gap-1.5 px-1">
        {tracks.map((track) => (
          <Badge
            key={track.id}
            variant={
              selectedTracks.size === 0 || selectedTracks.has(track.id)
                ? "default"
                : "outline"
            }
            className="cursor-pointer text-xs"
            style={
              selectedTracks.size === 0 || selectedTracks.has(track.id)
                ? { backgroundColor: track.color, borderColor: track.color }
                : { color: track.color, borderColor: track.color }
            }
            onClick={() => toggleTrack(track.id)}
          >
            {track.title}
          </Badge>
        ))}
        {selectedTracks.size > 0 && (
          <Badge
            key="clear-filter"
            variant="outline"
            className="cursor-pointer text-xs"
            onClick={() => setSelectedTracks(new Set())}
          >
            Clear
          </Badge>
        )}
      </div>

      {/* Tree container */}
      <div ref={containerRef} className="relative overflow-x-auto pb-4">
        {filteredNodes.length === 0 ? (
          <div className="rounded-lg border border-dashed p-8 text-center">
            <p className="text-sm text-muted-foreground">
              No guides match the selected filters
            </p>
            <Badge
              variant="outline"
              className="cursor-pointer text-xs mt-3"
              onClick={() => setSelectedTracks(new Set())}
            >
              Clear filters
            </Badge>
          </div>
        ) : (
          <>
            <SkillTreeEdges
              edges={filteredEdges}
              nodePositions={nodePositions}
              containerRect={containerRect}
              getTrackColor={getTrackColor}
            />

            <div className="relative z-10 flex flex-col gap-8">
              {depthRows.map(([depth, nodes]) => (
                <div key={depth} className="flex flex-wrap justify-center gap-3">
                  {nodes.map((node) => (
                    <SkillTreeNodeCard
                      key={node.id}
                      ref={(el) => setNodeRef(node.id, el)}
                      node={node}
                      trackColor={data.tracks[node.track]?.color ?? "#888"}
                    />
                  ))}
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
