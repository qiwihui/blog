#!/usr/bin/env python3
"""Sync GitHub issues into mdBook markdown files.

- Reads all issues from a repo via `gh issue list` (excludes PRs automatically)
- Skips issues labeled TODO (configurable)
- Writes files to src/blogs/qiwihui-blog-<issue_number>.md
- Rebuilds src/SUMMARY.md sorted by issue number (desc)
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Iterable, List

DEFAULT_REPO = "qiwihui/blog"
DEFAULT_OUTPUT_DIR = Path("src/blogs")
DEFAULT_SUMMARY_FILE = Path("src/SUMMARY.md")


def fetch_all_issues(repo: str, token: str | None) -> List[Dict]:
    """Fetch all issues (not PRs) via gh CLI, which handles auth and pagination."""
    env = os.environ.copy()
    if token:
        env["GH_TOKEN"] = token

    cmd = [
        "gh", "issue", "list",
        "--repo", repo,
        "--state", "all",
        "--json", "number,title,body,labels,state,url",
        "--limit", "10000",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        raise RuntimeError(
            f"gh issue list failed (exit {result.returncode}):\n{result.stderr.strip()}"
        )

    issues = json.loads(result.stdout)
    print(f"Fetched {len(issues)} issues from {repo}")
    return issues


def labels_of(issue: Dict) -> List[str]:
    return [l.get("name", "") for l in issue.get("labels", [])]


def issue_markdown(issue: Dict) -> str:
    title = issue.get("title", "")
    body = issue.get("body") or ""
    number = issue.get("number")
    issue_url = issue.get("url") or issue.get("html_url", "")
    state = issue.get("state", "unknown")

    return (
        f"# {title}\n\n"
        f"> Issue: #{number}  \n"
        f"> State: {state}  \n"
        f"> Source: [{issue_url}]({issue_url})\n\n"
        f"{body}\n"
    )


def write_issue_files(issues: Iterable[Dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for issue in issues:
        number = issue["number"]
        file_path = output_dir / f"qiwihui-blog-{number}.md"
        file_path.write_text(issue_markdown(issue), encoding="utf-8")


def write_summary(issues: Iterable[Dict], summary_file: Path) -> None:
    sorted_issues = sorted(issues, key=lambda x: x["number"], reverse=True)

    lines = ["# Summary", "", "[About Me](./README.md)"]
    for issue in sorted_issues:
        number = issue["number"]
        title = issue.get("title", "")
        lines.append(f"[{number}. {title}](./blogs/qiwihui-blog-{number}.md)")
    lines.append("")

    summary_file.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export all GitHub issues to mdBook src markdown files"
    )
    parser.add_argument(
        "--repo",
        default=os.getenv("GITHUB_REPOSITORY", DEFAULT_REPO),
        help="owner/repo",
    )
    parser.add_argument(
        "--token", default=os.getenv("GITHUB_TOKEN", ""), help="GitHub token"
    )
    parser.add_argument("--skip-label", default="TODO", help="Label name to skip")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Output directory for markdown files",
    )
    parser.add_argument(
        "--summary-file",
        default=str(DEFAULT_SUMMARY_FILE),
        help="Path of SUMMARY.md",
    )
    args = parser.parse_args()

    issues = fetch_all_issues(args.repo, args.token or None)

    filtered = [i for i in issues if args.skip_label not in labels_of(i)]

    if not filtered:
        print(
            f"ERROR: fetched {len(issues)} issues but 0 passed the filter "
            f"(skip_label={args.skip_label!r}). Refusing to overwrite {args.summary_file}.",
            file=sys.stderr,
        )
        sys.exit(1)

    output_dir = Path(args.output_dir)
    summary_file = Path(args.summary_file)

    write_issue_files(filtered, output_dir)
    write_summary(filtered, summary_file)

    print(f"Synced {len(filtered)} issues into {output_dir} and {summary_file}")


if __name__ == "__main__":
    main()
