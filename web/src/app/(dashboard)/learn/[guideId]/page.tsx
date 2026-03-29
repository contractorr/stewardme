"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { toast } from "sonner";
import {
  ArrowLeft,
  BookOpen,
  Clock,
  GraduationCap,
  Play,
  Plus,
  Trash2,
} from "lucide-react";

import { ChapterList } from "@/components/curriculum/ChapterList";
import { DifficultyBadge } from "@/components/curriculum/DifficultyBadge";
import { ProgressRing } from "@/components/curriculum/ProgressRing";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { useToken } from "@/hooks/useToken";
import { apiFetch } from "@/lib/api";
import type {
  AppliedAssessmentLaunchResult,
  GuideDepth,
  GuideDetail,
  PlacementQuestion,
  PlacementResult,
} from "@/types/curriculum";

function formatTime(minutes: number): string {
  if (minutes < 60) return `${minutes}m`;
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return m > 0 ? `${h}h ${m}m` : `${h}h`;
}

const depthLabels: Record<GuideDepth, string> = {
  survey: "Survey",
  practitioner: "Practitioner",
  deep_dive: "Deep dive",
};

const assessmentStageLabels: Record<string, string> = {
  chapter_completion: "After chapter",
  review: "Review",
  scenario_practice: "Scenario",
  capstone: "Capstone",
};

