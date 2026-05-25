# Experimental Design Checklist

## Pre-Study Checklist

```
## Research Question
- [ ] Specific and answerable
- [ ] Falsifiable hypothesis
- [ ] Variables operationally defined
- [ ] Literature gap identified

## Design Selection
- [ ] Matches research question (causal → experimental)
- [ ] Ethical constraints considered
- [ ] Feasibility assessed
- [ ] Power analysis completed (target: 80-90%)

## Bias Control
- [ ] Randomization method specified
- [ ] Allocation concealment planned
- [ ] Blinding at all feasible levels
- [ ] Confounders identified with control strategy
```

## Design Selection Guide

| Question Type | Best Design | Why |
|---------------|-------------|-----|
| Does X cause Y? | RCT | Controls confounding |
| Is X associated with Y? | Cohort | Temporal sequence |
| Why did Y happen? | Case-control | Efficient for rare outcomes |
| How common is Y? | Cross-sectional | Prevalence estimate |

## Sample Size Quick Guide

**For difference between means**:
```
n per group ≈ 16 × (SD/d)² × 2
where d = expected mean difference
```

**For correlations**:
- r = 0.3 → n ≈ 85
- r = 0.5 → n ≈ 30

**Rule**: Account for 15-20% attrition

## Randomization Methods

| Method | When to Use |
|--------|-------------|
| Simple | Large samples, no key covariates |
| Stratified | Balance key variables across groups |
| Block | Ensure equal group sizes |
| Cluster | Groups randomized (not individuals) |

**Critical**: Allocation concealment (sequence hidden until enrollment)

## Blinding Levels

| Level | Who's Blinded | Prevents |
|-------|---------------|----------|
| Single | Participants | Performance bias |
| Double | + Researchers | Observer bias |
| Triple | + Data analysts | Analysis bias |

## Control Groups

| Type | Use Case |
|------|----------|
| No treatment | Natural history comparison |
| Placebo | Control for expectation effects |
| Active control | Comparison to standard care |
| Wait-list | Ethical when treatment beneficial |

## Validity Threats

### Internal (Causal Inference)
- Selection bias
- Confounding
- Attrition
- Maturation
- History (external events)
- Regression to mean
- Testing effects

### External (Generalizability)
- Sample not representative
- Artificial setting
- Volunteer bias
- Time-specific effects

## Measurement Checklist

```
- [ ] Validated instruments
- [ ] Reliability established (test-retest, inter-rater)
- [ ] Sensitivity to expected change
- [ ] No floor/ceiling effects
- [ ] Blinded assessment
- [ ] Multiple measures of key constructs
```

## Analysis Plan (Prespecify)

```
- [ ] Primary outcome designated
- [ ] Primary analysis specified
- [ ] Secondary analyses labeled
- [ ] Multiple comparison correction chosen
- [ ] Missing data strategy
- [ ] Sensitivity analyses planned
```

## Reporting Guidelines

| Study Type | Guideline |
|------------|-----------|
| RCT | CONSORT |
| Observational | STROBE |
| Systematic review | PRISMA |
| Diagnostic | STARD |
| Qualitative | COREQ |

## Registration

**When**: Before data collection
**Where**: ClinicalTrials.gov, OSF, AsPredicted
**What**: Hypotheses, methods, analysis plan

**Purpose**: Distinguishes confirmatory from exploratory, prevents outcome switching
