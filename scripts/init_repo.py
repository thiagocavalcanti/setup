#!/usr/bin/env python3
"""
init_repo.py: Configures a repository by ensuring AGENTS.md and CLAUDE.md are linked,
and installs essential agent skills (skill-creator, gh-axi, chrome-devtools-axi) using `npx skills`.
"""

import sys
import os
import shutil
import subprocess
import argparse
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

def print_info(msg):
    print(f"  {Colors.BLUE}➔{Colors.RESET} {msg}")

def print_success(msg):
    print(f"  {Colors.GREEN}✔{Colors.RESET} {Colors.DIM}{msg}{Colors.RESET}")

def print_warn(msg):
    print(f"  {Colors.YELLOW}⚠{Colors.RESET} {msg}")

def print_error(msg):
    print(f"  {Colors.RED}✖{Colors.RESET} {msg}")

def init_repository(target_path):
    repo_dir = Path(target_path).resolve()
    print(f"\n{Colors.BOLD}{Colors.CYAN}Initializing repository at:{Colors.RESET} {repo_dir}\n")

    if not repo_dir.exists():
        repo_dir.mkdir(parents=True, exist_ok=True)
        print_info(f"Created repository directory: {repo_dir}")

    agents_md = repo_dir / "AGENTS.md"
    claude_md = repo_dir / "CLAUDE.md"

    has_agents = agents_md.exists() or agents_md.is_symlink()
    has_claude = claude_md.exists() or claude_md.is_symlink()

    # 1. Handle Memory Files & Symlinks
    if has_agents and not has_claude:
        print_info("Found existing AGENTS.md.")
        claude_md.symlink_to(Path("AGENTS.md"))
        print_success("Created symlink: CLAUDE.md -> AGENTS.md")
    elif has_claude and not has_agents:
        print_info("Found existing CLAUDE.md.")
        agents_md.symlink_to(Path("CLAUDE.md"))
        print_success("Created symlink: AGENTS.md -> CLAUDE.md")
    elif not has_agents and not has_claude:
        print_info("No AGENTS.md or CLAUDE.md found.")
        agents_md.write_text("", encoding="utf-8")
        print_success("Created base AGENTS.md file.")
        claude_md.symlink_to(Path("AGENTS.md"))
        print_success("Created symlink: CLAUDE.md -> AGENTS.md")
    else:
        print_info("Both AGENTS.md and CLAUDE.md already exist.")

    # 2. Install Skills via npx skills
    skills_to_install = [
        ("anthropics/skills", "skill-creator", "skill-creator"),
        ("kunchenguid/gh-axi", None, "gh-axi (GitHub Extension)"),
        ("kunchenguid/chrome-devtools-axi", None, "chrome-devtools-axi (Chrome DevTools Extension)")
    ]

    print_info("Installing agent skills via `npx skills`...")
    npx_bin = shutil.which("npx")
    if npx_bin:
        for pkg, skill_name, label in skills_to_install:
            cmd = [npx_bin, "-y", "skills", "add", pkg, "-y"]
            if skill_name:
                cmd.extend(["--skill", skill_name])
            try:
                res = subprocess.run(cmd, cwd=str(repo_dir), capture_output=True, text=True)
                if res.returncode == 0:
                    print_success(f"Installed '{label}' via `npx skills`")
                else:
                    print_warn(f"`npx skills` error installing {label}: {res.stderr.strip() or res.stdout.strip()}")
            except Exception as e:
                print_warn(f"Failed to install {label}: {e}")
    else:
        print_warn("npx command not found. Please install Node.js/npx to install skills.")

    print(f"\n{Colors.BOLD}{Colors.GREEN}✔ Repository successfully configured!{Colors.RESET}\n")

def main():
    parser = argparse.ArgumentParser(description="Configure a repository with AGENTS.md/CLAUDE.md links and essential agent skills.")
    parser.add_argument("path", nargs="?", default=".", help="Target repository directory path (default: current directory)")
    args = parser.parse_args()

    init_repository(args.path)

if __name__ == "__main__":
    main()
