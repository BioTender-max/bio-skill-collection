---
name: skill-updater
description: "Use this skill after a task succeeds (user confirms 'success' or tools report success). It extracts new experience from the session log + daily memory, locates relevant skills, and proposes diff-formatted updates to SKILL.md files with a clear summary for the user."
license: MIT License (NeuroClaw custom skill - freely modifiable within the project)
layer: interface
skill_type: workflow
dependencies: []
---
# Skill Updater (Experience-to-Skill Diff)

## Overview
`skill-updater` turns successful task execution into reusable skill improvements.

It reads the **session log** and **daily memory**, extracts new experience (what worked, new patterns, edge cases), identifies the most relevant skill files, and produces **diff-formatted** update suggestions for `SKILL.md`.

This skill follows NeuroClaw hierarchy:
- Defines **WHAT to do**, not low-level implementation details.
- Does **not** execute direct shell commands itself.
- Delegates any file scanning or execution via helper skills.

---

## When to Call This Skill
- Task just finished successfully and user confirms "success".
- A tool returns a success status and experience should be recorded.
- Repeated tasks indicate missing instructions or edge-case guidance.

---

## Core Workflow (Never Bypassed)
1. Read the **session log** and the relevant **daily memory**.
2. Extract **new experience**:
	- what worked
	- new patterns
	- edge cases solved
3. Identify the most relevant skill(s):
	- Use `skill-creator` to scan `workspace/skills/` if available.
	- If not available, request a list of relevant skill files from the user.
4. Draft **diff-formatted** changes for the target `SKILL.md`:
	- Explicitly state: "New experience X: previously missing Y, now add Z."
	- Specify which sections change: instructions / examples / error handling.
5. Present a clear summary + patch to the user.

---

## Required Output Format
Always include:

1. A concise summary list of new experience.
2. A target skill name.
3. A diff block for each proposed update.

Example output:

"""
This successful task yields new experience:
1. ...
2. ...

Suggested update for skill `xxx` (diff):
```diff
@@
- Old line
+ New line
```
"""

---

## Evidence Sources
- Session log (task execution trace)
- Daily memory (recent patterns and outcomes)

---

## Safety and Execution Policy
- Never write changes directly; only propose **diffs**.
- Do not update unrelated skills.
- Do not invent results; only use observed success outcomes.

---

## Complementary / Related Skills
- `multi-search-engine`
- `dependency-planner`

---

Created At: 2026-03-30 18:39 HKT
Last Updated At: 2026-03-30 18:39 HKT
Author: chengwang96
