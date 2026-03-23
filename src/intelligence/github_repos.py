"""GitHub API client for read-only repo monitoring."""

from dataclasses import dataclass, field
from datetime import datetime, timezone

import httpx
import structlog

from retry_utils import http_retry

logger = structlog.get_logger()


@dataclass
class RepoSummary:
    id: int
    name: str
    full_name: str
    private: bool
    archived: bool
    default_branch: str
    pushed_at: str | None
    open_issues_count: int
    language: str | None
    html_url: str


@dataclass
class CIStatus:
    state: str  # success/failure/pending/none
    updated_at: str | None = None
    workflow_name: str | None = None


@dataclass
class RepoSnapshot:
    repo_full_name: str
    snapshot_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    commits_30d: int = 0
    open_issues: int = 0
    open_prs: int = 0
    latest_release: str | None = None
    ci_status: str = "none"
    contributors_30d: int = 0
    pushed_at: datetime | None = None
    weekly_commits: list[int] = field(default_factory=list)


@dataclass
class MonitoredRepo:
    id: str
    user_id: str
    repo_full_name: str
    html_url: str
    is_private: bool = False
    linked_goal_path: str | None = None
    poll_tier: str = "moderate"
    last_polled_at: str | None = None
    added_at: str | None = None


class GitHubRepoClient:
    """Thin async wrapper around GitHub REST API (read-only)."""

    def __init__(
        self,
        token: str | None = None,
        base_url: str = "https://api.github.com",
        timeout: int = 15,
    ):
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "AI-Coach/1.0",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self._client = httpx.AsyncClient(base_url=base_url, headers=headers, timeout=timeout)
        self._rate_limit_remaining: int | None = None
        self._rate_limited = False

    def _update_rate_limit(self, response: httpx.Response) -> None:
        remaining = response.headers.get("X-RateLimit-Remaining")
        if remaining is not None:
            self._rate_limit_remaining = int(remaining)
            if self._rate_limit_remaining < 100:
                self._rate_limited = True
                logger.warning(
                    "github.rate_limit_low",
                    remaining=self._rate_limit_remaining,
                )

    @http_retry(exceptions=(httpx.ConnectError, httpx.RequestError))
    async def list_user_repos(self, username: str) -> list[RepoSummary]:
        """List user's owned repos sorted by push date."""
        repos: list[RepoSummary] = []
        page = 1
        while True:
            resp = await self._client.get(
                f"/users/{username}/repos",
                params={
                    "type": "owner",
                    "sort": "pushed",
                    "per_page": 100,
                    "page": page,
                },
            )
            self._update_rate_limit(resp)
            if resp.status_code == 404:
                return []
            if resp.status_code == 401:
                logger.warning("github.auth_failed_list_repos")
                return []
            if resp.status_code == 403:
                logger.warning("github.rate_limited_list_repos")
                return repos
            resp.raise_for_status()
            data = resp.json()
            if not data:
                break
            for r in data:
                repos.append(
                    RepoSummary(
                        id=r["id"],
                        name=r["name"],
                        full_name=r["full_name"],
                        private=r["private"],
                        archived=r.get("archived", False),
                        default_branch=r.get("default_branch", "main"),
                        pushed_at=r.get("pushed_at"),
                        open_issues_count=r.get("open_issues_count", 0),
                        language=r.get("language"),
                        html_url=r["html_url"],
                    )
                )
            if len(data) < 100:
                break
            page += 1
        return repos

    @http_retry(exceptions=(httpx.ConnectError, httpx.RequestError))
    async def get_commit_activity(self, owner: str, repo: str) -> list[int]:
        """Return last 12 weeks of commit counts from /stats/participation."""
        resp = await self._client.get(f"/repos/{owner}/{repo}/stats/participation")
        self._update_rate_limit(resp)
        if resp.status_code in (401, 403, 404):
            return []
        # 202 means stats are being computed — return empty
        if resp.status_code == 202:
            return []
        resp.raise_for_status()
        data = resp.json()
        # owner commits per week, last 52 weeks — take last 12
        all_weeks = data.get("all", [])
        return all_weeks[-12:] if len(all_weeks) >= 12 else all_weeks

    @http_retry(exceptions=(httpx.ConnectError, httpx.RequestError))
    async def get_ci_status(self, owner: str, repo: str, branch: str = "main") -> CIStatus:
        """Get latest CI run status for a branch."""
        resp = await self._client.get(
            f"/repos/{owner}/{repo}/actions/runs",
            params={"branch": branch, "per_page": 1},
        )
        self._update_rate_limit(resp)
        if resp.status_code in (401, 403, 404):
            return CIStatus(state="none")
        resp.raise_for_status()
        data = resp.json()
        runs = data.get("workflow_runs", [])
        if not runs:
            return CIStatus(state="none")
        run = runs[0]
        conclusion = run.get("conclusion") or "pending"
        state_map = {"success": "success", "failure": "failure"}
        return CIStatus(
            state=state_map.get(conclusion, "pending"),
            updated_at=run.get("updated_at"),
            workflow_name=run.get("name"),
        )

    async def get_repo_stats(self, owner: str, repo: str) -> RepoSnapshot | None:
        """Aggregate repo info + commit activity + CI into a snapshot."""
        # Get repo info
        resp = await self._client.get(f"/repos/{owner}/{repo}")
        self._update_rate_limit(resp)
        if resp.status_code == 404:
            return None
        if resp.status_code in (401, 403):
            logger.warning("github.auth_error_repo_stats", status=resp.status_code)
            return None
        resp.raise_for_status()
        info = resp.json()

        default_branch = info.get("default_branch", "main")

        # Get commit activity + CI status concurrently
        import asyncio

        weekly_commits, ci = await asyncio.gather(
            self.get_commit_activity(owner, repo),
            self.get_ci_status(owner, repo, default_branch),
            return_exceptions=True,
        )
        if isinstance(weekly_commits, Exception):
            weekly_commits = []
        if isinstance(ci, Exception):
            ci = CIStatus(state="none")

        # Compute commits in last 30 days (~4 weeks)
        commits_30d = sum(weekly_commits[-4:]) if weekly_commits else 0

        # Parse pushed_at
        pushed_at = None
        if info.get("pushed_at"):
            try:
                pushed_at = datetime.fromisoformat(info["pushed_at"].replace("Z", "+00:00"))
            except (ValueError, TypeError):
                pass

        # Get open PRs count (issues includes PRs on GitHub, so subtract)
        open_issues = info.get("open_issues_count", 0)

        # Get PR count separately
        open_prs = 0
        try:
            pr_resp = await self._client.get(
                f"/repos/{owner}/{repo}/pulls",
                params={"state": "open", "per_page": 1},
            )
            self._update_rate_limit(pr_resp)
            if pr_resp.status_code == 200:
                # Use link header to get total count if available
                link = pr_resp.headers.get("link", "")
                if 'rel="last"' in link:
                    import re

                    match = re.search(r"page=(\d+)>; rel=\"last\"", link)
                    if match:
                        open_prs = int(match.group(1))
                else:
                    open_prs = len(pr_resp.json())
        except Exception:
            pass

        # Adjust issues to not double-count PRs
        open_issues = max(0, open_issues - open_prs)

        return RepoSnapshot(
            repo_full_name=f"{owner}/{repo}",
            commits_30d=commits_30d,
            open_issues=open_issues,
            open_prs=open_prs,
            latest_release=info.get("latest_release"),
            ci_status=ci.state,
            contributors_30d=0,  # would need separate API call
            pushed_at=pushed_at,
            weekly_commits=weekly_commits,
        )

    async def close(self) -> None:
        await self._client.aclose()
