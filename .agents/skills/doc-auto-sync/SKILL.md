---
name: doc-auto-sync
description: Automatic documentation tracking and topic-versioned sync system. Inspects staged codebase changes against tracked documentation topics, checks topic versions in tracked_docs.json, updates relevant docs before commit, and bumps topic versions to save tokens and eliminate stale documentation.
---

# 📚 Documentation Auto-Sync & Topic Versioning Skill

This skill guarantees that project documentation (`README.md`, `CLAUDE.md`, etc.) remains **100% synchronized with code changes** while minimizing token consumption.

---

## 🎯 Topic Versioning Mechanism

Documentation is split into discrete **tracked topics**, managed via `.agents/skills/doc-auto-sync/tracked_docs.json`:

Each topic specifies:
- `id`: Unique topic identifier (e.g. `init-repo-stacks`).
- `name`: Human-readable topic label.
- `version`: Integer version counter incremented upon documentation updates.
- `match_patterns`: Code/script glob patterns that trigger a topic update decision.

---

## 🔄 AI Agent Workflow (Pre-Commit Documentation Decision)

Before drafting any Git commit:

### Step 1: Run Doc Sync Evaluator
Run `python3 scripts/check_doc_sync.py` or inspect staged files against `tracked_docs.json`:
```bash
python3 scripts/check_doc_sync.py
```

### Step 2: Decision Tree
- **If STALE topics are detected**:
  1. Read ONLY the documentation sections corresponding to the STALE topic IDs.
  2. Update the Markdown documentation to accurately reflect code changes.
  3. Increment the topic `version` counter by `1` in `tracked_docs.json`.
  4. Stage the updated documentation file AND `tracked_docs.json` (`git add README.md .agents/skills/doc-auto-sync/tracked_docs.json`).
- **If NO STALE topics are detected**:
  - Skip documentation edits completely to save tokens and maintain commit speed.

---

## 📁 Tracked Manifest Schema (`tracked_docs.json`)

```json
{
  "version": "1.0.0",
  "tracked_files": [
    {
      "path": "README.md",
      "topics": [
        {
          "id": "init-repo-stacks",
          "name": "init-repo & AI Stack Options",
          "version": 1,
          "description": "Repository initializer, Firstmate evaluation, Kunchenguid & Matt Pocock stack options",
          "match_patterns": ["scripts/init_repo.py"]
        }
      ]
    }
  ]
}
```
