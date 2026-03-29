import { test, expect } from "@playwright/test";
import {
  installApiMocks,
  MOCK_GUIDE_DETAIL,
  MOCK_GUIDES,
  MOCK_RETRY_REVIEW_ITEMS,
  MOCK_TODAY,
} from "../fixtures/api-mocks";

test.describe("Curriculum / Library", () => {
  test.beforeEach(async ({ page }) => {
    await installApiMocks(page);
  });

  test("learn page focuses on next up, reviews, and guide browsing", async ({ page }) => {
    await page.goto("/learn");

    await expect(page.getByText("Next up")).toBeVisible({ timeout: 10_000 });
    await expect(page.getByText(MOCK_TODAY.tasks[0].title, { exact: true })).toBeVisible();
    await expect(page.getByText("Reviews", { exact: true })).toBeVisible();
    await expect(page.getByRole("link", { name: "Start review" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "Browse guides" })).toBeVisible();
    await expect(page.getByText(MOCK_GUIDES[0].title).first()).toBeVisible();
    await expect(page.getByText(MOCK_GUIDES[1].title).first()).toBeVisible();
  });

  test("learn page supports topic filtering and a clearer guide order", async ({ page }) => {
    await page.goto("/learn");
    const browseGuides = page.locator("#browse-guides");

    await page.getByRole("button", { name: "Business" }).click();
    await expect(browseGuides.getByText("Market Analysis").first()).toBeVisible();
    await expect(browseGuides.getByText("Python Basics").first()).not.toBeVisible();

    await page.getByRole("button", { name: "All" }).click();
    await expect(browseGuides.locator("a[href^=\"/learn/\"]").nth(0)).toContainText("Python Basics");

    await page.getByRole("combobox").click();
    await page.getByRole("option", { name: "A-Z" }).click();
    await expect(browseGuides.locator("a[href^=\"/learn/\"]").nth(0)).toContainText("Market Analysis");
  });

  test("guide detail shows one primary action and the chapter list", async ({ page }) => {
    await page.goto("/learn/python-basics");

    await expect(page.getByRole("button", { name: "Continue" })).toBeVisible({ timeout: 10_000 });
    await expect(page.getByText("Work through the guide one chapter at a time.")).toBeVisible();
    await expect(page.getByText("Chapters", { exact: true })).toBeVisible();
    await expect(page.getByText(MOCK_GUIDE_DETAIL.chapters[0].title)).toBeVisible();
    await expect(page.getByText(MOCK_GUIDE_DETAIL.chapters[2].title).last()).toBeVisible();
  });

  test("home page surfaces a single learning next step", async ({ page }) => {
    await page.goto("/");

    await expect(page.getByText("Learning").first()).toBeVisible({ timeout: 10_000 });
    await expect(page.getByText(MOCK_TODAY.tasks[0].title, { exact: true })).toBeVisible();
    await expect(page.getByText("2 reviews waiting.")).toBeVisible();
    await expect(page.getByRole("link", { name: "Open Guide Library" })).toBeVisible();
  });

  test("review page falls back to retry items through the single review flow", async ({ page }) => {
    await page.goto("/learn/review");

    await expect(page.getByRole("heading", { name: "Review" })).toBeVisible({
      timeout: 10_000,
    });
    await expect(page.getByText(MOCK_RETRY_REVIEW_ITEMS[0].question)).toBeVisible();
  });
});
