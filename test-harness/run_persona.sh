#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
PERSONA="$1"
STATE_DIR="$SCRIPT_DIR/state/$PERSONA"
SCREENSHOTS_DIR="$STATE_DIR/screenshots"
SESSION_LOG="$STATE_DIR/session_log.md"
PERSONA_FILE="$SCRIPT_DIR/personas/${PERSONA}.md"
EVAL_FILE="$SCRIPT_DIR/eval_criteria.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

# Ensure state dirs exist
mkdir -p "$SCREENSHOTS_DIR"

# Initialize session log if first run
if [ ! -f "$SESSION_LOG" ]; then
  echo "# Session Log: ${PERSONA}" > "$SESSION_LOG"
  echo "" >> "$SESSION_LOG"
  echo "Started: ${TIMESTAMP}" >> "$SESSION_LOG"
  echo "" >> "$SESSION_LOG"
fi

# Build the prompt
PERSONA_CONTENT=$(cat "$PERSONA_FILE")
EVAL_CONTENT=$(cat "$EVAL_FILE")
SESSION_CONTENT=$(cat "$SESSION_LOG")

_prompt_tmp=$(mktemp)
cat > "$_prompt_tmp" <<PROMPT_EOF
You are testing a web app (StewardMe) by role-playing as a persona. Your job is to interact with the app naturally, then evaluate the experience.

## Your Persona
${PERSONA_CONTENT}

## Evaluation Criteria
${EVAL_CONTENT}

## Previous Sessions
${SESSION_CONTENT}

## Today's Task

1. **Navigate** to http://localhost:3000/login using the Playwright browser
2. **Log in** using the test credentials from the persona (select the username from the dropdown, type the password, click sign in)
3. **Check the current state** — read previous session log to know which arc beat to do next. If no previous sessions, start at beat 1.
4. **Interact as the persona:**
   - Write a journal entry (in character) relevant to the current arc beat
   - Ask the advisor a question relevant to the arc beat
   - Browse the intel page and note what's shown
5. **Take screenshots** at key moments:
   - After login (dashboard)
   - The journal entry you wrote
   - The advisor's response
   - The intel page
   - Save them to: ${SCREENSHOTS_DIR}/
6. **Check for errors:**
   - Get console logs and errors from browser-tools
   - Note any network errors
   - Note any UI glitches or broken layouts
7. **Evaluate** against the criteria above
8. **Append your findings** to ${SESSION_LOG} in this format:

---
## Session: ${TIMESTAMP}
### Arc Beat: [number and description]
### What I Did
[Brief description of interactions]
### Evaluation
[Rate each criteria category 1-5, note specifics]
### Bugs / Issues
[List any problems found]
### UX Notes
[Any UX observations or improvement suggestions]
### Advisor Quality
[How relevant/helpful was the advisor's response? Did it reference past context?]
---

Important:
- Stay in character when writing journal entries and asking questions
- Be thorough but concise in your evaluation
- Screenshot any bugs or visual issues
- If something is broken, note it and try to continue testing other areas
PROMPT_EOF
PROMPT=$(<"$_prompt_tmp")
rm -f "$_prompt_tmp"

echo "Starting ${PERSONA} session at ${TIMESTAMP}..."

# Run Claude Code with the assembled prompt
# --allowedTools scopes to Playwright, browser-tools, and file operations
cd "$REPO_DIR"
claude -p "$PROMPT" \
  --allowedTools "mcp__playwright__*,mcp__browser-tools__*,Read,Write,Edit,Bash(read-only commands like curl or ls)" \
  2>&1 | tee "$STATE_DIR/latest_run_output.txt"

echo "Session complete. Results in ${STATE_DIR}/"
