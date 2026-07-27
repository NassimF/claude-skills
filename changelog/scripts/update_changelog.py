#!/usr/bin/env python3
"""Update CHANGELOG.md with git commits not yet listed."""

import subprocess
import sys
from pathlib import Path
from collections import defaultdict


def get_git_commits():
    """Return list of (date, hash, subject) for all non-merge commits."""
    result = subprocess.run(
        ["git", "log", "--no-merges", "--pretty=format:%ad|%h|%s", "--date=short"],
        capture_output=True, text=True, check=True
    )
    commits = []
    for line in result.stdout.strip().splitlines():
        if not line:
            continue
        date, hash_, subject = line.split("|", 2)
        commits.append((date, hash_, subject))
    return commits


def get_listed_hashes(changelog_path: Path) -> set[str]:
    """Extract all short hashes already listed in the changelog."""
    if not changelog_path.exists():
        return set()
    hashes = set()
    for line in changelog_path.read_text().splitlines():
        # lines look like: - some message (abc1234)
        if line.startswith("- ") and line.endswith(")") and "(" in line:
            hash_ = line.rsplit("(", 1)[-1].rstrip(")")
            if len(hash_) == 7 and all(c in "0123456789abcdef" for c in hash_):
                hashes.add(hash_)
    return hashes


def build_new_entries(commits, listed_hashes):
    """Group new commits by date, newest date first."""
    by_date = defaultdict(list)
    for date, hash_, subject in commits:
        if hash_ not in listed_hashes:
            by_date[date].append((hash_, subject))
    return dict(sorted(by_date.items(), reverse=True))


def main():
    changelog_path = Path("CHANGELOG.md")
    existing = changelog_path.read_text() if changelog_path.exists() else ""

    commits = get_git_commits()
    listed = get_listed_hashes(changelog_path)
    new_entries = build_new_entries(commits, listed)

    if not new_entries:
        print("CHANGELOG.md is already up to date.")
        return

    new_sections = []
    for date, items in new_entries.items():
        lines = [f"## {date}", ""]
        for hash_, subject in items:
            lines.append(f"- {subject} ({hash_})")
        lines.append("")
        new_sections.append("\n".join(lines))

    header = "# Changelog\n\n"
    body = existing.lstrip()
    if body.startswith("# Changelog"):
        body = body[len("# Changelog"):].lstrip("\n")

    updated = header + "\n".join(new_sections) + (("\n" + body) if body else "")
    changelog_path.write_text(updated)

    total = sum(len(v) for v in new_entries.values())
    dates = ", ".join(new_entries.keys())
    print(f"Added {total} commit(s) across {len(new_entries)} date(s): {dates}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"git error: {e}", file=sys.stderr)
        sys.exit(1)
