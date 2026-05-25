<!--
# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

-->

# Tutorial: Self-Driving Labs with Bayesian Optimization

**Level:** Advanced
**Prerequisites:** Python, Numpy, Basic Statistics
**Estimated Time:** 30 Minutes

## Introduction

In "Self-Driving Labs", AI doesn't just analyze data—it **decides what experiment to run next**.

Experiments are expensive. We can't test every drug combination. We need to find the best candidate with the fewest tests. This is where **Bayesian Optimization** shines.

It uses a statistical model (Gaussian Process) to balance:
1.  **Exploitation:** Testing areas we think are good (high predicted yield).
2.  **Exploration:** Testing areas we know nothing about (high uncertainty).

## The Code Structure

The `BayesianOptimizer` class in `bayesian_optimization.py` has three key parts:

1.  `fit(X, Y)`: Trains the Gaussian Process on experiments we've already done.
2.  `predict(X_new)`: Guesses the outcome (mean) and uncertainty (variance) for new parameters.
3.  `propose_next_location()`: Uses the **Upper Confidence Bound (UCB)** math to pick the best next experiment.

## Step-by-Step Implementation

### Step 1: Define your "Lab Experiment"
In a real lab, this is a robot. Here, we simulate it with a function.

```python
def protein_yield(params):
    temperature = params[0]
    ph = params[1]
    
    # Optimum at Temp=37, pH=7.4
    return -((temperature - 37)**2 + (ph - 7.4)**2)
```

### Step 2: Initialize the Optimizer
Define the bounds.
*   Temperature: 20 to 50
*   pH: 0 to 14

```python
from bayesian_optimization import BayesianOptimizer

opt = BayesianOptimizer(bounds=[(20.0, 50.0), (0.0, 14.0)])
```

### Step 3: The "Closed Loop"
Run the loop: **AI Suggests -> Robot Executes -> AI Learns**.

```python
known_params = []
known_results = []

for i in range(10):
    # 1. AI Suggests
    next_conditions = opt.propose_next_location()
    
    # 2. Robot Executes (Simulation)
    result = protein_yield(next_conditions)
    
    # 3. AI Learns
    known_params.append(next_conditions)
    known_results.append(result)
    opt.fit(known_params, known_results)
    
    print(f"Batch {i}: Tried {next_conditions} -> Yield {result}")
```

## Why this matters?

Standard "Grid Search" (trying every combination) would take 1000s of experiments. Bayesian Optimization can find the optimum in 10-20 steps. This reduces R&D costs by 90%.

## Assignments
1.  Modify `synthetic_experiment` in `bayesian_optimization.py` to be a 2D function (like the protein yield example above).
2.  Tune the `kappa` parameter. What happens if you make it 10.0? (Hint: The AI becomes more curious/exploratory).


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->