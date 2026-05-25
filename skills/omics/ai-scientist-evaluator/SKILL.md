---
name: ai-scientist-evaluator
description: >-
  Critically review, score, compare, and rank one or more AI scientist outputs
  for biology, bioinformatics, computational life science, or adjacent research
  tasks. Trigger when the user asks to evaluate notebooks, code, figures,
  analyses, manuscripts, software, or final reports produced by AI scientists;
  compare multiple AI scientists on the same task; judge publication readiness;
  or audit rigor, reproducibility, novelty, and task completion. Do not use
  this skill to perform the original research task itself unless the user is
  explicitly asking for a reviewer-style audit of already produced outputs.
---

# AI Scientist Evaluator

Use this skill when Codex should behave like a skeptical reviewer panel rather
than a research generator. Evaluate completed outputs, not just plans.

## Instructions

1. Confirm the request is evaluative. Use this skill to audit or compare
   existing outputs, not to perform the original research task.
2. Restate the exact task in one or two sentences so the review stays anchored
   to the real objective and required deliverables.
3. Inventory the submitted artifacts and note what is missing. Prefer primary
   artifacts over summaries:
   - notebooks, code, scripts, and workflow files
   - environment files, package versions, and runtime logs
   - figures, tables, and manuscript drafts
   - data provenance, accession lists, database versions, and citations
   - benchmark results, hardware notes, and task constraints
4. Choose the closest task profile from
   [`references/task_profiles.md`](references/task_profiles.md) and load the
   matching weights from
   [`assets/default_weight_profiles.yaml`](assets/default_weight_profiles.yaml).
   Use the primary scientific profile first for composite tasks, then add
   manuscript comments as a secondary layer.
5. Review with a four-person panel and synthesize a consensus:
   - scientific validity reviewer
   - computational and reproducibility reviewer
   - domain biology reviewer
   - writing and editorial reviewer
6. Apply hard gates before generous scoring. A submission is not
   publication-ready if required deliverables are missing, claims are not
   supported by visible outputs, provenance is untraceable, the core method is
   not rerunnable, or the submission solves an easier adjacent problem.
7. Interrogate the submission with the relevant sections of
   [`references/question_bank.md`](references/question_bank.md). Always include
   the universal questions, then add the profile-specific and multi-submission
   questions when needed.
8. Scan for integrity, rigor, and validity problems using
   [`references/red_flags.md`](references/red_flags.md). Penalize missing
   evidence, task drift, unsupported biological claims, fabricated identifiers,
   and unverifiable citations more than polished narrative.
9. Score each category on the anchored 0 to 5 scale in
   [`references/score_scale.md`](references/score_scale.md). Use
   [`references/category_definitions.md`](references/category_definitions.md) if
   category meaning is unclear. A score of 5 earns the full category weight.
10. Convert the category scores to a weighted total out of 100. Apply explicit
    penalties sparingly and explain them when they are not already captured by
    the category scores.
11. For multiple submissions, score each one independently before ranking. Use
    tie-breaks in this order:
    - fewer integrity or reproducibility problems
    - better satisfaction of the task's main objective
    - stronger validation or benchmarking
    - clearer limitation handling
    - better writing only after science and evidence are settled
12. Produce a concise consensus verdict with actionable revisions. Ground the
    review in concrete evidence from files, notebook cells, figure numbers,
    accessions, parameters, and versioned tools whenever possible.
13. When a structured artifact is useful, start from
    [`assets/evaluation_template.json`](assets/evaluation_template.json) and
    validate the shape against
    [`assets/evaluation_schema.json`](assets/evaluation_schema.json). Use
    [`assets/report_template.md`](assets/report_template.md) for markdown
    reports. For completed JSON reviews, you may aggregate rankings with
    `python scripts/aggregate_reviews.py review1.json review2.json --out_md leaderboard.md`.

## Quick Reference

