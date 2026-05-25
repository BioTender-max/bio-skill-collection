# bio-manuscript-refine

**Refine loop: three-reviewer iterative refinement (三审稿人迭代优化)**

Run a reviewer-style refinement loop over the manuscript plan using three perspectives: editor, computational reviewer, and biological reviewer.

## Purpose

1. Review the current manuscript plan
2. Produce structured review comments
3. Revise the proposal round by round
4. Track score history and revision history

## Input Format

```text
manuscript_plan: [full manuscript plan generated in previous steps]
target_journal: [target journal, default nat-communications]
num_rounds: [number of refine rounds, default 2]
```

## Workflow

### Round 0

- save the initial proposal snapshot

### Each review round

Produce three reviews:

1. **Editor**
   - novelty
   - feasibility
   - journal fit
2. **Computational reviewer**
   - method design
   - technical rigor
   - benchmark quality
   - implementation feasibility
3. **Biological reviewer**
   - biological significance
   - analysis design
   - dataset suitability

Then generate:

- a review summary
- a revision response
- a refined proposal

## Output Format

```markdown
# Refine Report

## Round 0
- initial proposal snapshot

## Round 1 Reviews
### Editor
- scores:
- key concerns:

### Computational Reviewer
- scores:
- key concerns:

### Biological Reviewer
- scores:
- key concerns:

## Round 1 Revision
- addressed concerns:
- remaining risks:

## Score History
| Round | Editor | Computational | Biological | Overall |
|-------|--------|---------------|------------|---------|
| 0 | ... | ... | ... | ... |

## Final Proposal Status
- ready for next phase / needs more revision
```

## Reviewer Criteria

### Editor

- novelty
- feasibility
- journal fit

### Computational reviewer

- algorithmic soundness
- method novelty
- benchmark rigor
- code feasibility

### Biological reviewer

- biological significance
- analysis relevance
- dataset realism

## Usage

```bash
/bio-manuscript-refine "manuscript_plan: [path to proposal] | target_journal: nat-communications | num_rounds: 2"
```

## Notes

1. Revision should update the proposal itself, not only append comments.
2. Keep a full history of each round.
3. Scores are guidance, not absolute truth; comments matter more than raw numbers.
