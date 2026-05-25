# Bias Detection Reference

## Cognitive Biases (Researcher)

| Bias | Signs | Mitigation |
|------|-------|------------|
| Confirmation | Only supporting evidence cited | Preregister, seek disconfirming data |
| HARKing | Hypotheses match results perfectly | Check registration vs publication |
| Publication | Missing negative results | Include grey literature, funnel plots |
| Hindsight | Post-hoc rationalization | Document predictions before data |

## Selection Biases

| Bias | Signs | Mitigation |
|------|-------|------------|
| Sampling | Non-representative sample | Compare to target population |
| Volunteer | Self-selected participants | Document who declined, why |
| Attrition | Differential dropout | Compare dropouts to completers |
| Survivorship | Only "survivors" in sample | Consider who's missing |
| Berkson's | Hospital-based sample | Use population-based controls |

## Measurement Biases

| Bias | Signs | Mitigation |
|------|-------|------------|
| Observer | Unblinded assessors | Blind outcome assessment |
| Recall | Retrospective self-report | Use records, prospective design |
| Social desirability | Sensitive topics | Anonymous, validated scales |
| Instrument | Systematic measurement error | Calibration, validation |

## Analysis Biases

| Bias | Signs | Mitigation |
|------|-------|------------|
| P-hacking | p-values clustered at .049 | Preregister analysis plan |
| Outcome switching | Different outcomes than registered | Compare to registration |
| Subgroup fishing | Many subgroups, no correction | Require prespecification |
| Selective reporting | Missing planned outcomes | Use reporting checklists |

## Confounding

**Detection questions**:
- What affects both exposure AND outcome?
- Were these measured and controlled?
- Could unmeasured confounding explain findings?
- Is there residual confounding after adjustment?

**Control methods**: Randomization > matching > stratification > statistical adjustment > restriction

## Study-Level Bias Assessment

### Cochrane Risk of Bias Domains

1. **Selection**: Random sequence generation, allocation concealment
2. **Performance**: Blinding of participants and personnel
3. **Detection**: Blinding of outcome assessment
4. **Attrition**: Incomplete outcome data
5. **Reporting**: Selective outcome reporting
6. **Other**: Funding, early stopping, baseline imbalance

Rate each: Low risk / High risk / Unclear

### Newcastle-Ottawa Scale (Observational)

- **Selection** (max 4 stars): Representativeness, selection of controls, exposure ascertainment
- **Comparability** (max 2 stars): Confounding control
- **Outcome** (max 3 stars): Assessment, follow-up adequacy
