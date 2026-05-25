# Composite Scoring

**Purpose**: Rank designs using multi-metric scoring strategies

## Why composite scoring is essential

Individual metrics have weak predictive power:

| Metric | ROC AUC | Predictive Power |
|--------|---------|------------------|
| ipTM | ~0.64 | Weak |
| PAE | ~0.65 | Weak |
| pLDDT | ~0.60 | Weak alone |
| ESM2 PLL | ~0.72 | Best single metric |
| **Composite** | ~0.75+ | **Always use** |

Using individual metrics alone is only slightly better than random. Composite scoring is required for meaningful design ranking.

---

## Standard composite score

Balanced weighting for general binder design:

```python
def composite_score(row):
    """
    Standard composite score for binder design.

    All values should be normalized to 0-1 scale.
    Higher score = better design.
    """
    return (
        0.30 * row['pLDDT'] +
        0.20 * row['ipTM'] +
        0.20 * (1 - row['PAE_interaction'] / 20) +  # Invert PAE
        0.15 * row['shape_complementarity'] +
        0.15 * row['esm2_pll_normalized']
    )
```

**Weight rationale:**
- pLDDT (30%): Primary structural confidence
- ipTM (20%): Interface quality
- PAE (20%): Interface alignment error
- SC (15%): Physics-based geometric fit
- ESM2 (15%): Sequence plausibility

---

## Enhanced composite score

Three-category scoring with physics metrics:

```python
def enhanced_composite_score(row):
    """
    Enhanced composite with structure, interface, and sequence components.
    """
    # Structural confidence (40%)
    structure = (
        0.15 * row['pLDDT'] +
        0.15 * row['ipTM'] +
        0.10 * (1 - row['PAE_interaction'] / 20)
    )

    # Interface physics (30%)
    interface = (
        0.10 * row['shape_complementarity'] +
        0.10 * min(row['interface_dG'] / -30, 1.0) +  # Normalize dG
        0.10 * min(row['dSASA'] / 1500, 1.0)  # Normalize dSASA
    )

    # Sequence quality (30%)
    sequence = (
        0.15 * row['esm2_pll_normalized'] +
        0.15 * max(1 - row['instability_index'] / 60, 0.0)  # Normalize II
    )

    return structure + interface + sequence
```

---

## BoltzGen Quality-Diversity Tradeoff

BoltzGen uses the `--alpha` parameter for diversity selection:

```bash
boltzgen run ... \
  --budget 60 \
  --alpha 0.01 \
  --filter_biased true
```

| Alpha | Behavior | Use Case |
|-------|----------|----------|
| 0.0 | Quality-only ranking | Maximum predicted quality |
| 0.01 | Default (slight diversity) | Standard design |
| 0.1-0.5 | Moderate diversity | Exploratory campaigns |
| 1.0 | Diversity-only | Maximum sequence diversity |

**Recommendation**: Start with alpha=0.01, increase if experimental hits are too similar.

---

## Pareto frontier selection

Select non-dominated designs across multiple metrics:

```python
import numpy as np

def pareto_frontier(df, metrics=['ipTM', 'pLDDT', 'esm2_pll'],
                    maximize=[True, True, True]):
    """
    Find Pareto-optimal designs.

    Args:
        df: DataFrame with design metrics
        metrics: Columns to optimize
        maximize: Whether to maximize each metric (True) or minimize (False)

    Returns:
        Boolean mask of Pareto-optimal designs
    """
    values = df[metrics].values.copy()

    # Convert minimization objectives to maximization
    for i, max_it in enumerate(maximize):
        if not max_it:
            values[:, i] = -values[:, i]

    is_efficient = np.ones(len(df), dtype=bool)

    for i in range(len(df)):
        if is_efficient[i]:
            # Check if any other point dominates this one
            dominated = np.all(values >= values[i], axis=1) & \
                       np.any(values > values[i], axis=1)
            is_efficient[dominated] = False

    return is_efficient

# Usage
df['pareto_optimal'] = pareto_frontier(df,
    metrics=['ipTM', 'pLDDT', 'esm2_pll'],
    maximize=[True, True, True]
)
pareto_designs = df[df['pareto_optimal']]
```

---

## Tiered selection strategy

Combine hard filters with composite scoring:

