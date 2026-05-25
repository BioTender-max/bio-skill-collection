---
name: proposal-review
description: Structured, decision-ready review framework for AI/ML, computational biology, and bioscience proposals. Use when evaluating grant, project, or funding proposals.
---

# Proposal Review

Produce a rigorous, decision-ready review for AI/ML, computational biology, and bioscience proposals. Be fair, skeptical, specific, and explicit about missing information.

## Instructions

1. Read the proposal and identify the decision context if provided: sponsor goals, rubric, budget cap, timeline, and risk tolerance.
2. If critical information is missing, do not invent it. Flag the gap and turn it into a prioritized question for the PI.
3. Structure the review with these sections:
   - Executive summary
   - Heilmeier catechism
   - Technical merit
   - Data, compute, and experimental resources
   - Risk register
   - Team and execution capability
   - Ethics, safety, and compliance
   - Budget and schedule realism
   - Scorecard
   - Decision and funding conditions
   - Questions for the PI
4. Tailor the technical review to the proposal type:
   - AI/ML: baselines, ablations, leakage prevention, calibration, external validation, compute realism
   - Bio or wet lab: controls, replicates, statistical plan, assay feasibility, translational path
5. Include at least six risks covering technical, data or experimental, budget or timeline, and adoption or regulatory concerns when relevant.
6. Provide a weighted scorecard on a 1 to 5 scale with short justifications for each score.
7. End with a clear funding recommendation: `Strong Accept`, `Accept`, `Borderline`, or `Reject`.
8. Keep the review concrete and action-oriented. Reference proposal details when available and name fatal flaws plainly.

## Quick Reference

| Task | Action |
|------|--------|
| Summarize proposal | Describe aims, novelty, and bottom-line recommendation in <=150 words |
| Test strategic logic | Answer the Heilmeier catechism explicitly |
| Review feasibility | Check assumptions, methods, milestones, and resource realism |
| Review rigor | Assess controls, baselines, validation, statistics, and reproducibility |
| Review risk | Build a risk register with likelihood, impact, warning signs, and mitigations |
| Make a decision | Give a final recommendation plus concrete funding conditions or rejection reasons |

## Input Requirements

- Proposal text or a linkable proposal excerpt
- Optional sponsor or program context
- Optional scoring rubric, budget cap, and timeline constraints

## Output

- A decision-ready structured proposal review
- A weighted scorecard with justified subscores
- A clear funding recommendation and conditions
- A prioritized list of questions that could change the decision

## Quality Gates

- [ ] Missing information is flagged instead of invented
- [ ] The review covers novelty, rigor, feasibility, risks, team, ethics, and budget
- [ ] At least six concrete risks are documented with mitigations
- [ ] The final recommendation is explicit and consistent with the evidence

## Examples

### Example 1: Review a computational biology grant draft

```text
Review this proposal for a microbiome foundation-model project. Use a 1-5 scorecard,
identify fatal flaws if any, and list conditions for funding.
```

### Example 2: Review with sponsor constraints

```text
Review this translational bioscience proposal for a program with a 24-month timeline,
$1.5M budget cap, and high concern for regulatory risk.
```

## Troubleshooting

**Issue**: The proposal is missing a clear evaluation plan
**Solution**: Mark this as a major weakness, explain what convincing evidence would look like, and add PI questions about milestones and success metrics.

**Issue**: The budget or timeline is hard to judge
**Solution**: State the uncertainty, identify the likely critical path, and evaluate whether the claimed scope is credible under the stated constraints.

**Issue**: Ethics or compliance details are absent
**Solution**: Treat the omission as a potential blocker and ask targeted questions about subjects, privacy, biosafety, or regulatory readiness.

## Related Skills

- `/manuscript-review-council` — equivalent pipeline for manuscripts
- `/scientific-writing` — draft or revise the proposal narrative
- `/bio-logic` — assess methodology and evidence rigor
