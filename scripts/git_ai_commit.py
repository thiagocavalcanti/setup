#!/usr/bin/env python3
"""
git-ai-commit: Token-optimized Git diff generator for AI commit message drafting.
"""

import sys
import subprocess
import argparse
from pathlib import Path

# Common patterns to exclude from LLM diff prompts to save tokens
IGNORE_PATTERNS = [
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "Cargo.lock",
    "go.sum",
    "composer.lock",
    "Pipfile.lock",
    "poetry.lock",
    "*.min.js",
    "*.min.css",
    "*.map",
    "*.svg",
    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.ico",
]

MAX_DIFF_LINES = 150

def run_git_cmd(args):
    try:
        res = subprocess.run(["git"] + args, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def get_compact_diff():
    # Construct git exclude pathspecs
    exclude_pathspecs = [f":!{pattern}" for pattern in IGNORE_PATTERNS]
    
    # 1. Get staged status
    staged_status = run_git_cmd(["diff", "--cached", "--name-status"] + ["--"] + exclude_pathspecs)
    if not staged_status:
        return "No relevant staged changes found (lockfiles and binaries ignored)."

    # 2. Get stat summary
    stat_summary = run_git_cmd(["diff", "--cached", "--stat"] + ["--"] + exclude_pathspecs)

    # 3. Get compact diff patch with line cap
    raw_diff = run_git_cmd(["diff", "--cached", "-U2"] + ["--"] + exclude_pathspecs)
    
    diff_lines = raw_diff.splitlines() if raw_diff else []
    truncated = False
    if len(diff_lines) > MAX_DIFF_LINES:
        diff_lines = diff_lines[:MAX_DIFF_LINES]
        truncated = True

    diff_body = "\n".join(diff_lines)
    if truncated:
        diff_body += f"\n... (diff truncated to first {MAX_DIFF_LINES} lines to save tokens)"

    prompt = (
        "Draft a single-line Conventional Commit message (e.g. feat:, fix:, refactor:, docs:) "
        "for the following staged changes:\n\n"
        f"### Staged Files:\n{staged_status}\n\n"
        f"### Summary:\n{stat_summary}\n\n"
        f"### Compact Diff:\n```diff\n{diff_body}\n```"
    )
    return prompt

def main():
    parser = argparse.ArgumentParser(description="Token-optimized Git AI commit tool.")
    parser.add_argument("-m", "--message", help="Commit message to execute git commit with.")
    args = parser.parse_args()

    if args.message:
        subprocess.run(["git", "commit", "-m", args.message])
    else:
        print(get_compact_diff())

if __name__ == "__main__":
    main()
