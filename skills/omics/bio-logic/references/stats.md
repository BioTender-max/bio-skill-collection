# Statistical Pitfalls Reference

## P-Value Misinterpretations

| Misconception | Reality |
|---------------|---------|
| p = .05 means 5% chance null is true | p = probability of data if null true |
| p > .05 proves no effect | Absence of evidence ≠ evidence of absence |
| p < .05 means important effect | Statistical ≠ practical significance |
| p = .049 vs .051 are different | Nearly identical evidence |

**Red flag**: p-values clustered just below .05

## Multiple Comparisons

**Problem**: Testing 20 hypotheses at α=.05 → ~65% chance of false positive

**Corrections**:
- Bonferroni: α/n (conservative)
- FDR (Benjamini-Hochberg): Less conservative
- Prespecify primary outcome

**Warning signs**: Many subgroups tested, exploratory analyses presented as confirmatory

## Power and Sample Size

| Issue | Consequence |
|-------|-------------|
| Underpowered study | High false negatives, inflated effect sizes when significant |
| No power analysis | Can't interpret null results |
| Post-hoc power | Uninformative (just transforms p-value) |

**Rule of thumb**: n < 30 per group warrants skepticism

## Effect Size Interpretation

| Measure | Small | Medium | Large |
|---------|-------|--------|-------|
| Cohen's d | 0.2 | 0.5 | 0.8 |
| r | 0.1 | 0.3 | 0.5 |
| OR | 1.5 | 2.5 | 4.0 |
| η² | .01 | .06 | .14 |

**Caution**: Field-specific norms vary. Always report effect sizes + CIs, not just p-values.

## Common Statistical Errors

| Error | Why Wrong |
|-------|-----------|
| Correlation → causation | Confounding, reverse causation possible |
| Ecological fallacy | Group-level ≠ individual-level relationships |
| Simpson's paradox | Aggregated trend can reverse subgroup trends |
| Regression to mean | Extreme scores naturally become less extreme |

## Regression Pitfalls

| Pitfall | Detection | Fix |
|---------|-----------|-----|
| Overfitting | R² high, cross-validation poor | Penalized regression, holdout set |
| Multicollinearity | VIF > 10, unstable coefficients | Remove redundant predictors |
| Extrapolation | Predictions outside data range | Only interpolate |
| Assumption violations | Residual plots | Transformations, robust methods |

## Missing Data

| Type | Meaning | Safe Methods |
|------|---------|--------------|
| MCAR | Completely random | Listwise deletion OK |
| MAR | Random given observed data | Multiple imputation, ML |
| MNAR | Related to missing values | Sensitivity analysis required |

**Red flag**: >20% missing without analysis of missingness patterns

## Confidence Interval Interpretation

- 95% CI: If repeated infinitely, 95% of intervals contain true value
- Overlapping CIs ≠ no significant difference (less stringent than direct comparison)
- Wide CIs = low precision, skepticism warranted even if "significant"

## Test Selection Quick Reference

| Data Type | Groups | Test |
|-----------|--------|------|
| Continuous, normal | 2 independent | Independent t-test |
| Continuous, normal | 2 paired | Paired t-test |
| Continuous, normal | 3+ groups | ANOVA |
| Continuous, non-normal | 2 groups | Mann-Whitney U |
| Continuous, non-normal | 3+ groups | Kruskal-Wallis |
| Categorical | 2x2 | Chi-square (or Fisher's if n<5) |
| Correlation, linear | - | Pearson r |
| Correlation, non-linear | - | Spearman ρ |
