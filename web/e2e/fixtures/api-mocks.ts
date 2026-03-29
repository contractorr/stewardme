import type { Page } from "@playwright/test";

// ── Mock data (exported for assertions in specs) ──────────────────────

export const MOCK_USER = { name: "Junior Dev" };

export const MOCK_SETTINGS = {
  llm_api_key_set: true,
  using_shared_key: false,
  has_profile: true,
};

export const MOCK_GREETING = {
  text: "Welcome back. You have 3 journal entries this week.",
  return_brief: null,
  stale: false,
};

export const MOCK_GUIDE = {
  id: "python-basics",
  title: "Python Basics",
  category: "technology",
  difficulty: "introductory",
  chapter_count: 5,
  total_reading_time_minutes: 45,
  enrolled: true,
  progress_pct: 40,
  chapters_completed: 2,
};

export const MOCK_GUIDES = [
  MOCK_GUIDE,
  {
    id: "system-design",
    title: "System Design",
    category: "technology",
    difficulty: "advanced",
    chapter_count: 12,
    total_reading_time_minutes: 180,
    enrolled: false,
    progress_pct: 0,
    chapters_completed: 0,
  },
];

export const MOCK_STATS = {
  guides_enrolled: 1,
  guides_completed: 0,
  chapters_completed: 2,
  total_chapters: 17,
  total_reading_time_seconds: 2700,
  reviews_completed: 4,
  average_grade: 2.4,
  current_streak_days: 3,
  reviews_due: 2,
  mastery_by_category: {},
  mastery_by_track: {},
  daily_activity: {},
};

export const MOCK_NEXT = {
  guide_id: "python-basics",
  guide_title: "Python Basics",
  chapter: { id: "python-basics/ch03", title: "Functions and Scope" },
};

export const MOCK_TODAY = {
  headline: "Today in Learn",
  summary: "Today: Resume Functions and Scope • 2 reviews due • 1 active path",
  recommended_action: {
    guide_id: "python-basics",
    guide_title: "Python Basics",
    chapter: { id: "python-basics/ch03", title: "Functions and Scope" },
    reason: "Continue where you left off.",
    recommendation_type: "continue",
    signals: [
      {
        kind: "progress",
        label: "Active momentum",
        detail: "You already started this guide, so the shortest path is to keep moving.",
      },
    ],
    matched_programs: [
      {
        id: "operator-path",
        title: "Operator Path",
        audience: "Operators",
        description: "Core technical guide plus a healthcare capstone.",
        color: "#2563eb",
        outcomes: ["Build practical technical judgment"],
        guide_ids: ["python-basics"],
        applied_module_ids: ["industry-healthcare"],
      },
    ],
    applied_assessments: [
      {
        type: "decision_brief",
        stage: "review",
        title: "Decision brief",
        summary: "Use one framework from Python Basics to support a real decision.",
        deliverable: "One-page brief",
        prompt: "Write a brief.",
        evaluation_focus: ["Clear framing"],
      },
    ],
  },
  tasks: [
    {
      id: "recommendation:python-basics:python-basics/ch03",
      task_type: "continue_chapter",
      title: "Resume Functions and Scope",
      detail: "Continue where you left off.",
      cta_label: "Resume lesson",
      priority: 110,
      estimate_minutes: 12,
      guide_id: "python-basics",
      guide_title: "Python Basics",
      chapter_id: "python-basics/ch03",
      chapter_title: "Functions and Scope",
      recommendation_type: "continue",
      signals: [
        {
          kind: "progress",
          label: "Active momentum",
          detail: "You already started this guide, so the shortest path is to keep moving.",
        },
      ],
      matched_programs: [
        {
          id: "operator-path",
          title: "Operator Path",
          audience: "Operators",
          description: "Core technical guide plus a healthcare capstone.",
          color: "#2563eb",
          outcomes: ["Build practical technical judgment"],
          guide_ids: ["python-basics"],
          applied_module_ids: ["industry-healthcare"],
        },
      ],
      assessment: null,
    },
    {
      id: "due-reviews",
      task_type: "due_reviews",
      title: "Clear 2 due reviews",
      detail: "Clear recall work waiting across Python Basics.",
      cta_label: "Start reviews",
      priority: 96,
      estimate_minutes: 8,
      guide_id: null,
      guide_title: null,
      chapter_id: null,
      chapter_title: null,
      recommendation_type: null,
      review_count: 2,
      signals: [],
      matched_programs: [],
      assessment: null,
    },
    {
      id: "applied:python-basics:decision_brief",
      task_type: "applied_practice",
      title: "Decision brief",
      detail: "Use one framework from Python Basics to support a real decision.",
      cta_label: "Open guide",
      priority: 68,
      estimate_minutes: 20,
      guide_id: "python-basics",
      guide_title: "Python Basics",
      chapter_id: "python-basics/ch03",
      chapter_title: "Functions and Scope",
      recommendation_type: "continue",
      signals: [],
      matched_programs: [],
      assessment: {
        type: "decision_brief",
        stage: "review",
        title: "Decision brief",
        summary: "Use one framework from Python Basics to support a real decision.",
        deliverable: "One-page brief",
        prompt: "Write a brief.",
        evaluation_focus: ["Clear framing"],
      },
    },
  ],
  focus_programs: [
    {
      id: "operator-path",
      title: "Operator Path",
      audience: "Operators",
      description: "Core technical guide plus a healthcare capstone.",
      color: "#2563eb",
      outcomes: ["Build practical technical judgment"],
      guide_ids: ["python-basics"],
      applied_module_ids: ["industry-healthcare"],
      status: "active",
      total_guide_count: 2,
      enrolled_guide_count: 1,
      completed_guide_count: 0,
      in_progress_guide_count: 1,
      ready_guide_count: 1,
      progress_pct: 0,
    },
  ],
  reviews_due: 2,
};

