"""GitHub repo monitoring routes."""

import re

import structlog
from fastapi import APIRouter, Depends, HTTPException, status

from web.auth import get_current_user
from web.deps import get_github_repo_store, get_secret_key
from web.models import (
    LinkGoalRequest,
    MonitoredRepoResponse,
    MonitorRepoRequest,
    RepoSnapshotResponse,
    RepoSummaryResponse,
)
from web.user_store import get_user_secret

logger = structlog.get_logger()

router = APIRouter(prefix="/api/github/repos", tags=["github"])

_REPO_NAME_RE = re.compile(r"^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$")


def _resolve_github_token(user_id: str) -> str | None:
    """Try github_pat first, fall back to github_token."""
    try:
        fernet_key = get_secret_key()
        token = get_user_secret(user_id, "github_pat", fernet_key)
        if token:
            return token
        return get_user_secret(user_id, "github_token", fernet_key)
    except Exception:
        return None


def _snapshot_to_response(snapshot) -> RepoSnapshotResponse | None:
    if not snapshot:
        return None
    return RepoSnapshotResponse(
        commits_30d=snapshot.commits_30d,
        open_issues=snapshot.open_issues,
        open_prs=snapshot.open_prs,
        latest_release=snapshot.latest_release,
        ci_status=snapshot.ci_status,
        contributors_30d=snapshot.contributors_30d,
        pushed_at=snapshot.pushed_at.isoformat() if snapshot.pushed_at else None,
        weekly_commits=snapshot.weekly_commits,
        snapshot_at=snapshot.snapshot_at.isoformat() if snapshot.snapshot_at else None,
    )


def _repo_to_response(repo, store) -> MonitoredRepoResponse:
    snapshot = store.get_latest_snapshot(repo.id)
    return MonitoredRepoResponse(
        id=repo.id,
        repo_full_name=repo.repo_full_name,
        html_url=repo.html_url,
        is_private=repo.is_private,
        linked_goal_path=repo.linked_goal_path,
        poll_tier=repo.poll_tier,
        last_polled_at=repo.last_polled_at,
        added_at=repo.added_at or "",
        latest_snapshot=_snapshot_to_response(snapshot),
    )


@router.get("", response_model=list[RepoSummaryResponse])
async def list_user_repos(user: dict = Depends(get_current_user)):
    """Discover user's GitHub repos."""
    from profile.storage import ProfileStorage

    from web.deps import get_profile_path

    profile_path = get_profile_path(user["id"])
    ps = ProfileStorage(profile_path)
    profile = ps.load()
    username = profile.github_username if profile else None

    if not username:
        raise HTTPException(
            status_code=400,
            detail="GitHub username not set. Update it in Settings or Profile.",
        )

    token = _resolve_github_token(user["id"])

    from intelligence.github_repos import GitHubRepoClient

    client = GitHubRepoClient(token=token)
    try:
        repos = await client.list_user_repos(username)
    finally:
        await client.close()

    return [
        RepoSummaryResponse(
            name=r.name,
            full_name=r.full_name,
            private=r.private,
            html_url=r.html_url,
            language=r.language,
            pushed_at=r.pushed_at,
            open_issues_count=r.open_issues_count,
        )
        for r in repos
        if not r.archived
    ]


@router.post("/monitor", status_code=status.HTTP_201_CREATED, response_model=MonitoredRepoResponse)
async def monitor_repo(
    body: MonitorRepoRequest,
    user: dict = Depends(get_current_user),
):
    """Add a repo to monitoring."""
    if not _REPO_NAME_RE.match(body.repo_full_name):
        raise HTTPException(status_code=400, detail="Invalid repo name format")

    store = get_github_repo_store()
    html_url = body.html_url or f"https://github.com/{body.repo_full_name}"
    try:
        repo_id = store.add_repo(
            user_id=user["id"],
            repo_full_name=body.repo_full_name,
            html_url=html_url,
            is_private=body.is_private,
        )
    except ValueError:
        raise HTTPException(status_code=409, detail="Repo already monitored")

    repo = store.get_repo(user["id"], repo_id)
    return _repo_to_response(repo, store)


@router.delete("/monitor/{repo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unmonitor_repo(repo_id: str, user: dict = Depends(get_current_user)):
    """Remove a repo from monitoring."""
    store = get_github_repo_store()
    if not store.remove_repo(user["id"], repo_id):
        raise HTTPException(status_code=404, detail="Repo not found")


@router.get("/monitored", response_model=list[MonitoredRepoResponse])
async def list_monitored(user: dict = Depends(get_current_user)):
    """List monitored repos with latest snapshots."""
    store = get_github_repo_store()
    repos = store.list_repos(user["id"])
    return [_repo_to_response(r, store) for r in repos]


@router.patch("/monitor/{repo_id}/link", response_model=MonitoredRepoResponse)
async def link_goal(
    repo_id: str,
    body: LinkGoalRequest,
    user: dict = Depends(get_current_user),
):
    """Link a monitored repo to a goal."""
    store = get_github_repo_store()
    repo = store.get_repo(user["id"], repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repo not found")
    store.link_goal(repo_id, body.goal_path)
    repo = store.get_repo(user["id"], repo_id)
    return _repo_to_response(repo, store)


@router.patch("/monitor/{repo_id}/unlink", response_model=MonitoredRepoResponse)
async def unlink_goal(repo_id: str, user: dict = Depends(get_current_user)):
    """Unlink a goal from a monitored repo."""
    store = get_github_repo_store()
    repo = store.get_repo(user["id"], repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repo not found")
    store.unlink_goal(repo_id)
    repo = store.get_repo(user["id"], repo_id)
    return _repo_to_response(repo, store)


@router.post("/monitor/{repo_id}/refresh", response_model=RepoSnapshotResponse)
async def refresh_repo(repo_id: str, user: dict = Depends(get_current_user)):
    """Trigger immediate poll for a single repo."""
    store = get_github_repo_store()
    repo = store.get_repo(user["id"], repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repo not found")

    token = _resolve_github_token(user["id"])

    from intelligence.github_repo_poller import GitHubRepoPoller
    from intelligence.github_repos import GitHubRepoClient

    client = GitHubRepoClient(token=token)
    poller = GitHubRepoPoller(client, store)
    try:
        snapshot = await poller._poll_one(repo)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Poll failed: {e}")
    finally:
        await client.close()

    return _snapshot_to_response(snapshot)
