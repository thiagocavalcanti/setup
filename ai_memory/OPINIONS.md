# Thiago's Technical Opinions & Viewpoints

These are technical opinions, design principles, and engineering philosophies that guide Thiago's software development.

## Engineering Standards & Architecture

* Prefer simplicity, robustness, maintainability, and scalability over quick hacks or initial development speed.
* Code should be self-documenting, clean, and strictly typed where possible.
* Cross-platform tooling is essential - scripts and configurations should work seamlessly across macOS, Linux, and Windows.
* Avoid OS-specific shell hacks; prefer Python or standardized cross-platform scripts for setup automation.

## Quality Assurance & Testing

* Fix the root cause, never patch symptoms or swallow errors.
* Always attempt to reproduce bugs in an End-to-End (E2E) environment that reflects real end-user conditions before attempting fixes.
* Be obsessive about UI/UX quality and pixel perfection - if something visually looks broken or misaligned, fix it.
* Treat lint warnings, test failures, and test flakiness with zero tolerance.

## Tooling & Workflows

* Keep dotfiles and environment configurations version-controlled in a centralized setup repository.
* Automate computer setup using clean, idempotent scripts.
* Use global AI memory files (CLAUDE.md, AGENTS.md, OPINIONS.md, VOICE.md) to maintain consistent context across AI coding assistants.
