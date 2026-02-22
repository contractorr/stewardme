"""Onboarding chat — LLM-driven profile interview + goal creation."""

import json
import re

import structlog
from fastapi import APIRouter, Depends, HTTPException

from advisor.goals import get_goal_defaults
from journal.storage import JournalStorage
from llm import create_llm_provider
from web.auth import get_current_user
from web.deps import get_api_key_for_user, get_config, get_user_paths
from web.models import OnboardingChat, OnboardingResponse

logger = structlog.get_logger()

router = APIRouter(prefix="/api/onboarding", tags=["onboarding"])

# In-memory sessions keyed by user_id
_sessions: dict[str, dict] = {}

MAX_TURNS = 15

ONBOARDING_SYSTEM = """You are a friendly career coach onboarding a new user. Ask one clear question at a time.
Your job is to gather enough information to build their professional profile AND identify initial goals.

You need to learn:
1. Current role and career stage (junior/mid/senior/lead/exec)
2. Technical skills and proficiency levels (1-5 scale)
3. Programming languages and frameworks used
4. Professional interests and passions
5. Career aspirations and goals
6. Location (city/country)
7. Preferred learning style (visual/reading/hands-on/mixed)
8. Weekly hours available for professional development
9. 1-3 concrete goals they want to track (e.g. "learn Rust", "get promoted", "publish a paper")
10. Current challenges or concerns they're facing
11. What they hope to get from this app

Adapt your questions based on previous answers. Be conversational but efficient.
Group related questions when natural (e.g. role + career stage).
After gathering enough info (5-8 questions), output EXACTLY this JSON block:

```json
{"done": true, "profile": {
  "current_role": "...",
  "career_stage": "junior|mid|senior|lead|exec",
  "skills": [{"name": "...", "proficiency": 1-5}, ...],
  "languages_frameworks": ["python", "react", ...],
  "interests": ["...", ...],
  "aspirations": "...",
  "location": "...",
  "learning_style": "visual|reading|hands-on|mixed",
  "weekly_hours_available": N
}, "goals": [
  {"title": "Short goal title", "description": "Brief description of what they want to achieve"},
  ...
]}
```

Before the JSON block, include a brief friendly wrap-up message summarizing what you learned."""

ONBOARDING_START = """Start the onboarding interview. Greet the user warmly, briefly explain you'll ask a few questions
to personalize their experience, then ask your first question. Be concise."""


def _extract_completion_json(text: str) -> dict | None:
    """Extract completion JSON with profile + goals from LLM response."""
    # Try ```json block first
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(1))
            if data.get("done") and "profile" in data:
                return data
        except json.JSONDecodeError:
            pass

    # Try bare JSON
    match = re.search(r'\{"done"\s*:\s*true.*?"profile"\s*:\s*\{.*\}.*\}', text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(0))
            if "profile" in data:
                return data
        except json.JSONDecodeError:
            pass

    return None


def _make_llm_caller(user_id: str):
    """Build LLM caller for a user (same pattern as advisor route)."""
    config = get_config()
    api_key = get_api_key_for_user(user_id, config.llm.provider)
    if not api_key:
        raise HTTPException(status_code=400, detail="No LLM API key configured")

    secrets_provider = None
    try:
        from web.deps import get_decrypted_secrets_for_user

        secrets = get_decrypted_secrets_for_user(user_id)
        secrets_provider = secrets.get("llm_provider")
    except Exception:
        pass

    provider = secrets_provider or config.llm.provider
    model = config.llm.model
    llm = create_llm_provider(provider=provider, api_key=api_key, model=model)

    def caller(system: str, prompt: str, max_tokens: int = 1500) -> str:
        return llm.generate(
            messages=[{"role": "user", "content": prompt}],
            system=system,
            max_tokens=max_tokens,
        )

    return caller


