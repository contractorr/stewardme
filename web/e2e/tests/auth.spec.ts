import { test, expect } from "@playwright/test";
import { installApiMocks } from "../fixtures/api-mocks";

test.describe("Authentication", () => {
  test("unauthenticated user is redirected to /login", async ({ browser }) => {
    // Explicitly empty storageState — no cookies at all
    const ctx = await browser.newContext({
      storageState: { cookies: [], origins: [] },
    });
    const page = await ctx.newPage();
    await page.goto("/home", { waitUntil: "commit" });
    // NextAuth middleware or server-side auth should redirect to /login
    await page.waitForURL("**/login**", { timeout: 10_000 });
    await ctx.close();
  });

  test("login page renders OAuth buttons", async ({ browser }) => {
    const ctx = await browser.newContext({
      storageState: { cookies: [], origins: [] },
    });
    const page = await ctx.newPage();
    await page.goto("/login");
    await expect(page.getByRole("button", { name: /Continue with GitHub/i })).toBeVisible();
    await expect(page.getByRole("button", { name: /Continue with Google/i })).toBeVisible();
    await ctx.close();
  });

  test("authenticated user can access /home", async ({ page }) => {
    // This test uses the stored auth from auth.setup.ts (storageState)
    await installApiMocks(page);
    await page.goto("/home");
    await expect(page).toHaveURL(/\/home/);
    // DashboardShell should render — check for greeting or main content
    await expect(page.locator("h1")).toBeVisible({ timeout: 10_000 });
  });
});
