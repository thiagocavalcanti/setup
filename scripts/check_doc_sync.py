#!/usr/bin/env python3
"""
check_doc_sync.py: Evaluates staged or modified files against tracked_docs.json match patterns.
Identifies stale documentation topics requiring updates and topic version bumps before commit.
"""

import sys
import os
import json
import fnmatch
import subprocess
from pathlib import Path

# Terminal Colors
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"

def get_git_changed_files():
    # Staged files first
    res = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True)
    files = [f.strip() for f in res.stdout.splitlines() if f.strip()]
    if not files:
        # Fallback to unstaged modified files
        res = subprocess.run(["git", "diff", "--name-only"], capture_output=True, text=True)
        files = [f.strip() for f in res.stdout.splitlines() if f.strip()]
    return files

def main():
    repo_dir = Path(__file__).parent.parent.resolve()
    manifest_path = repo_dir / ".agents" / "skills" / "doc-auto-sync" / "tracked_docs.json"

    if not manifest_path.exists():
        print(f"{Colors.YELLOW}⚠ Manifest file not found at {manifest_path}{Colors.RESET}")
        sys.exit(0)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    changed_files = get_git_changed_files()

    if not changed_files:
        print(f"{Colors.GREEN}✔ No changed files detected in git working tree.{Colors.RESET}")
        sys.exit(0)

    print(f"\n{Colors.BOLD}{Colors.CYAN}Checking documentation sync for {len(changed_files)} changed file(s)...{Colors.RESET}\n")

    stale_topics = []

    for file_entry in manifest.get("tracked_files", []):
        doc_path = file_entry.get("path")
        for topic in file_entry.get("topics", []):
            topic_id = topic.get("id")
            topic_name = topic.get("name")
            version = topic.get("version")
            patterns = topic.get("match_patterns", [])

            is_match = False
            for changed in changed_files:
                for pat in patterns:
                    if fnmatch.fnmatch(changed, pat) or pat in changed:
                        is_match = True
                        break
                if is_match:
                    break

            if is_match:
                stale_topics.append({
                    "doc_path": doc_path,
                    "topic_id": topic_id,
                    "topic_name": topic_name,
                    "version": version,
                    "description": topic.get("description")
                })

    if stale_topics:
        print(f"{Colors.BOLD}{Colors.YELLOW}⚠ Stale Documentation Topics Detected ({len(stale_topics)}):{Colors.RESET}")
        for t in stale_topics:
            print(f"  • {Colors.BOLD}[{t['doc_path']}]{Colors.RESET} {Colors.CYAN}{t['topic_name']}{Colors.RESET} (Topic ID: {t['topic_id']} | Version: v{t['version']})")
            print(f"    {Colors.DIM}Description: {t['description']}{Colors.RESET}")
        print(f"\n{Colors.MAGENTA}Action Required:{Colors.RESET} Update the relevant sections in {set(t['doc_path'] for t in stale_topics)} and bump topic version in tracked_docs.json before commit.\n")
    else:
        print(f"{Colors.GREEN}✔ Documentation is up to date for all staged changes. (Tokens saved!){Colors.RESET}\n")

if __name__ == "__main__":
    main()
