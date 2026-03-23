import path from "node:path";
import { test as setup, expect } from "@playwright/test";
import { installApiMocks } from "./api-mocks";

const AUTH_FILE = path.join(__dirname, "../.auth/user.json");

setup("authenticate as junior_dev", async ({ page }) => {
  // Install API mocks so DashboardShell's gate check passes after login
  await installApiMocks(page);

  await page.goto("/login");

  // Wait for the test-auth section to render
  await expect(page.locator("#test-username")).toBeVisible();

  // Select user and fill password
  await page.selectOption("#test-username", "junior_dev");
  await page.fill("#test-password", "test");

  // Click sign-in button
  await page.getByRole("button", { name: /Sign in as junior_dev/i }).click();

  // Wait for redirect to /home (NextAuth callback → /home)
  await page.waitForURL("**/home", { timeout: 15_000 });

  // Save auth state
  await page.context().storageState({ path: AUTH_FILE });
});