```python
def tiered_selection(df, n_select=100):
    """
    Three-tier selection strategy.

    Tier 1: Hard filters (binary pass/fail)
    Tier 2: Composite score ranking
    Tier 3: Diversity clustering
    """
    # Tier 1: Hard filters
    filtered = df[
        (df['pLDDT'] > 0.85) &
        (df['ipTM'] > 0.50) &
        (df['PAE_interaction'] < 10) &
        (df['scRMSD'] < 2.0) &
        (df['instability_index'] < 40) &
        (df['cysteine_count'] % 2 == 0)
    ].copy()

    print(f"After filters: {len(filtered)} designs")

    # Tier 2: Composite scoring
    filtered['score'] = filtered.apply(composite_score, axis=1)
    top_scored = filtered.nlargest(n_select * 2, 'score')

    # Tier 3: Diversity (cluster and select representatives)
    # Assuming sequence_cluster column exists
    if 'sequence_cluster' in top_scored.columns:
        selected = top_scored.groupby('sequence_cluster').apply(
            lambda x: x.nlargest(1, 'score')
        ).head(n_select)
    else:
        selected = top_scored.head(n_select)

    return selected
```

---

## Metric-override weighting

Adjust weights for specific targets or experimental feedback:

```python
def custom_composite_score(row, weights=None):
    """
    Composite score with customizable weights.

    Args:
        row: Design metrics
        weights: Dict of {metric: weight}, defaults provided

    Returns:
        float: Composite score
    """
    default_weights = {
        'pLDDT': 0.30,
        'ipTM': 0.20,
        'PAE_norm': 0.20,
        'shape_complementarity': 0.15,
        'esm2_pll_normalized': 0.15
    }

    if weights:
        default_weights.update(weights)

    # Normalize PAE (invert so higher is better)
    row = row.copy()
    row['PAE_norm'] = 1 - row.get('PAE_interaction', 10) / 20

    score = 0
    for metric, weight in default_weights.items():
        if metric in row:
            score += weight * row[metric]

    return score

# Example: Emphasize interface quality for difficult targets
custom_weights = {
    'ipTM': 0.35,  # Increased from 0.20
    'pLDDT': 0.20,  # Decreased from 0.30
}
df['custom_score'] = df.apply(
    lambda r: custom_composite_score(r, custom_weights),
    axis=1
)
```

---

## Design-level severity scoring

For pattern-based checks, use severity aggregation:

```python
def severity_score(liabilities):
    """
    Calculate total severity from design-level checks.

    Args:
        liabilities: List of detected liabilities with 'severity' key

    Returns:
        dict: {total, level, top_issues}
    """
    total = sum(l.get('severity', 0) for l in liabilities)
    total = min(total, 100)  # Cap at 100

    if total <= 15:
        level = 'LOW'
    elif total <= 35:
        level = 'MODERATE'
    elif total <= 60:
        level = 'HIGH'
    else:
        level = 'CRITICAL'

    # Top 3 contributors
    sorted_liabilities = sorted(liabilities,
                                key=lambda x: x.get('severity', 0),
                                reverse=True)
    top_issues = [l.get('message', '') for l in sorted_liabilities[:3]]

    return {
        'total': total,
        'level': level,
        'top_issues': top_issues
    }
```

---

## Integration with experimental feedback

After experimental validation, update weights:

```python
def calibrate_weights(experimental_df, n_iterations=100):
    """
    Calibrate composite weights using experimental results.

    Args:
        experimental_df: DataFrame with metrics + experimental_success column

    Returns:
        dict: Optimized weights
    """
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler

    feature_cols = ['pLDDT', 'ipTM', 'PAE_interaction',
                    'shape_complementarity', 'esm2_pll_normalized']

    X = experimental_df[feature_cols].values
    y = experimental_df['experimental_success'].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LogisticRegression(penalty='l2', C=1.0)
    model.fit(X_scaled, y)

    # Convert coefficients to weights
    raw_weights = np.abs(model.coef_[0])
    normalized_weights = raw_weights / raw_weights.sum()

    weights = dict(zip(feature_cols, normalized_weights))

    return weights
```

---

## Recommended workflow

1. **Pre-filter**: Apply hard thresholds (pLDDT > 0.85, ipTM > 0.50)
2. **Score**: Calculate composite score for all passing designs
3. **Rank**: Sort by composite score
4. **Diversify**: Cluster sequences, select representatives
5. **Severity check**: Flag design-level issues
6. **Select**: Take top N for experimental testing
7. **Iterate**: Calibrate weights with experimental feedback