export default function GuideDetailPage() {
  const token = useToken();
  const params = useParams();
  const router = useRouter();
  const guideId = params.guideId as string;

  const [guide, setGuide] = useState<GuideDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState(false);
  const [archiveLoading, setArchiveLoading] = useState(false);
  const [extendOpen, setExtendOpen] = useState(false);
  const [extending, setExtending] = useState(false);
  const [launchingAssessmentType, setLaunchingAssessmentType] = useState<string | null>(null);
  const resolvedGuideId = guide?.id ?? guideId;

  const [extensionForm, setExtensionForm] = useState({
    prompt: "",
    depth: "practitioner" as GuideDepth,
    audience: "",
    time_budget: "",
    instruction: "",
  });

  const [showPlacement, setShowPlacement] = useState(false);
  const [placementQuestions, setPlacementQuestions] = useState<PlacementQuestion[]>([]);
  const [placementAnswers, setPlacementAnswers] = useState<Record<string, string>>({});
  const [placementResult, setPlacementResult] = useState<PlacementResult | null>(null);
  const [placementLoading, setPlacementLoading] = useState(false);

  useEffect(() => {
    if (!token || !guideId) return;
    setLoading(true);
    apiFetch<GuideDetail>(`/api/v1/curriculum/guides/${guideId}`, {}, token)
      .then(setGuide)
      .catch((e) => toast.error((e as Error).message))
      .finally(() => setLoading(false));
  }, [token, guideId]);

  const handleEnroll = async () => {
    if (!token) return;
    setEnrolling(true);
    try {
      await apiFetch(
        `/api/v1/curriculum/guides/${resolvedGuideId}/enroll`,
        { method: "POST" },
        token,
      );
      const updated = await apiFetch<GuideDetail>(
        `/api/v1/curriculum/guides/${resolvedGuideId}`,
        {},
        token,
      );
      setGuide(updated);
      toast.success("Enrolled");
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setEnrolling(false);
    }
  };

  const handleExtendGuide = async () => {
    if (!token) return;
    setExtending(true);
    try {
      const created = await apiFetch<GuideDetail>(
        `/api/v1/curriculum/guides/${resolvedGuideId}/extend`,
        {
          method: "POST",
          body: JSON.stringify({
            prompt: extensionForm.prompt.trim(),
            depth: extensionForm.depth,
            audience: extensionForm.audience.trim() || undefined,
            time_budget: extensionForm.time_budget.trim() || undefined,
            instruction: extensionForm.instruction.trim() || undefined,
          }),
        },
        token,
      );
      setExtendOpen(false);
      setExtensionForm({
        prompt: "",
        depth: "practitioner",
        audience: "",
        time_budget: "",
        instruction: "",
      });
      toast.success(`Created ${created.title}`);
      router.push(`/learn/${created.id}`);
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setExtending(false);
    }
  };

  const handleArchiveGuide = async () => {
    if (!token) return;
    if (!window.confirm("Archive this guide? You can restore it later from Learn.")) {
      return;
    }
    setArchiveLoading(true);
    try {
      await apiFetch(
        `/api/v1/curriculum/guides/${resolvedGuideId}`,
        { method: "DELETE" },
        token,
      );
      toast.success("Guide archived");
      router.push("/learn");
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setArchiveLoading(false);
    }
  };

  const handleStartPlacement = async () => {
    if (!token) return;
    setPlacementLoading(true);
    setPlacementResult(null);
    setPlacementAnswers({});
    try {
      const data = await apiFetch<{ questions: PlacementQuestion[] }>(
        `/api/v1/curriculum/guides/${resolvedGuideId}/placement/generate`,
        { method: "POST" },
        token,
      );
      setPlacementQuestions(data.questions);
      setShowPlacement(true);
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setPlacementLoading(false);
    }
  };

  const handleSubmitPlacement = async () => {
    if (!token) return;
    setPlacementLoading(true);
    try {
      const result = await apiFetch<PlacementResult>(
        `/api/v1/curriculum/guides/${resolvedGuideId}/placement/submit`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ answers: placementAnswers }),
        },
        token,
      );
      setPlacementResult(result);
      if (result.passed) {
        toast.success("Placement passed and guide completed");
        const updated = await apiFetch<GuideDetail>(
          `/api/v1/curriculum/guides/${resolvedGuideId}`,
          {},
          token,
        );
        setGuide(updated);
      }
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setPlacementLoading(false);
    }
  };

  const handleLaunchAssessment = async (assessmentType: string) => {
    if (!token) return;
    setLaunchingAssessmentType(assessmentType);
    try {
      const artifact = await apiFetch<AppliedAssessmentLaunchResult>(
        `/api/v1/curriculum/guides/${resolvedGuideId}/assessments/${assessmentType}/launch`,
        { method: "POST" },
        token,
      );
      toast.success(artifact.created ? "Draft created in Journal" : "Opening existing draft");
      router.push(`/journal?open=${encodeURIComponent(artifact.entry_path)}`);
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setLaunchingAssessmentType(null);
    }
  };

  const isGuideCompleted = !!guide?.enrollment_completed_at;
  const firstUnread = guide?.chapters?.find(
    (chapter) => !chapter.is_glossary && chapter.status !== "completed",
  );

  if (loading) {
    return (
      <div className="space-y-4">
        <div className="h-8 w-48 animate-pulse rounded bg-muted" />
        <div className="h-40 animate-pulse rounded-lg bg-muted" />
      </div>
    );
  }

  if (!guide) {
    return (
      <div className="py-12 text-center">
        <p className="text-muted-foreground">Guide not found</p>
        <Link href="/learn">
          <Button variant="ghost" className="mt-2">
            Back to guides
          </Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl space-y-6 p-4 md:p-6">
      <div className="flex items-center gap-2">
        <Link href="/learn">
          <Button variant="ghost" size="icon" className="h-8 w-8">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <h1 className="text-2xl font-semibold tracking-tight">{guide.title}</h1>
      </div>

      <Card>
        <CardContent className="flex flex-wrap items-center justify-between gap-4 p-5">
          <div className="space-y-3">
            <div className="flex flex-wrap items-center gap-3">
              {guide.origin === "user" ? (
                <Badge variant="outline" className="text-[10px]">
                  Your guide
                </Badge>
              ) : (
                <Badge variant="secondary" className="text-[10px]">
                  Built-in
                </Badge>
              )}
              {guide.kind === "extension" && (
                <Badge variant="outline" className="text-[10px]">
                  Extension
                </Badge>
              )}
              <DifficultyBadge level={guide.difficulty} />
              <span className="flex items-center gap-1 text-sm text-muted-foreground">
                <BookOpen className="h-3.5 w-3.5" />
                {guide.chapter_count} chapters
              </span>
              <span className="flex items-center gap-1 text-sm text-muted-foreground">
                <Clock className="h-3.5 w-3.5" />
                {formatTime(guide.total_reading_time_minutes)}
              </span>
              {guide.has_glossary && (
                <Badge variant="outline" className="text-[10px]">
                  Glossary
                </Badge>
              )}
            </div>

            {guide.base_guide_id && (
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-xs font-medium text-muted-foreground">Extends:</span>
                <Link href={`/learn/${guide.base_guide_id}`}>
                  <Badge variant="outline" className="text-[10px]">
                    {guide.base_guide_id}
                  </Badge>
                </Link>
              </div>
            )}

            {(guide.learning_programs?.length ?? 0) > 0 && (
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-xs font-medium text-muted-foreground">Programs:</span>
                {guide.learning_programs?.map((program) => (
                  <Badge
                    key={program.id}
                    variant="outline"
                    className="text-[10px]"
                    style={{ borderColor: program.color, color: program.color }}
                    title={program.description}
                  >
                    {program.title}
                  </Badge>
                ))}
              </div>
            )}
          </div>

          <div className="flex flex-wrap items-center gap-3">
            {guide.enrolled && (
              <ProgressRing progress={guide.progress_pct ?? 0} size={44} strokeWidth={4} />
            )}
            {!guide.enrolled && (
              <Button onClick={handleEnroll} disabled={enrolling}>
                {enrolling ? "Enrolling..." : "Enroll"}
              </Button>
            )}
            <Button variant="outline" onClick={() => setExtendOpen(true)}>
              <Plus className="mr-1.5 h-3.5 w-3.5" />
              Extend guide
            </Button>
            {guide.origin === "user" && (
              <Button
                variant="outline"
                onClick={() => void handleArchiveGuide()}
                disabled={archiveLoading}
              >
                <Trash2 className="mr-1.5 h-3.5 w-3.5" />
                {archiveLoading ? "Archiving..." : "Delete guide"}
              </Button>
            )}
            {!isGuideCompleted && (
              <Button
                variant="outline"
                onClick={handleStartPlacement}
                disabled={placementLoading}
              >
                <GraduationCap className="mr-1.5 h-3.5 w-3.5" />
                {placementLoading ? "Generating..." : "Test out"}
              </Button>
            )}
            {firstUnread && (
              <Link href={`/learn/${resolvedGuideId}/${firstUnread.id.split("/").pop()}`}>
                <Button>
                  <Play className="mr-1.5 h-3.5 w-3.5" />
                  {guide.chapters_completed ? "Continue" : "Start reading"}
                </Button>
              </Link>
            )}
          </div>
        </CardContent>
      </Card>

      {(guide.linked_extensions?.length ?? 0) > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Extensions</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-3 md:grid-cols-2">
            {guide.linked_extensions?.map((extension) => (
              <Link key={extension.id} href={`/learn/${extension.id}`}>
                <div className="h-full rounded-lg border p-4 transition-colors hover:border-primary/40">
                  <div className="flex flex-wrap items-center gap-2">
                    <p className="font-medium">{extension.title}</p>
                    <Badge variant="outline" className="text-[10px]">
                      Extension
                    </Badge>
                  </div>
                  <p className="mt-2 text-sm text-muted-foreground">
                    {extension.chapter_count} chapters,{" "}
                    {formatTime(extension.total_reading_time_minutes)}
                  </p>
                </div>
              </Link>
            ))}
          </CardContent>
        </Card>
      )}

      {(guide.applied_assessments?.length ?? 0) > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Applied Assessment Pilot</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-3 lg:grid-cols-2">
            {guide.applied_assessments?.map((assessment) => (
              <div
                key={`${assessment.stage}-${assessment.type}`}
                className="space-y-2 rounded-lg border p-3"
              >
                <div className="flex flex-wrap items-center gap-2">
                  <Badge variant="outline" className="text-[10px]">
                    {assessmentStageLabels[assessment.stage] ?? assessment.stage}
                  </Badge>
                  {assessment.draft_status && (
                    <Badge variant="secondary" className="text-[10px]">
                      {assessment.draft_status}
                    </Badge>
                  )}
                  {assessment.draft_feedback && (
                    <Badge variant="outline" className="text-[10px]">
                      Grade {assessment.draft_feedback.grade}/5
                    </Badge>
                  )}
                  <p className="text-sm font-medium">{assessment.title}</p>
                </div>
                <p className="text-sm text-muted-foreground">{assessment.summary}</p>
                <p className="text-xs text-muted-foreground">{assessment.deliverable}</p>
                <p className="text-xs">{assessment.prompt}</p>
                <p className="text-xs text-muted-foreground">
                  Evaluate on {assessment.evaluation_focus.join(", ").toLowerCase()}.
                </p>
                {assessment.draft_feedback && (
                  <p className="text-xs text-muted-foreground">
                    {assessment.draft_feedback.feedback}
                  </p>
                )}
                <div className="flex flex-wrap gap-2 pt-1">
                  {assessment.draft_entry_path ? (
                    <Link href={`/journal?open=${encodeURIComponent(assessment.draft_entry_path)}`}>
                      <Button size="sm" variant="outline">
                        {assessment.draft_status === "active" ? "Revise draft" : "Open draft"}
                      </Button>
                    </Link>
                  ) : (
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => void handleLaunchAssessment(assessment.type)}
                      disabled={launchingAssessmentType === assessment.type}
                    >
                      {launchingAssessmentType === assessment.type
                        ? "Creating..."
                        : "Create deliverable"}
                    </Button>
                  )}
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {showPlacement && placementQuestions.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <GraduationCap className="h-4 w-4" />
              Placement Quiz
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {placementResult ? (
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <Badge variant={placementResult.passed ? "default" : "destructive"}>
                    {placementResult.passed ? "Passed" : "Not passed"}
                  </Badge>
                  <span className="text-sm text-muted-foreground">
                    Average: {placementResult.average_grade.toFixed(1)} / 5 (need{" "}
                    {placementResult.threshold})
                  </span>
                </div>
                {placementResult.results.map((r, i) => (
                  <div key={r.question_id} className="space-y-1 rounded border p-3 text-sm">
                    <p className="font-medium">
                      Q{i + 1}: {placementQuestions[i]?.question}
                    </p>
                    <p className="text-muted-foreground">
                      Grade: {r.grade}/5 - {r.feedback}
                    </p>
                  </div>
                ))}
                {!placementResult.passed && (
                  <div className="flex gap-2">
                    {firstUnread && (
                      <Link href={`/learn/${resolvedGuideId}/${firstUnread.id.split("/").pop()}`}>
                        <Button>Start reading instead</Button>
                      </Link>
                    )}
                    <Button variant="ghost" onClick={() => setShowPlacement(false)}>
                      Dismiss
                    </Button>
                  </div>
                )}
              </div>
            ) : (
              <>
                {placementQuestions.map((q, i) => (
                  <div key={q.id} className="space-y-1.5">
                    <label className="text-sm font-medium">
                      {i + 1}. {q.question}
                    </label>
                    <Input
                      placeholder="Your answer..."
                      value={placementAnswers[q.id] ?? ""}
                      onChange={(e) =>
                        setPlacementAnswers((prev) => ({ ...prev, [q.id]: e.target.value }))
                      }
                    />
                  </div>
                ))}
                <div className="flex gap-2">
                  <Button
                    onClick={handleSubmitPlacement}
                    disabled={
                      placementLoading ||
                      Object.keys(placementAnswers).length < placementQuestions.length
                    }
                  >
                    {placementLoading ? "Grading..." : "Submit"}
                  </Button>
                  <Button variant="ghost" onClick={() => setShowPlacement(false)}>
                    Cancel
                  </Button>
                </div>
              </>
            )}
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Chapters</CardTitle>
        </CardHeader>
        <CardContent>
          <ChapterList guideId={resolvedGuideId} chapters={guide.chapters ?? []} />
        </CardContent>
      </Card>

      <Dialog open={extendOpen} onOpenChange={setExtendOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Extend Guide</DialogTitle>
            <DialogDescription>
              Create a separate linked guide with additional material for this topic.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">What should this extension cover?</label>
              <Textarea
                value={extensionForm.prompt}
                onChange={(event) =>
                  setExtensionForm((current) => ({
                    ...current,
                    prompt: event.target.value,
                  }))
                }
                rows={4}
                placeholder="Add case studies for regulated AI launches and decision frameworks for model risk."
              />
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <label className="text-sm font-medium">Depth</label>
                <select
                  value={extensionForm.depth}
                  onChange={(event) =>
                    setExtensionForm((current) => ({
                      ...current,
                      depth: event.target.value as GuideDepth,
                    }))
                  }
                  className="h-9 w-full rounded-md border bg-background px-3 text-sm"
                >
                  {Object.entries(depthLabels).map(([value, label]) => (
                    <option key={value} value={value}>
                      {label}
                    </option>
                  ))}
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Time Budget</label>
                <Input
                  value={extensionForm.time_budget}
                  onChange={(event) =>
                    setExtensionForm((current) => ({
                      ...current,
                      time_budget: event.target.value,
                    }))
                  }
                  placeholder="2 focused sessions"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">Audience</label>
              <Input
                value={extensionForm.audience}
                onChange={(event) =>
                  setExtensionForm((current) => ({
                    ...current,
                    audience: event.target.value,
                  }))
                }
                placeholder="Technical product lead"
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">Instruction</label>
              <Textarea
                value={extensionForm.instruction}
                onChange={(event) =>
                  setExtensionForm((current) => ({
                    ...current,
                    instruction: event.target.value,
                  }))
                }
                rows={4}
                placeholder="Optional: emphasize trade-offs, implementation pitfalls, and decision criteria."
              />
            </div>
          </div>

          <DialogFooter>
            <Button
              onClick={() => void handleExtendGuide()}
              disabled={extending || !extensionForm.prompt.trim()}
            >
              {extending ? "Creating..." : "Create extension"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
