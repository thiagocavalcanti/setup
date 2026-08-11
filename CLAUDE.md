# Setup Repository - Agent Guide & Project Memory

This repository stores cross-platform computer setup scripts, CLI utilities, and global AI memory configurations for Thiago.

## Repository Architecture

- `setup.py`: Entry point script. Coordinates multi-step system setup with colorized terminal logging (`[1/N]`, `[2/N]`, `[3/N]`).
- `ai_memory/`: Source templates for global AI memory files (`CLAUDE.md`, `OPINIONS.md`, `VOICE.md`). Deployed to `~/.config/ai-memory/` and symlinked to `~/.claude/CLAUDE.md`, `~/AGENTS.md`, `~/OPINIONS.md`, `~/VOICE.md`.
- `scripts/setup_tools.py`: Modular installer for development runtimes (NVM, SDKMAN, Golang, Docker, DBeaver) and macOS apps (Maccy, Rectangle + startup login items).
- `scripts/git_ai_commit.py`: Token-optimized Git diff generator for AI commit message drafting. Installed to `~/bin/git-ai-commit`.
- `scripts/init_repo.py`: Repository initializer script. Evaluates Firstmate on machine path, links `AGENTS.md`/`CLAUDE.md`, and installs skills for chosen AI stack (`kunchenguid` or `mattpocock`).
- `scripts/check_doc_sync.py`: Evaluates staged files against `.agents/skills/doc-auto-sync/tracked_docs.json` topic match patterns to detect stale documentation before commit.
- `.agents/skills/doc-auto-sync/`: Custom skill for topic-versioned documentation tracking and token-saving pre-commit verification.

## Guidelines for Future Agents

1. **Adding New Tools / Apps**:
   - Add new software or runtime installers as modular functions inside `scripts/setup_tools.py`.
   - Maintain cross-platform compatibility checking `sys.platform` (`darwin` via Homebrew, `linux` via apt/snap/curl, `win32` via winget).
   - If adding macOS GUI apps, launch them and register them in macOS Login Items using `osascript`.

2. **Terminal Logging Standards**:
   - Use `Colors` class and helper functions (`print_step`, `print_info`, `print_success`, `print_warn`, `print_error`) for clean output.

3. **Commit & Documentation Workflow**:
   - Run `python3 scripts/check_doc_sync.py` to check for stale documentation topics. If changes touch tracked topics, update the Markdown documentation and bump topic versions in `tracked_docs.json`.
   - Before drafting git commit messages, ALWAYS run `python3 ~/scripts/git_ai_commit.py` (or `git ai-commit`) to generate a token-optimized diff summary.

4. **New Repository Configuration**:
   - Run `init-repo` (or `git init-repo`) inside any new target directory to set up memory symlinks, Firstmate, core base skills, and AI stack options.
