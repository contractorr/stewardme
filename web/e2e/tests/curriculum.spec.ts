import { test, expect } from "@playwright/test";
import {
  installApiMocks,
  MOCK_ASSESSMENT_DRAFT,
  MOCK_GUIDE_DETAIL,
  MOCK_STATS,
  MOCK_TODAY,
  MOCK_TREE,
} from "../fixtures/api-mocks";

test.describe("Curriculum / Learn", () => {
  test.beforeEach(async ({ page }) => {
    await installApiMocks(page);
  });

  test("learn page shows guide grid and stats", async ({ page }) => {
    await page.goto("/learn");

    await expect(page.getByRole("heading", { name: "Today in Learn" })).toBeVisible({ timeout: 10_000 });
    await expect(page.getByText(MOCK_TODAY.tasks[0].title, { exact: true })).toBeVisible();
    await expect(page.getByRole("heading", { name: "Program paths" })).toBeVisible();

    // Stats row should render
    await expect(page.getByText("Enrolled")).toBeVisible({ timeout: 10_000 });
    await expect(
      page.getByText(`${MOCK_STATS.chapters_completed}/${MOCK_STATS.total_chapters}`),
    ).toBeVisible();
    await expect(page.getByText(`${MOCK_STATS.current_streak_days}d`)).toBeVisible();

    // Guide cards should render — use first() since title may appear in multiple places
    await expect(page.getByText("Python Basics").first()).toBeVisible();
    await expect(page.getByText("System Design").first()).toBeVisible();
  });

  test("navigate to guide detail and see chapters", async ({ page }) => {
    await page.goto("/learn");
    await expect(page.getByText("Enrolled")).toBeVisible({ timeout: 10_000 });

    // Click on the Python Basics guide card (not the "Continue reading" card)
    // The guide card links to /learn/python-basics (no chapter suffix)
    await page.locator('a[href="/learn/python-basics"]').click();

    // Guide detail page should load
    await page.waitForURL("**/learn/python-basics", { timeout: 10_000 });

    // Chapter list card should be visible
    await expect(page.getByText("Chapters", { exact: true })).toBeVisible({ timeout: 10_000 });
    await expect(page.getByText(MOCK_GUIDE_DETAIL.chapters[0].title)).toBeVisible();
    await expect(page.getByText(MOCK_GUIDE_DETAIL.chapters[2].title)).toBeVisible();
  });

  test("guide detail can launch an applied deliverable draft", async ({ page }) => {
    await page.goto("/learn/python-basics");
    await expect(page.getByText("Applied Assessment Pilot")).toBeVisible({ timeout: 10_000 });

    await page.getByRole("button", { name: "Create deliverable" }).click();

    await page.waitForURL(`**/journal?open=${encodeURIComponent(MOCK_ASSESSMENT_DRAFT.entry_path)}`, {
      timeout: 10_000,
    });
    await expect(page.getByRole("heading", { name: "Journal" })).toBeVisible();
  });

  test("home page surfaces the learning queue", async ({ page }) => {
    await page.goto("/");

    await expect(page.locator("text=Today in Learn").first()).toBeVisible({ timeout: 10_000 });
    await expect(page.getByText(MOCK_TODAY.tasks[0].title, { exact: true })).toBeVisible();
    await expect(page.getByText("Program paths").first()).toBeVisible();
    await expect(page.getByText("Operator Path")).toBeVisible();
  });

  test("tree program filter keeps applied modules visible", async ({ page }) => {
    await page.goto("/learn");
    await page.getByRole("tab", { name: "Tree" }).click();

    await expect(page.getByText("Core Curriculum")).toBeVisible({ timeout: 10_000 });
    await expect(page.getByText("Industry Applications")).toBeVisible();

    const learningPathControl = page.locator("div").filter({ hasText: "Learning Path:" }).locator("select");
    await learningPathControl.selectOption("operator-path");

    await expect(page.getByText("2 guides")).toBeVisible();
    await expect(page.getByText("Healthcare Industry")).toBeVisible();
    await expect(page.getByText("Finance Industry")).toHaveCount(0);
    await expect(page.getByText(MOCK_TREE.programs[0].description).first()).toBeVisible();
  });
});
