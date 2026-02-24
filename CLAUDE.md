# Project Overview

This repository contains an agentic workflow and/or web application system.

The goal is to build clean, production-ready software using small, testable, incremental changes.

This file defines high-level engineering standards for the repository.

---

# Before You Start

- Always read `project_specs.md` before implementing features.
- Review relevant existing files before introducing new structure.
- Do not begin implementation without understanding the current scope.

---

# Engineering Principles

- Prefer clarity over cleverness.
- Make small, focused changes.
- Do not refactor unrelated code.
- Follow existing patterns in the codebase.
- Avoid introducing new abstractions unless necessary.

If architectural changes are required, explain why before proceeding.

---

# File Structure

Typical structure:

- `/app` or `/src` → Application code
- `/tmp` → Test files
- `/scripts` → Local utilities (non-production)
- `.env` → Environment variables (never edit or commit)
- `project_specs.md` → Current feature definition

Place new code where similar code already exists.

Do not create new top-level folders without approval.

---

# Testing & Safety

- Add tests when introducing new behavior.
- Add regression tests when fixing bugs.
- Never remove tests without explanation.
- Never hardcode secrets.
- Never modify `.env` directly.
- Ask before deleting or renaming critical files.

---

# Scope Control

Stay within the scope defined in `project_specs.md`.

If requirements are unclear, ask for clarification.
Do not assume missing details.

---

# Core Rule

Act as a disciplined senior engineer operating inside a real codebase.

Define clearly.
Change minimally.
Verify before expanding.