def _save_results(user_id: str, data: dict) -> int:
    """Save profile and create goals. Returns number of goals created."""
    paths = get_user_paths(user_id)

    # Save profile
    from profile.interview import _build_profile
    from profile.storage import ProfileStorage

    profile = _build_profile(data.get("profile", {}))
    storage = ProfileStorage(paths["profile"])
    storage.save(profile)
    logger.info("onboarding.profile_saved", user_id=user_id, skills=len(profile.skills))

    # Create goals
    goals = data.get("goals", [])
    goals_created = 0
    if goals:
        journal_storage = JournalStorage(paths["journal_dir"])
        for g in goals:
            if isinstance(g, dict) and g.get("title"):
                try:
                    journal_storage.create(
                        content=g.get("description", ""),
                        entry_type="goal",
                        title=g["title"],
                        metadata=get_goal_defaults(),
                    )
                    goals_created += 1
                except Exception as e:
                    logger.warning("onboarding.goal_create_failed", title=g["title"], error=str(e))

    logger.info("onboarding.goals_created", user_id=user_id, count=goals_created)
    return goals_created


def _strip_json_block(text: str) -> str:
    """Remove JSON block from response text to get just the conversational part."""
    # Remove ```json...``` blocks
    cleaned = re.sub(r"```json\s*\{.*?\}\s*```", "", text, flags=re.DOTALL)
    # Remove bare {"done": true...} blocks
    cleaned = re.sub(r'\{"done"\s*:\s*true.*\}', "", cleaned, flags=re.DOTALL)
    return cleaned.strip()


@router.post("/start", response_model=OnboardingResponse)
async def start_onboarding(user: dict = Depends(get_current_user)):
    user_id = user["id"]

    try:
        caller = _make_llm_caller(user_id)
        response = caller(ONBOARDING_SYSTEM, ONBOARDING_START)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("onboarding.start_failed", user_id=user_id, error=str(e))
        raise HTTPException(status_code=502, detail=f"LLM call failed: {e}")

    _sessions[user_id] = {
        "messages": [("assistant", response)],
        "caller": caller,
        "turns": 0,
    }

    return OnboardingResponse(message=response, done=False)


@router.post("/chat", response_model=OnboardingResponse)
async def chat_onboarding(
    body: OnboardingChat,
    user: dict = Depends(get_current_user),
):
    user_id = user["id"]
    session = _sessions.get(user_id)
    if not session:
        raise HTTPException(
            status_code=400, detail="No active onboarding session — call /start first"
        )

    session["messages"].append(("user", body.message))
    session["turns"] += 1

    # Build conversation history
    history = "\n".join(
        f"{'Coach' if role == 'assistant' else 'User'}: {msg}" for role, msg in session["messages"]
    )

    force = session["turns"] >= MAX_TURNS
    if force:
        prompt = f"""Based on this interview, generate the profile and goals JSON now.

{history}

Output the JSON block now with whatever information you have."""
    else:
        prompt = f"Interview so far:\n{history}\n\nContinue the interview or finalize if you have enough info."

    caller = session["caller"]
    try:
        response = caller(ONBOARDING_SYSTEM, prompt, max_tokens=2000)
    except Exception as e:
        logger.error("onboarding.chat_failed", user_id=user_id, error=str(e))
        raise HTTPException(status_code=502, detail=f"LLM call failed: {e}")

    # Check for completion JSON
    completion = _extract_completion_json(response)
    if completion:
        goals_created = _save_results(user_id, completion)
        _sessions.pop(user_id, None)
        clean_msg = _strip_json_block(response)
        if not clean_msg:
            clean_msg = "Great, I've got everything I need! Your profile is set up."
        return OnboardingResponse(message=clean_msg, done=True, goals_created=goals_created)

    session["messages"].append(("assistant", response))

    # Force extraction if we hit max turns and LLM didn't include JSON
    if force:
        force_prompt = f"""{history}

Coach: {response}

Now output ONLY the JSON block with profile and goals based on everything discussed."""
        force_response = caller(ONBOARDING_SYSTEM, force_prompt, max_tokens=2000)
        completion = _extract_completion_json(force_response)
        goals_created = 0
        if completion:
            goals_created = _save_results(user_id, completion)
        _sessions.pop(user_id, None)
        return OnboardingResponse(message=response, done=True, goals_created=goals_created)

    return OnboardingResponse(message=response, done=False)
