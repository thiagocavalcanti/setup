#!/usr/bin/env python3
"""
init_repo.py: Configures a repository with an empty AGENTS.md, a CLAUDE.md symlink, 
and installs the 'skill-creator' skill.
"""

import sys
import os
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

SKILL_CREATOR_CONTENT = """---
name: skill-creator
description: Create, structure, and refine new agent skills for this repository. Use when designing a new skill, adding runbooks, or documenting domain-specific agent workflows.
---

# Skill Creator Guide

This skill provides step-by-step guidance for creating high-quality, reusable skills for AI agents.

## What is a Skill?

A Skill is a directory containing a `SKILL.md` file (and optional helper scripts or resources) that teaches AI agents how to perform specialized multi-step tasks, execute runbooks, or use specific tools.

## Skill Folder Structure

```
.agents/skills/<skill-name>/
├── SKILL.md (Required: main instructions with YAML frontmatter)
├── scripts/ (Optional: helper scripts)
└── references/ (Optional: additional documentation or templates)
```

## SKILL.md Specification

Every `SKILL.md` must begin with YAML frontmatter:

```yaml
---
name: <skill-name-kebab-case>
description: <Clear 1-2 sentence description of when and why the agent should activate this skill>
---
```

## Workflow to Create a New Skill

1. Identify the task or runbook to automate.
2. Create the directory `.agents/skills/<skill-name>/`.
3. Create `SKILL.md` with descriptive YAML frontmatter.
4. Document clear, step-by-step instructions, pre-requisites, command invocations, and verification steps.
5. If helper scripts are needed, place them in `.agents/skills/<skill-name>/scripts/`.
"""

def init_repository(target_path):
    repo_dir = Path(target_path).resolve()
    print(f"\n{Colors.BOLD}{Colors.CYAN}Initializing repository at:{Colors.RESET} {repo_dir}\n")

    if not repo_dir.exists():
        repo_dir.mkdir(parents=True, exist_ok=True)
        print_info(f"Created repository directory: {repo_dir}")

    # 1. Create empty AGENTS.md
    agents_md = repo_dir / "AGENTS.md"
    if not agents_md.exists():
        agents_md.write_text("", encoding="utf-8")
        print_success("Created empty AGENTS.md file")
    else:
        print_info("AGENTS.md already exists")

    # 2. Create symlink CLAUDE.md -> AGENTS.md
    claude_md = repo_dir / "CLAUDE.md"
    if claude_md.exists() or claude_md.is_symlink():
        print_info("CLAUDE.md already exists")
    else:
        claude_md.symlink_to(Path("AGENTS.md"))
        print_success("Created symlink: CLAUDE.md -> AGENTS.md")

    # 3. Add skill-creator skill
    skill_dirs = [
        repo_dir / ".agents" / "skills" / "skill-creator",
        repo_dir / ".claude" / "skills" / "skill-creator"
    ]

    for skill_dir in skill_dirs:
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(SKILL_CREATOR_CONTENT, encoding="utf-8")
        print_success(f"Installed 'skill-creator' skill at {skill_file.relative_to(repo_dir)}")

    print(f"\n{Colors.BOLD}{Colors.GREEN}✔ Repository successfully configured!{Colors.RESET}\n")

def main():
    parser = argparse.ArgumentParser(description="Configure a new repository with AGENTS.md, CLAUDE.md symlink, and skill-creator.")
    parser.add_argument("path", nargs="?", default=".", help="Target repository directory path (default: current directory)")
    args = parser.parse_args()

    init_repository(args.path)

if __name__ == "__main__":
    main()
