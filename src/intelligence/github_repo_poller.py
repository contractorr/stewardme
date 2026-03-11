"""Scheduled polling of monitored GitHub repos."""

import asyncio
from datetime import datetime, timezone

import structlog

from .github_repo_store import GitHubRepoStore
from .github_repos import GitHubRepoClient, MonitoredRepo, RepoSnapshot

logger = structlog.get_logger()


class GitHubRepoPoller:
    """Polls monitored repos and saves health snapshots."""

    def __init__(self, client: GitHubRepoClient, store: GitHubRepoStore):
        self.client = client
        self.store = store

    async def poll_user_repos(self, user_id: str) -> list[RepoSnapshot]:
        """Poll all repos due for this user. Returns new snapshots."""
        repos = self.store.get_repos_due_for_poll(user_id)
        if not repos:
            return []

        logger.info("github_poll.start", user_id=user_id, repo_count=len(repos))
        snapshots = await asyncio.gather(
            *[self._poll_one(repo) for repo in repos],
            return_exceptions=True,
        )

        results = []
        for i, s in enumerate(snapshots):
            if isinstance(s, RepoSnapshot):
                results.append(s)
            elif isinstance(s, Exception):
                repo = repos[i]
                # Rate limit → stop polling remaining repos for this user
                if "403" in str(s) or "rate" in str(s).lower():
                    logger.warning(
                        "github_poll.rate_limited",
                        user_id=user_id,
                        repo=repo.repo_full_name,
                    )
                    break
                logger.warning(
                    "github_poll.repo_failed",
                    user_id=user_id,
                    repo=repo.repo_full_name,
                    error=str(s),
                )
        return results

    async def _poll_one(self, repo: MonitoredRepo) -> RepoSnapshot:
        parts = repo.repo_full_name.split("/", 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid repo name: {repo.repo_full_name}")
        owner, name = parts

        snapshot = await self.client.get_repo_stats(owner, name)
        if snapshot is None:
            raise ValueError(f"Repo not found: {repo.repo_full_name}")

        self.store.save_snapshot(repo.id, snapshot)
        new_tier = self._compute_tier(snapshot)
        if new_tier != repo.poll_tier:
            self.store.update_poll_tier(repo.id, new_tier)
            logger.info(
                "github_poll.tier_changed",
                repo=repo.repo_full_name,
                old_tier=repo.poll_tier,
                new_tier=new_tier,
            )
        return snapshot

    @staticmethod
    def _compute_tier(snapshot: RepoSnapshot) -> str:
        """Assign poll tier based on pushed_at recency."""
        if not snapshot.pushed_at:
            return "stale"
        now = datetime.now(timezone.utc)
        if snapshot.pushed_at.tzinfo is None:
            age = datetime.now() - snapshot.pushed_at
        else:
            age = now - snapshot.pushed_at
        if age.days <= 7:
            return "active"
        if age.days <= 30:
            return "moderate"
        return "stale"
