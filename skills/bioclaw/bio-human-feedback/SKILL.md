# bio-human-feedback

**Phase 2.6: Human review checkpoint (人类反馈验证)**

Present the refined proposal to a human reviewer, collect feedback, and decide whether to continue or loop back for revision.

## Purpose

1. Present the current proposal in a concise reviewable form
2. Wait for explicit human feedback
3. Record approval or requested changes
4. Route the workflow back to the correct phase if needed

## Inputs

- `FINAL_PROPOSAL.md`
- current round number

## Workflow

1. Present the proposal summary
2. Wait for approval or feedback
3. Classify the feedback severity
4. Record the response and decide the next phase

## Human Review Summary Format

```markdown
# Proposal Review - Round X

## Innovation Summary
- ...

## Figure Overview
- Figure 1:
- Figure 2:

## Experimental Plan
| Task | Dataset | Metric | Baseline |
|------|---------|--------|----------|
| ... | ... | ... | ... |

## Key Decisions Requiring Human Approval
1. ...
2. ...

## Reviewer Summary
| Reviewer | Score / status | Main advice |
|----------|----------------|-------------|
| Editor | ... | ... |
| Computational | ... | ... |
| Biological | ... | ... |

## Human Decision
- Approve and continue
- Request revisions
```

## Feedback Severity

- **Critical**: return to early planning
- **Major**: return to design / manuscript refinement
- **Minor**: revise locally and continue

## Files To Record

- `refine-logs/human-feedback/feedback-round-X.md`
- `refine-logs/HUMAN_APPROVAL.md`

## Usage

```bash
/bio-human-feedback --round 2 --proposal refine-logs/FINAL_PROPOSAL.md
```

## Notes

1. Do not continue automatically without explicit human approval.
2. Record all human feedback in the workspace.
3. Keep the requested decisions concise and actionable.