export const MOCK_TREE = {
  tracks: {
    technology: {
      id: "technology",
      title: "Technology",
      description: "Technical foundations",
      color: "#2563eb",
      guide_count: 2,
      guides_completed: 0,
      average_mastery: 0,
      completion_pct: 0,
      guide_ids: ["python-basics", "system-design"],
    },
    industry: {
      id: "industry",
      title: "Industry",
      description: "Applied industry modules",
      color: "#059669",
      guide_count: 2,
      guides_completed: 0,
      average_mastery: 0,
      completion_pct: 0,
      guide_ids: ["industry-healthcare", "industry-finance"],
    },
  },
  programs: [
    {
      id: "operator-path",
      title: "Operator Path",
      audience: "Operators",
      description: "Core technical guide plus a healthcare capstone.",
      color: "#2563eb",
      outcomes: ["Build practical technical judgment"],
      guide_ids: ["python-basics"],
      applied_module_ids: ["industry-healthcare"],
    },
  ],
  nodes: [
    {
      id: "python-basics",
      title: "Python Basics",
      track: "technology",
      category: "technology",
      difficulty: "introductory",
      chapter_count: 5,
      prerequisites: [],
      is_entry_point: true,
      status: "enrolled",
      enrolled: true,
      progress_pct: 40,
      mastery_score: 25,
      chapters_completed: 2,
      chapters_total: 5,
      position: { x: 0, y: 0, depth: 0 },
    },
    {
      id: "system-design",
      title: "System Design",
      track: "technology",
      category: "technology",
      difficulty: "advanced",
      chapter_count: 12,
      prerequisites: ["python-basics"],
      is_entry_point: false,
      status: "not_started",
      enrolled: false,
      progress_pct: 0,
      mastery_score: 0,
      chapters_completed: 0,
      chapters_total: 12,
      position: { x: 0, y: 1, depth: 1 },
    },
    {
      id: "industry-healthcare",
      title: "Healthcare Industry",
      track: "industry",
      category: "industry",
      difficulty: "intermediate",
      chapter_count: 1,
      prerequisites: [],
      is_entry_point: false,
      status: "not_started",
      enrolled: false,
      progress_pct: 0,
      mastery_score: 0,
      chapters_completed: 0,
      chapters_total: 1,
      position: { x: 0, y: 0, depth: 0 },
    },
    {
      id: "industry-finance",
      title: "Finance Industry",
      track: "industry",
      category: "industry",
      difficulty: "intermediate",
      chapter_count: 1,
      prerequisites: [],
      is_entry_point: false,
      status: "not_started",
      enrolled: false,
      progress_pct: 0,
      mastery_score: 0,
      chapters_completed: 0,
      chapters_total: 1,
      position: { x: 1, y: 0, depth: 0 },
    },
  ],
  edges: [{ source: "python-basics", target: "system-design" }],
};

export const MOCK_GUIDE_DETAIL = {
  id: "python-basics",
  title: "Python Basics",
  category: "technology",
  difficulty: "introductory",
  chapter_count: 5,
  total_reading_time_minutes: 45,
  enrolled: true,
  progress_pct: 40,
  chapters_completed: 2,
  has_glossary: false,
  enrollment_completed_at: null,
  applied_assessments: [
    {
      type: "decision_brief",
      stage: "review",
      title: "Decision brief",
      summary: "Use one framework from Python Basics to support a real decision.",
      deliverable: "One-page brief",
      prompt: "Write a short brief for a technical trade-off.",
      evaluation_focus: ["Clear framing", "Recommendation quality"],
    },
  ],
  chapters: [
    { id: "python-basics/ch01", title: "Introduction", status: "completed", reading_time_minutes: 8 },
    { id: "python-basics/ch02", title: "Variables & Types", status: "completed", reading_time_minutes: 10 },
    { id: "python-basics/ch03", title: "Functions and Scope", status: "not_started", reading_time_minutes: 12 },
    { id: "python-basics/ch04", title: "Control Flow", status: "not_started", reading_time_minutes: 8 },
    { id: "python-basics/ch05", title: "Data Structures", status: "not_started", reading_time_minutes: 7 },
  ],
};

