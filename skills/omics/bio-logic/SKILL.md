---
name: bio-logic
description: Evaluate scientific rigor, methods, biases, and evidence quality for claims, papers, and study designs.
---

# Bio-Logic: Scientific Reasoning Evaluation

Use structured frameworks to evaluate scientific claims, methodology, and evidence strength.

## Instructions

1. Identify the task (claim assessment, paper critique, study design review, project interpretation, or hypothesis revision).
2. For project work, maintain a hypothesis register with at least 5 distinct active hypotheses until the project is no longer exploratory.
3. After each major intermediate result, reflect on what changed, revise hypothesis status, and identify the next discriminating check.
4. When findings need context, pair this reasoning with a literature-search skill such as `/polars-dovmed`, then revise hypotheses against the literature.
5. Apply the relevant checklist below.
6. Structure output using the provided format.

### Project Hypothesis Loop

Use this loop for omics projects, unexpected results, exploratory analyses, and any request that asks what results mean.

1. **Initialize**: create at least 5 working hypotheses. Include biological mechanisms, technical artifacts, null explanations, sampling/batch effects, and annotation/database artifacts where relevant.
2. **Build an analysis playbook**: search the literature for the inferred organism, virus group, data type, or closest lineage. Summarize typical analyses, comparison baselines, markers/features, plots, and outlier criteria used by scientists in that literature.
3. **Reflect**: for every major intermediate result or QC gate, state the observation, QC status, strongest interpretation, remaining alternatives, and what evidence would separate them.
4. **Contextualize**: compare findings against the playbook and run additional literature searches for central or unexpected findings. Use broad synonym-aware queries and cite DOI/PMCID when available.
5. **Revise**: update each hypothesis as supported, weakened, ruled out, or unresolved. Keep ruled-out hypotheses visible with the evidence that changed their status.
6. **Replace**: if fewer than 5 active hypotheses remain during exploratory work, add plausible replacements or explicitly state why no additional plausible alternatives exist.

### Critique Checklist

Use relevant sections based on the review scope. Skip items not applicable to the study type.

```
## Methodology
- [ ] Design matches research question (causal claim → RCT needed)
- [ ] Sample size justified (power analysis reported)
- [ ] Randomization/blinding implemented where feasible
- [ ] Confounders identified and controlled
- [ ] Measurements validated and reliable

## Statistics
- [ ] Tests appropriate for data type
- [ ] Assumptions checked
- [ ] Multiple comparisons corrected
- [ ] Effect sizes + CIs reported (not just p-values)
- [ ] Missing data handled appropriately

## Interpretation
- [ ] Conclusions match evidence strength
- [ ] Limitations acknowledged
- [ ] Causal claims only from experimental designs
- [ ] No cherry-picking or overgeneralization

## Red Flags
- [ ] P-values clustered just below .05
- [ ] Outcomes differ from registration
- [ ] Correlation presented as causation
- [ ] Subgroups analyzed without preregistration
```

### Claim Assessment

1. Identify claim type (causal, associational, descriptive).
2. Match evidence to claim type.
3. Check logical connection between data and conclusion.
4. Ensure confidence matches evidence strength.

**Claim strength ladder**:
| Language | Requires |
|----------|----------|
| "Proves" / "Demonstrates" | Strong experimental evidence |
| "Suggests" / "Indicates" | Observational with controlled confounds |
| "Associated with" | Observational, no causal claim |
| "May" / "Might" | Preliminary or hypothesis-generating |

### Output Format

```markdown
## Summary
[1-2 sentences: What was studied and main finding]

## Strengths
- [Specific methodological strengths]

## Concerns
### Critical (threaten main conclusions)
- [Issue + why it matters]

### Important (affect interpretation)
- [Issue + why it matters]

### Minor (worth noting)
- [Issue]

## Evidence Rating
[GRADE level: High/Moderate/Low/Very Low with justification]

## Bottom Line
[What can/cannot be concluded from this evidence]
```

### Project Reasoning Output Format

```markdown
## Current Result
[Observed intermediate/final result and QC status]

## Hypothesis Register
| Rank | Hypothesis | Status | Evidence For | Evidence Against | Next Discriminating Check |
|------|------------|--------|--------------|------------------|---------------------------|
| 1 | [Hypothesis] | supported/weakened/ruled out/unresolved | [Evidence] | [Evidence] | [Test] |
| 2 | [Hypothesis] | ... | ... | ... | ... |
| 3 | [Hypothesis] | ... | ... | ... | ... |
| 4 | [Hypothesis] | ... | ... | ... | ... |
| 5 | [Hypothesis] | ... | ... | ... | ... |

## Literature Context
- [Paper or search result, DOI/PMCID if available]: supports/contradicts/narrows [hypothesis] because [reason].

## Analysis Playbook
- [Literature-derived analysis/comparison/outlier check and why it applies]

## Revision
[What changed since the previous register and why]

## Next Step
[Most informative analysis, control, or experiment]
```

## Quick Reference

| Task | Action |
|------|--------|
| Review a paper | Use the Critique Checklist below |
| Evaluate a claim | Use Claim Assessment steps |
| Assess evidence strength | See `references/evidence.md` |
| Identify biases | See `references/biases.md` |
| Statistical errors | See `references/stats.md` |
| Logical fallacies | See `references/fallacies.md` |
| Study design review | See `references/design.md` |

## Input Requirements

- Manuscript or study summary
- Claim statements to evaluate
- Methods and results (as available)

## Output

- Structured critique with strengths, concerns, and evidence rating
- Clear recommendation on claim strength and limitations

## Quality Gates

- [ ] Claim type matches evidence type
- [ ] Key methodological risks are identified
- [ ] Evidence rating is justified with concrete issues
- [ ] Exploratory project work includes at least 5 active hypotheses or explains why fewer are plausible
- [ ] Discovery work includes a literature-derived analysis playbook before selecting analyses
- [ ] Intermediate results update hypothesis status before the next workflow step
- [ ] Central or unexpected findings are checked against the literature before final interpretation

## Examples

### Example 1: Quick Paper Critique

**Input**: "Review this RCT on vitamin D and depression"

**Output**:
```
## Summary
RCT of 200 adults testing vitamin D supplementation for depression over 12 weeks.

## Strengths
- Randomized, double-blind, placebo-controlled
- Validated depression scale (PHQ-9)
- Adequate power analysis

## Concerns
### Critical
- 35% dropout, differential by group (attrition bias)
- ITT analysis not performed

### Important
- Single-site limits generalizability

## Evidence Rating
Moderate (downgraded from high due to attrition bias)

## Bottom Line
Suggestive but not conclusive due to differential attrition.
```

### Example 2: Claim Assessment

**Input**: "This study proves that coffee prevents Alzheimer's"

**Assessment**: If based on observational data, this is a correlation→causation error. Appropriate language: "Coffee consumption is associated with lower Alzheimer's risk."

## Troubleshooting

**Issue**: Insufficient methods details
**Solution**: Request missing design/statistics information before rating evidence.

**Issue**: Conflicting results across studies
**Solution**: Report uncertainty and suggest stronger study designs for resolution.

## Related Skills

- `/ai-scientist-evaluator` — rubric-scored evaluation of AI scientist outputs
- `/manuscript-review-council` — multi-reviewer critique of peer-reviewed manuscripts
- `/proposal-review` — structured critique of funding proposals
