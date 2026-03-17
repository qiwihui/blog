#!/usr/bin/env python3
"""Sync GitHub issues into mdBook markdown files.

- Reads all issues from a repo (paginated)
- Skips pull requests
- Skips issues labeled TODO (configurable)
- Writes files to src/blogs/qiwihui-blog-<issue_number>.md
- Rebuilds src/SUMMARY.md sorted by issue number (desc)
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Dict, Iterable, List

import requests

DEFAULT_REPO = "qiwihui/blog"
DEFAULT_OUTPUT_DIR = Path("src/blogs")
DEFAULT_SUMMARY_FILE = Path("src/SUMMARY.md")


def github_headers(token: str | None) -> Dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_all_issues(repo: str, token: str | None) -> List[Dict]:
    """Fetch all issues from GitHub (includes PRs from /issues endpoint)."""
    all_issues: List[Dict] = []
    page = 1
    per_page = 100

    while True:
        url = f"https://api.github.com/repos/{repo}/issues"
        resp = requests.get(
            url,
            params={
                "state": "all",
                "per_page": per_page,
                "page": page,
                "sort": "created",
                "direction": "asc",
            },
            headers=github_headers(token),
            timeout=30,
        )
        resp.raise_for_status()
        chunk = resp.json()
        if not chunk:
            break

        all_issues.extend(chunk)
        if len(chunk) < per_page:
            break
        page += 1

    return all_issues


def labels_of(issue: Dict) -> List[str]:
    return [l.get("name", "") for l in issue.get("labels", [])]


def issue_markdown(issue: Dict) -> str:
    title = issue.get("title", "")
    body = issue.get("body") or ""
    number = issue.get("number")
    issue_url = issue.get("html_url", "")
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


def write_summary(issues: Iterable[Dict], summary_file: Path, output_dir: Path) -> None:
    sorted_issues = sorted(issues, key=lambda x: x["number"], reverse=True)

    lines = ["# Summary", "", "[About Me](./README.md)"]
    for issue in sorted_issues:
        number = issue["number"]
        title = issue.get("title", "")
        lines.append(f"[{number}. {title}](./blogs/qiwihui-blog-{number}.md)")
    lines.append("")

    summary_file.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export all GitHub issues to mdBook src markdown files")
    parser.add_argument("--repo", default=os.getenv("GITHUB_REPOSITORY", DEFAULT_REPO), help="owner/repo")
    parser.add_argument("--token", default=os.getenv("GITHUB_TOKEN", ""), help="GitHub token")
    parser.add_argument("--skip-label", default="TODO", help="Label name to skip")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Output directory for markdown files")
    parser.add_argument("--summary-file", default=str(DEFAULT_SUMMARY_FILE), help="Path of SUMMARY.md")
    args = parser.parse_args()

    issues = fetch_all_issues(args.repo, args.token or None)

    filtered = [
        i
        for i in issues
        if "pull_request" not in i and args.skip_label not in labels_of(i)
    ]

    output_dir = Path(args.output_dir)
    summary_file = Path(args.summary_file)

    write_issue_files(filtered, output_dir)
    write_summary(filtered, summary_file, output_dir)

    print(f"Synced {len(filtered)} issues into {output_dir} and {summary_file}")


if __name__ == "__main__":
    main()
