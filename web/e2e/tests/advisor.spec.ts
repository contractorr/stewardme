import { test, expect } from "@playwright/test";
import { installApiMocks, MOCK_SSE_ANSWER } from "../fixtures/api-mocks";

test.describe("Advisor Chat", () => {
  test.beforeEach(async ({ page }) => {
    await installApiMocks(page);
  });

  test("advisor page shows empty state", async ({ page }) => {
    await page.goto("/advisor");
    // Empty state heading: "What's on your mind?"
    await expect(page.getByRole("heading", { name: /on your mind/i })).toBeVisible({
      timeout: 10_000,
    });
  });

  test("send message and receive SSE response", async ({ page }) => {
    await page.goto("/advisor");
    await expect(page.getByRole("heading", { name: /on your mind/i })).toBeVisible({
      timeout: 10_000,
    });

    // Type a question
    const input = page.getByPlaceholder("Ask me anything...");
    await input.fill("How should I prioritize my day?");

    // Click the send button (last button in the input area)
    await page.locator("button").filter({ has: page.locator("svg.lucide-send") }).click();

    // User message should appear
    await expect(page.getByText("How should I prioritize my day?")).toBeVisible({
      timeout: 5_000,
    });

    // Mocked SSE response should appear
    await expect(
      page.getByText(MOCK_SSE_ANSWER.content.slice(0, 40), { exact: false }),
    ).toBeVisible({ timeout: 10_000 });
  });
});
