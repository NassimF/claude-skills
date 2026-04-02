#!/usr/bin/env bash
# check-git-commit.sh
# PostToolUse hook for Claude Code.
# Reads JSON from stdin describing a Bash tool call.
# If the command was a `git commit` (but NOT a latex-report-update commit),
# outputs a message that Claude Code injects into the conversation,
# prompting Claude to run /latex-report.

set -euo pipefail

# Read stdin into a variable
INPUT=$(cat)

# Extract the command field from the JSON using python3 (available on macOS by default)
COMMAND=$(python3 -c "
import sys, json
try:
    data = json.loads(sys.stdin.read())
    # Handle both direct tool_input and nested structures
    cmd = data.get('tool_input', {}).get('command', '') or data.get('command', '')
    print(cmd)
except Exception:
    print('')
" <<< "$INPUT")

# Check if this was a git commit command
if echo "$COMMAND" | grep -qE '^\s*git\s+(.*\s+)?commit\b'; then
    # Exclude latex-report-update commits to prevent infinite loops
    if echo "$COMMAND" | grep -q 'latex-report-update'; then
        exit 0
    fi
    # Also exclude --amend of report commits (check recent commit message)
    LAST_MSG=$(git log -1 --format="%s" 2>/dev/null || echo "")
    if echo "$LAST_MSG" | grep -q 'latex-report-update'; then
        exit 0
    fi
    # Output the trigger message — Claude Code injects this into the conversation
    echo "[HOOK] Git commit detected. Per your project setup, please invoke /latex-report to update the changelog report with the changes from this commit."
fi

exit 0
