---
name: manuscript-review-council
description: Run a multi-agent scientific manuscript review with parallel specialist reviewers, disagreement checks, and an editor meta-review. Use when reviewing a manuscript, preprint, revision, or rebuttal in Codex or Claude Code.
---

# Manuscript Review Council

Run a journal-style review council instead of a single blended opinion. This skill is self-contained and works in both Codex and Claude Code.

The council definition lives in local files:
- role roster: `references/reviewer-roles.md`
- workflow and artifact bundle: `references/council-workflow.md`
- per-reviewer handoff template: `templates/reviewer-brief.md`
- editor synthesis template: `templates/editor-meta-review.md`

## Instructions

1. Confirm the review context: manuscript or revision stage, target venue if known, desired decision scale, and whether the user wants a full review, triage, version comparison, or rebuttal assessment.
2. Gather the review packet before delegating:
   - manuscript text or accessible PDF/DOCX
   - title, abstract, main claims, methods snapshot, and figure or table list
   - user priorities such as novelty, rigor, statistics, reproducibility, or journal fit
   - prior reviews or author response if this is a revision
3. Normalize the manuscript into a shared packet for every reviewer. At minimum, preserve section boundaries, figure references, and the claims being evaluated. If the source is a PDF or DOCX, extract a sectioned text view before review. Use `references/council-workflow.md` for the packet contents.
4. Load the local council definition before delegating:
   - reviewer roles and activation rules: `references/reviewer-roles.md`
   - stage flow and artifact bundle: `references/council-workflow.md`
   - reviewer prompt skeleton: `templates/reviewer-brief.md`
   - editor synthesis skeleton: `templates/editor-meta-review.md`
5. Use the platform's native delegation primitive when available:
   - Codex: spawn specialist sub-agents or workers
   - Claude Code: spawn Task agents or equivalent delegated runs
   - If delegation is unavailable, emulate the same reviewer roles sequentially and keep outputs role-separated
6. Launch these three default reviewers in parallel:
   - Domain reviewer: novelty, significance, positioning against prior work, and overclaiming
   - Methods and statistics reviewer: design, controls, benchmarks, sample size, figure interpretation, and analysis validity
   - Skeptical reviewer: weakest links, alternate explanations, unsupported causal claims, and missing controls
7. Add support reviewers only when triggered by the manuscript:
   - Reproducibility reviewer for computational papers, code or data availability, workflow clarity, and parameter transparency
   - Ethics or compliance reviewer for human subjects, animal work, privacy, conflicts, dual-use, or citation bias concerns
   - Translational reviewer when the manuscript makes clinical, ecological, or deployment claims that need reality checks
8. Give every reviewer the same structured contract:
   - one-paragraph summary
   - top strengths
   - major concerns
   - minor concerns
   - must-fix experiments or analyses
   - confidence level
   - provisional recommendation: `accept`, `minor_revision`, `major_revision`, or `reject`
   - direct grounding in manuscript sections, figures, tables, or explicit missing information
9. Require reviewers to ground criticisms in the manuscript text or in clearly missing information. Do not invent citations, datasets, reviewer expectations, or unstated experiments.
10. Run a cross-review pass after the first round:
   - compare disagreements
   - merge duplicate concerns
   - identify the few issues that actually drive the decision
   - separate fatal flaws from fixable revision items
11. Capture a lightweight artifact bundle even if the user only asked for prose:
    - shared review packet
    - reviewer reports
    - disagreement or conflict notes
    - editor meta-review
12. Write an editor meta-review that includes:
   - headline recommendation
   - rationale across novelty, rigor, evidence strength, clarity, reproducibility, and significance
   - ranked major revisions
   - ranked minor revisions
   - questions for the authors
   - a short decision letter or reviewer summary
13. If outside validation is needed, do targeted spot-checks instead of broad literature review:
    - use `/polars-dovmed` for claim-specific literature context
    - use `/bio-logic` for evidence-strength and causal-claim stress tests
    - never fabricate supporting papers
14. If the user wants polished review prose, a rebuttal outline, or a cleaned-up decision letter, use `/scientific-writing` after the council establishes the factual review skeleton.
15. Preserve provenance in the final deliverable:
    - keep per-reviewer notes separate from the editor synthesis
    - point to sections, figures, or tables when possible
    - clearly mark inference versus explicit manuscript statement

## Quick Reference

| Task | Action |
|------|--------|
| Full manuscript review | Run the 3-reviewer council plus editor synthesis |
| Computational manuscript | Add a reproducibility reviewer |
| Human, animal, or clinical manuscript | Add an ethics or compliance reviewer |
| Revision assessment | Compare prior critiques to the new draft and label each issue resolved, partial, or unresolved |
| Fast triage | Use domain reviewer plus skeptic, then write a short editor recommendation |
| Rebuttal check | Judge whether the author response closes the decision-driving issues |
| Reviewer definitions | Read `references/reviewer-roles.md` |
| Stage flow and artifacts | Read `references/council-workflow.md` |

## Input Requirements

- Manuscript text or an accessible PDF/DOCX
- Optional journal rubric, scorecard, or decision scale
- Optional prior reviews, decision letter, rebuttal, or previous manuscript version
- Optional focus areas such as novelty, methods, statistics, reproducibility, or clarity

## Output

- Role-separated reviewer notes
- A short disagreement or adjudication log
- An editor meta-review with a clear recommendation
- A prioritized major and minor revision list
- Specific questions for the authors
- Optional decision letter, rebuttal assessment, or version-delta summary

## Quality Gates

- [ ] At least three distinct reviewer roles are used, or the reduced scope is justified explicitly
- [ ] Reviewer outputs stay role-separated until synthesis
- [ ] Major concerns are grounded in manuscript text or explicit missing information
- [ ] Reviewer disagreements are adjudicated explicitly instead of silently averaged
- [ ] The final recommendation matches the ranked issues
- [ ] No citations, datasets, experiments, or venue rules are invented
- [ ] Reproducibility and ethics checks are added when the manuscript warrants them

## Examples

### Example 1: Full journal-style review

```text
Review this microbiome manuscript with a multi-agent council. Use domain,
methods/statistics, skeptic, and reproducibility reviewers. End with an editor
meta-review, a recommendation, and ranked major/minor revisions.
```

### Example 2: Revision comparison

```text
Compare this revised manuscript against the prior decision letter. Tell me
which major issues are resolved, partially resolved, or still open, then write
an editor recommendation.
```

### Example 3: Fast triage

```text
Give me a fast desk-review style assessment of this preprint. Use only a domain
reviewer and a skeptic, then summarize whether it is promising, immature, or
fatally flawed.
```

## Troubleshooting

**Issue**: The manuscript is too long for every reviewer to read in full.
**Solution**: Build a shared review packet first, then route only the relevant sections, claims, and figures to each reviewer while keeping a common abstract and methods snapshot.

**Issue**: Reviewers disagree sharply.
**Solution**: Make the disagreement explicit, identify the evidence each reviewer is using, and let the editor resolve the conflict instead of averaging positions.

**Issue**: No journal rubric or venue is provided.
**Solution**: State the default criteria being applied: novelty, rigor, evidence strength, clarity, reproducibility, and significance.

**Issue**: Only one agent can run.
**Solution**: Emulate the council sequentially with role-scoped passes and keep the notes separated until the editor synthesis step.

## Related Skills

- `/scientific-writing` — apply the reviewer feedback to the manuscript
- `/bio-logic` — deeper reasoning about evidence strength
- `/ai-scientist-evaluator` — equivalent pipeline for AI scientist outputs
