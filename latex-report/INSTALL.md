# Installation

## Files in this directory

| File | Purpose |
|---|---|
| `SKILL.md` | The `/latex-report` skill prompt |
| `check-git-commit.sh` | PostToolUse hook — auto-triggers the skill after git commits |
| `INSTALL.md` | This file |

## Deploy to a new machine

**1. Copy the skill directory:**
```bash
scp -r ~/.claude/skills/latex-report/ <user>@<host>:~/.claude/skills/latex-report/
chmod +x ~/.claude/skills/latex-report/check-git-commit.sh
```

**2. Add the hooks block to `~/.claude/settings.json` on the target machine:**
```json
"hooks": {
  "PostToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "~/.claude/skills/latex-report/check-git-commit.sh"
        }
      ]
    }
  ]
}
```

If `settings.json` already exists, merge the `hooks` block in — do not overwrite the whole file.