| Task | Action |
|------|--------|
| General scientific audit | Use profile `scientific-analysis` |
| Phylogenomics or comparative genomics review | Use profile `phylogenomics-comparative-genomics` |
| Viral functional genomics review | Use profile `viral-functional-genomics` |
| Methods or software benchmark review | Use profile `methods-software` |
| Manuscript or short communication review | Use profile `manuscript-packaging` |
| Pick scoring weights | Read `assets/default_weight_profiles.yaml` |
| Interpret category names | Read `references/category_definitions.md` |
| Ask evidence-forcing review questions | Read `references/question_bank.md` |
| Check integrity and rigor failures | Read `references/red_flags.md` |
| Score consistently | Read `references/score_scale.md` |
| Draft a report | Use `assets/report_template.md` |
| Produce structured JSON | Use `assets/evaluation_template.json` and `assets/evaluation_schema.json` |
| Rank finished JSON reviews | Run `python scripts/aggregate_reviews.py review1.json review2.json --out_md leaderboard.md` |

## Input Requirements

- The original task statement, success criteria, and any explicit constraints
- One or more completed submissions or artifacts to review
- Enough evidence to audit claims when available:
  - notebooks, code, scripts, workflows, or repositories
  - figures, tables, and manuscript drafts
  - environment files, runtime notes, and benchmark context
  - accession lists, database versions, citations, and provenance notes
- Submission names or IDs when comparing multiple AI scientists

If key artifacts are missing, continue the review and mark the evidence gap
explicitly instead of pretending certainty.

## Output

For a single submission, produce:

- a verdict paragraph
- a gate-check table
- a weighted score table
- reviewer panel comments by category
- answers to the most important critical questions
- required revisions
- a final recommendation label

For multiple submissions, produce:

- a consensus ranking table
- per-submission totals and category scores
- pairwise comparison notes
- best-in-class awards for science, reproducibility, writing, and engineering
- a winner with justification
- a merge recommendation when combining strengths would outperform any one entry

Use these recommendation labels:

- `90-100`: Outstanding / near publication-ready
- `75-89`: Strong but needs minor to moderate revision
- `60-74`: Promising but major revision needed
- `40-59`: Weak / unreliable in important respects
- `<40`: Not trustworthy for scientific use

## Quality Gates

- [ ] The review is anchored to the exact task rather than an easier adjacent one
- [ ] Artifact inventory and missing evidence are stated explicitly
- [ ] A task profile and weight set were chosen deliberately
- [ ] Hard gates were checked before final scoring
- [ ] Questions and red flags were grounded in the provided artifacts
- [ ] Scores follow the anchored 0 to 5 scale and sum to a weighted total out of 100
- [ ] Multi-submission rankings were done only after independent scoring
- [ ] Final recommendations distinguish absent, flawed, weakly validated, and well-supported work

## Examples

### Example 1: Compare five AI scientist submissions

```text
Use $ai-scientist-evaluator to review five AI scientist submissions for the
same task. Inspect notebooks, code, figures, runtime notes, and manuscripts.
Score each submission with the appropriate weight profile, answer the critical
questions, identify red flags, and produce a ranked consensus table with
best-in-class awards.
```

### Example 2: Audit one submission for publication readiness

```text
Use $ai-scientist-evaluator to review this AI scientist submission as if you are
a skeptical reviewer panel. Tell me whether the notebook and manuscript really
support the main claims, score the work, and list the revisions required before
I would trust it.
```

### Example 3: Rank finished JSON evaluations

```bash
python scripts/aggregate_reviews.py review_a.json review_b.json --out_md leaderboard.md
```

## Troubleshooting

**Issue**: The submission includes only a polished manuscript and no underlying artifacts.
**Solution**: Continue the review, but mark reproducibility and claim-evidence gaps explicitly and do not award publication-ready status.

**Issue**: The task spans more than one domain profile.
**Solution**: Score with the closest primary scientific profile first, then add manuscript or secondary-domain comments without inventing a new weight set unless the user asks for one.

**Issue**: Multiple submissions look close in total score.
**Solution**: Break ties with integrity, task completion, validation strength, and limitation handling before writing quality.

**Issue**: A claim looks impressive but evidence is thin or missing.
**Solution**: Penalize unsupported claims, cite the missing evidence directly, and keep the verdict skeptical.

## Related Skills

- `/bio-logic` — general scientific reasoning beyond AI evaluation
- `/manuscript-review-council` — equivalent pipeline for human-authored manuscripts
- `/scientific-writing` — draft the evaluation writeup
