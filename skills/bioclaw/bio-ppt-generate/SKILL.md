# bio-ppt-generate

**Presentation generation (组会汇报 PPT)**

Generate a concise presentation package from the final proposal and demo / validation outputs.

## Purpose

1. Extract the core message from `FINAL_PROPOSAL.md`
2. Incorporate demo or validation results
3. Produce a 10-15 slide presentation outline
4. Output Markdown-first slides that can be converted later

## Input Format

```text
final_proposal: [path to FINAL_PROPOSAL.md]
demo_result: [path to DEMO_VALIDATION.md or equivalent]
ppt_title: [presentation title]
author: [author]
date: [date]
```

## Suggested Slide Order

1. Title
2. Background
3. Research question
4. Innovation
5. Method overview
6. Task design
7. Data and metrics
8. Demo / validation results
9. Expected figure set
10. Biological significance
11. Next steps
12. Summary
13. Q&A

## Output Format

Preferred output:

- Markdown slide deck
- optionally HTML / reveal.js structure
- optionally a PowerPoint-style outline

```markdown
---
marp: true
theme: gaia
paginate: true
---

# [Title]

**[Author]**

[Date]

---

# Background

- ...

---

# Research Question

- ...
```

## Usage

```bash
/bio-ppt-generate "final_proposal: FINAL_PROPOSAL.md | demo_result: DEMO_VALIDATION.md | ppt_title: Project Update | author: Name | date: 2026-04-04"
```

## Notes

1. Keep the deck concise and review-friendly.
2. One slide should carry one main idea.
3. Demo evidence should be included if available.