export const MOCK_ASSESSMENT_DRAFT = {
  guide_id: "python-basics",
  assessment_type: "decision_brief",
  entry_path: "C:/mock-journal/python-basics-decision-brief.md",
  entry_title: "Python Basics - Decision brief",
  goal_path: "C:/mock-journal/python-basics-decision-brief-goal.md",
  goal_title: "Apply Python Basics: Decision brief",
  created: true,
};

export const MOCK_JOURNAL_ENTRY = {
  path: MOCK_ASSESSMENT_DRAFT.entry_path,
  title: MOCK_ASSESSMENT_DRAFT.entry_title,
  type: "action_brief",
  created: "2026-03-29T09:00:00Z",
  tags: ["learning", "assessment"],
  content: "# Decision brief\n\nDraft content here.",
};

export const MOCK_SSE_ANSWER = {
  type: "answer",
  content: "Based on your journal, I'd recommend focusing on deep work blocks in the morning.",
  conversation_id: "conv-smoke-1",
  council_used: false,
};

// ── Route installer ───────────────────────────────────────────────────

export async function installApiMocks(page: Page) {
  // Settings (onboarding gate)
  await page.route("**/api/v1/settings", (route) =>
    route.fulfill({ json: MOCK_SETTINGS }),
  );

  // User identity
  await page.route("**/api/v1/user/me", (route) =>
    route.fulfill({ json: MOCK_USER }),
  );

  // Home page
  await page.route("**/api/v1/greeting", (route) =>
    route.fulfill({ json: MOCK_GREETING }),
  );
  await page.route("**/api/v1/suggestions*", (route) =>
    route.fulfill({ json: [] }),
  );
  await page.route("**/api/v1/journal?limit=200", (route) =>
    route.fulfill({ json: [] }),
  );
  await page.route("**/api/v1/journal?limit=100", (route) =>
    route.fulfill({ json: [MOCK_JOURNAL_ENTRY] }),
  );
  await page.route("**/api/v1/journal/*/mind-map", (route) =>
    route.fulfill({ json: { status: "not_available", mind_map: null } }),
  );
  await page.route("**/api/v1/journal/*", (route) =>
    route.fulfill({ json: MOCK_JOURNAL_ENTRY }),
  );
  await page.route("**/api/v1/goals", (route) =>
    route.fulfill({ json: [] }),
  );

  // Home stats
  await page.route("**/api/v1/home/stats", (route) =>
    route.fulfill({ json: { journal_entries: 12, active_goals: 3, thread_count: 5 } }),
  );

  // Advisor
  await page.route("**/api/v1/advisor/conversations", (route) => {
    if (route.request().method() === "GET") {
      return route.fulfill({ json: [] });
    }
    return route.fulfill({ json: {} });
  });

  await page.route("**/api/v1/advisor/ask/stream", (route) => {
    const sseBody = `data: ${JSON.stringify(MOCK_SSE_ANSWER)}\n\n`;
    return route.fulfill({
      status: 200,
      headers: { "Content-Type": "text/event-stream" },
      body: sseBody,
    });
  });

  // Curriculum — register detail route FIRST (more specific)
  await page.route(
    "**/api/v1/curriculum/guides/python-basics/assessments/decision_brief/launch",
    (route) => route.fulfill({ json: MOCK_ASSESSMENT_DRAFT }),
  );
  await page.route("**/api/v1/curriculum/guides/*", (route) =>
    route.fulfill({ json: MOCK_GUIDE_DETAIL }),
  );
  // Guide list (exact path — no trailing segments)
  await page.route("**/api/v1/curriculum/guides", (route) =>
    route.fulfill({ json: MOCK_GUIDES }),
  );
  await page.route("**/api/v1/curriculum/stats", (route) =>
    route.fulfill({ json: MOCK_STATS }),
  );
  await page.route("**/api/v1/curriculum/next", (route) =>
    route.fulfill({ json: MOCK_NEXT }),
  );
  await page.route("**/api/v1/curriculum/today", (route) =>
    route.fulfill({ json: MOCK_TODAY }),
  );
  await page.route("**/api/v1/curriculum/tree", (route) =>
    route.fulfill({ json: MOCK_TREE }),
  );

  // Fire-and-forget endpoints
  await page.route("**/api/v1/page-view*", (route) =>
    route.fulfill({ status: 204, body: "" }),
  );
  await page.route("**/api/v1/pageview*", (route) =>
    route.fulfill({ status: 204, body: "" }),
  );
  await page.route("**/api/v1/engagement*", (route) =>
    route.fulfill({ status: 204, body: "" }),
  );
}
