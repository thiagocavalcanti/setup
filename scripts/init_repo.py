#!/usr/bin/env python3
"""
init_repo.py: Configures a repository by ensuring AGENTS.md and CLAUDE.md are linked,
evaluates and configures Firstmate on the machine path, and prompts the user to select
between the Kunchenguid AI Stack or the Matt Pocock AI Stack via `npx skills@latest`.
"""

import sys
import os
import shutil
import stat
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
    MAGENTA = "\033[35m"

def print_info(msg):
    print(f"  {Colors.BLUE}➔{Colors.RESET} {msg}")

def print_success(msg):
    print(f"  {Colors.GREEN}✔{Colors.RESET} {Colors.DIM}{msg}{Colors.RESET}")

def print_warn(msg):
    print(f"  {Colors.YELLOW}⚠{Colors.RESET} {msg}")

def print_error(msg):
    print(f"  {Colors.RED}✖{Colors.RESET} {msg}")

def ensure_firstmate():
    print_info("Evaluating Firstmate configuration on machine path...")
    home = Path.home()
    firstmate_dir = home / ".firstmate"
    firstmate_bin = home / "bin" / "firstmate"

    if firstmate_dir.exists() and (firstmate_bin.exists() or shutil.which("firstmate")):
        print_info("Updating Firstmate repository at ~/.firstmate...")
        res = subprocess.run(["git", "-C", str(firstmate_dir), "pull"], capture_output=True, text=True)
        if res.returncode == 0 or "Already up to date" in res.stdout or "Already up to date" in res.stderr:
            print_success("Firstmate is already configured on machine path at ~/.firstmate")
        else:
            print_warn(f"Firstmate update: {res.stderr.strip() or res.stdout.strip()}")
    else:
        print_info("Firstmate is not configured on machine path. Installing to ~/.firstmate...")
        res = subprocess.run(["git", "clone", "https://github.com/kunchenguid/firstmate", str(firstmate_dir)], capture_output=True, text=True)
        if res.returncode == 0 or firstmate_dir.exists():
            print_success("Cloned Firstmate to ~/.firstmate")
        else:
            print_error(f"Failed to clone Firstmate: {res.stderr}")

        firstmate_bin.parent.mkdir(parents=True, exist_ok=True)
        wrapper_content = '#!/bin/sh\ncd "$HOME/.firstmate" && exec claude "$@"\n'
        firstmate_bin.write_text(wrapper_content, encoding="utf-8")
        firstmate_bin.chmod(firstmate_bin.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print_success(f"Installed firstmate launcher command at {firstmate_bin}")

def prompt_stack_selection(cli_choice=None):
    if cli_choice in ["kunchenguid", "mattpocock"]:
        return cli_choice

    if not sys.stdin.isatty():
        print_info("Non-interactive terminal detected. Defaulting to 'kunchenguid' AI stack.")
        return "kunchenguid"

    print(f"\n{Colors.BOLD}{Colors.CYAN}Select AI Stack to Install:{Colors.RESET}")
    print(f"  {Colors.BOLD}1){Colors.RESET} {Colors.GREEN}Kunchenguid AI Stack{Colors.RESET} (skill-creator, gh-axi, chrome-devtools-axi, Firstmate, Treehouse, No-Mistakes, GNHF)")
    print(f"  {Colors.BOLD}2){Colors.RESET} {Colors.MAGENTA}Matt Pocock AI Stack{Colors.RESET} (mattpocock/skills: setup-matt-pocock-skills, ask-matt, grill-with-docs, wayfinder, to-spec, to-tickets, implement, code-review)")
    
    try:
        choice = input(f"\nChoose stack [{Colors.BOLD}1{Colors.RESET}/2] (default: 1): ").strip()
        if choice == "2" or choice.lower().startswith("m") or choice.lower().startswith("2"):
            return "mattpocock"
        return "kunchenguid"
    except (KeyboardInterrupt, EOFError):
        print("\n")
        return "kunchenguid"

def install_stack_skills(repo_dir, stack_choice):
    npx_bin = shutil.which("npx")
    if not npx_bin:
        print_warn("npx command not found. Please install Node.js/npx to install skills.")
        return

    if stack_choice == "kunchenguid":
        print_info("Installing Kunchenguid AI Stack skills via `npx skills@latest`...")
        skills = [
            ("anthropics/skills", "skill-creator", "skill-creator"),
            ("kunchenguid/gh-axi", None, "gh-axi (GitHub Extension)"),
            ("kunchenguid/chrome-devtools-axi", None, "chrome-devtools-axi (Chrome DevTools Extension)")
        ]
        for pkg, skill_name, label in skills:
            cmd = [npx_bin, "-y", "skills@latest", "add", pkg, "-y"]
            if skill_name:
                cmd.extend(["--skill", skill_name])
            try:
                res = subprocess.run(cmd, cwd=str(repo_dir), capture_output=True, text=True)
                if res.returncode == 0:
                    print_success(f"Installed '{label}' via `npx skills@latest`")
                else:
                    print_warn(f"`npx skills` error installing {label}: {res.stderr.strip() or res.stdout.strip()}")
            except Exception as e:
                print_warn(f"Failed to install {label}: {e}")
        print_success("Kunchenguid Multi-Agent AI Toolsuite fully configured.")

    elif stack_choice == "mattpocock":
        print_info("Installing Matt Pocock AI Stack skills via `npx skills@latest add mattpocock/skills`...")
        matt_skills = [
            "setup-matt-pocock-skills",
            "ask-matt",
            "grill-with-docs",
            "wayfinder",
            "to-spec",
            "to-tickets",
            "implement",
            "code-review"
        ]
        cmd = [npx_bin, "-y", "skills@latest", "add", "mattpocock/skills", "-y"]
        for sk in matt_skills:
            cmd.extend(["--skill", sk])
        try:
            res = subprocess.run(cmd, cwd=str(repo_dir), capture_output=True, text=True)
            if res.returncode == 0:
                print_success(f"Installed Matt Pocock skills ({', '.join(matt_skills)})")
            else:
                print_warn(f"Error installing Matt Pocock skills: {res.stderr.strip() or res.stdout.strip()}")
        except Exception as e:
            print_warn(f"Failed to install Matt Pocock skills: {e}")

def init_repository(target_path, cli_stack=None):
    repo_dir = Path(target_path).resolve()
    print(f"\n{Colors.BOLD}{Colors.CYAN}Initializing repository at:{Colors.RESET} {repo_dir}\n")

    if not repo_dir.exists():
        repo_dir.mkdir(parents=True, exist_ok=True)
        print_info(f"Created repository directory: {repo_dir}")

    # 1. Handle Firstmate Configuration on Machine Path
    ensure_firstmate()

    # 2. Handle Memory Files & Symlinks
    agents_md = repo_dir / "AGENTS.md"
    claude_md = repo_dir / "CLAUDE.md"

    has_agents = agents_md.exists() or agents_md.is_symlink()
    has_claude = claude_md.exists() or claude_md.is_symlink()

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

    # 3. Stack Prompt & Skills Installation
    chosen_stack = prompt_stack_selection(cli_stack)
    print_info(f"Selected stack: {Colors.BOLD}{chosen_stack}{Colors.RESET}")
    install_stack_skills(repo_dir, chosen_stack)

    print(f"\n{Colors.BOLD}{Colors.GREEN}✔ Repository successfully configured!{Colors.RESET}\n")

def main():
    parser = argparse.ArgumentParser(description="Configure a repository with AGENTS.md/CLAUDE.md links, Firstmate, and AI agent skills.")
    parser.add_argument("path", nargs="?", default=".", help="Target repository directory path (default: current directory)")
    parser.add_argument("--stack", choices=["kunchenguid", "mattpocock"], help="AI Stack to install (kunchenguid or mattpocock)")
    args = parser.parse_args()

    init_repository(args.path, cli_stack=args.stack)

if __name__ == "__main__":
    main()
