# 🚀 Personal Workstation & AI Development Setup

<p align="center">
  <img src="https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue?style=for-the-badge" alt="Platform Support" />
  <img src="https://img.shields.io/badge/python-3.10%2B-brightgreen?style=for-the-badge" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/license-MIT-purple?style=for-the-badge" alt="MIT License" />
</p>

An automated, cross-platform workstation provisioner designed for modern software development and multi-agent AI coding workflows. 

Running a single command (`python3 setup.py`) configures central AI memory, developer CLI utilities, terminal aesthetics, runtimes, and an autonomous multi-agent toolsuite.

---

## 🌟 Highlights & Features

### 🧠 1. Centralized AI Global Memory
- **Centralized Guidelines**: Stores master memory files (`CLAUDE.md`, `OPINIONS.md`, `VOICE.md`) at `~/.config/ai-memory/`.
- **Automatic Symlinking**: Symlinks `~/.claude/CLAUDE.md`, `~/AGENTS.md`, `~/OPINIONS.md`, and `~/VOICE.md` to ensure any active AI coding assistant follows system rules and coding style invariants.

### ⚡ 2. Repository Initializer & CLI Utilities
- **`init-repo` / `git-init-repo`**:
  - Automatically links existing `AGENTS.md` and `CLAUDE.md` files in any workspace.
  - Installs essential agent skills via `npx skills`:
    - `skill-creator` (`anthropics/skills`)
    - `gh-axi` (GitHub CLI & API extension by `@kunchenguid`)
    - `chrome-devtools-axi` (Chrome DevTools automation extension by `@kunchenguid`)
- **`git-ai-commit`**:
  - Token-optimized Git diff generator that caps diff patches at 150 lines and filters lockfiles/binaries for concise, low-cost AI commit message generation.
- **`firstmate` Launcher**:
  - Instant terminal launcher (`firstmate` alias) that navigates to `~/.firstmate` and runs `claude`.

### 🤖 3. Multi-Agent AI Orchestration Suite
- ⛵ **[Firstmate](https://github.com/kunchenguid/firstmate)**: Agent distro for supervising multi-agent crew sessions.
- 🌳 **[Treehouse](https://github.com/kunchenguid/treehouse)**: Reusable Git worktree pool manager for instant, isolated agent environments.
- 🛡️ **[No-Mistakes](https://github.com/kunchenguid/no-mistakes)**: AI-driven validation gate & local git proxy (`git push no-mistakes`).
- 🌙 **[GNHF](https://github.com/kunchenguid/gnhf)** ("Good Night, Have Fun"): Autoresearch-style autonomous loop orchestrator for overnight agent tasks.

### 🛠️ 4. Developer Runtimes & Applications
- **Node Version Manager (NVM)** (`~/.nvm`)
- **Java SDKMAN!** (`~/.sdkman`)
- **Golang (Go)**
- **Docker & DBeaver**
- **[Herdr](https://github.com/ogulcancelik/herdr)**: Next-gen terminal workspace manager for AI agents (replaces `tmux`).
- **OpenSuperWhisper**: Voice-to-text dictation application configured with auto-detection for **English** and **Brazilian Portuguese**.
- **macOS Productivity Apps**: Maccy & Rectangle installed via Homebrew Cask and registered in macOS Login Items for automatic startup.

### 🎨 5. WezTerm Terminal Visuals
- Deploys custom [`config/wezterm/wezterm.lua`](file:///Users/thiagocavalcanti/Programacao/projetos_pessoais/setup/config/wezterm/wezterm.lua) to `~/.config/wezterm/wezterm.lua`.
- **Theme**: `rose-pine-moon`
- **Font**: `Hack Nerd Font` (size `15.0`) with automatic fallback to system fonts.
- **Effects**: `opacity = 0.8`, macOS background blur (`50`), and dynamic focus dimming on unfocused windows.

---

## 🚀 Quick Start

To provision or update your workstation setup:

```bash
git clone https://github.com/thiagocavalcanti/setup.md
cd setup
python3 setup.py
```

### Initializing a New Project Repository

Run `init-repo` inside any project folder:

```bash
init-repo /path/to/my-new-repo
```

---

## 📁 Repository Architecture

```text
setup/
├── setup.py                    # Main setup orchestrator (colorized logs, 4-step workflow)
├── CLAUDE.md                   # Repository guide for AI coding assistants
├── README.md                   # Project documentation
├── ai_memory/                  # Master AI memory templates
│   ├── CLAUDE.md
│   ├── OPINIONS.md
│   └── VOICE.md
├── config/
│   └── wezterm/
│       └── wezterm.lua         # WezTerm configuration script
└── scripts/
    ├── setup_tools.py          # Modular tools, runtimes, & apps installer
    ├── init_repo.py            # Repository initializer (AGENTS.md links + npx skills)
    └── git_ai_commit.py        # Token-optimized diff summarizer
```

---

## 📜 License

This repository is open source and available under the [MIT License](LICENSE).
