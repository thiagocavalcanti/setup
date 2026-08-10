import os
import shutil
import sys
import stat
import subprocess
from pathlib import Path

# Terminal Colors & Formatting
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

def print_header(title):
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}========================================{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}  {title}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}========================================{Colors.RESET}\n")

def print_step(step_num, total_steps, title):
    print(f"{Colors.BOLD}{Colors.CYAN}[{step_num}/{total_steps}]{Colors.RESET} {Colors.BOLD}{title}{Colors.RESET}")

def print_info(message):
    print(f"  {Colors.BLUE}➔{Colors.RESET} {message}")

def print_success(message):
    print(f"  {Colors.GREEN}✔{Colors.RESET} {Colors.DIM}{message}{Colors.RESET}")

def print_warn(message):
    print(f"  {Colors.YELLOW}⚠{Colors.RESET} {message}")

def print_error(message):
    print(f"  {Colors.RED}✖{Colors.RESET} {message}")

def setup_ai_memory_and_tools():
    print_header("Personal System Setup")
    repo_dir = Path(__file__).parent.resolve()
    home_dir = Path.home()

    total_steps = 3

    # Step 1: AI Memory Files Setup
    print_step(1, total_steps, "Setting up AI Global Memory...")
    ai_memory_src = repo_dir / "ai_memory"
    if not ai_memory_src.exists():
        print_error(f"Source directory {ai_memory_src} does not exist.")
        sys.exit(1)

    config_ai_memory_dir = home_dir / ".config" / "ai-memory"
    config_ai_memory_dir.mkdir(parents=True, exist_ok=True)
    
    files_mapping = [
        ("CLAUDE.md", "CLAUDE.md", [home_dir / ".claude" / "CLAUDE.md", home_dir / "AGENTS.md"]),
        ("OPINIONS.md", "OPINIONS.md", [home_dir / "OPINIONS.md"]),
        ("VOICE.md", "VOICE.md", [home_dir / "VOICE.md"])
    ]

    for src_name, central_name, symlink_targets in files_mapping:
        source_file = ai_memory_src / src_name
        if not source_file.exists():
            print_warn(f"{source_file} does not exist, skipping.")
            continue

        central_file = config_ai_memory_dir / central_name
        print_info(f"Copying {src_name} -> {central_file}")
        shutil.copy2(source_file, central_file)

        for symlink_target in symlink_targets:
            symlink_target.parent.mkdir(parents=True, exist_ok=True)
            if symlink_target.exists() or symlink_target.is_symlink():
                symlink_target.unlink(missing_ok=True)
            
            print_success(f"Symlinked {symlink_target} -> {central_file}")
            symlink_target.symlink_to(central_file)

    # Step 2: Scripts and CLI Tools Setup
    print()
    print_step(2, total_steps, "Setting up CLI Tools & Scripts...")
    scripts_src = repo_dir / "scripts" / "git_ai_commit.py"
    if scripts_src.exists():
        user_scripts_dir = home_dir / "scripts"
        user_scripts_dir.mkdir(parents=True, exist_ok=True)
        dest_script = user_scripts_dir / "git_ai_commit.py"
        
        print_info(f"Copying git_ai_commit.py -> {dest_script}")
        shutil.copy2(scripts_src, dest_script)
        dest_script.chmod(dest_script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        candidate_bin_dirs = [
            home_dir / ".local" / "bin",
            home_dir / "bin"
        ]

        installed_bin = False
        for bin_dir in candidate_bin_dirs:
            try:
                bin_dir.mkdir(parents=True, exist_ok=True)
                bin_symlink = bin_dir / "git-ai-commit"
                if bin_symlink.exists() or bin_symlink.is_symlink():
                    bin_symlink.unlink(missing_ok=True)
                bin_symlink.symlink_to(dest_script)
                print_success(f"Installed CLI command: {bin_symlink} -> {dest_script}")
                installed_bin = True
                break
            except Exception as e:
                print_warn(f"Could not use {bin_dir} ({e}). Trying fallback...")

        if not installed_bin:
            print_warn("Could not create symlink in standard bin directories. Available at ~/scripts/git_ai_commit.py.")

    # Step 3: Development Tools & Mac Apps
    print()
    print_step(3, total_steps, "Setting up Development Tools & macOS Apps...")
    setup_tools_script = repo_dir / "scripts" / "setup_tools.py"
    if setup_tools_script.exists():
        subprocess.run([sys.executable, str(setup_tools_script)])
    else:
        print_warn(f"setup_tools.py not found at {setup_tools_script}")

    print(f"\n{Colors.BOLD}{Colors.GREEN}✔ Personal System Setup completed successfully!{Colors.RESET}\n")

if __name__ == "__main__":
    setup_ai_memory_and_tools()
