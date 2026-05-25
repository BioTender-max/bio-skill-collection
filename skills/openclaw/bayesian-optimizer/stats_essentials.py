# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import numpy as np
import scipy.stats as stats

def hypothesis_testing_demo():
    print("--- Hypothesis Testing: T-Test ---")
    # Scenario: Drug A (Control) vs Drug B (Treatment)
    # Effect is "Blood Pressure Reduction"
    
    np.random.seed(42)
    group_a = np.random.normal(loc=10, scale=5, size=30)  # Mean drop 10
    group_b = np.random.normal(loc=14, scale=5, size=30)  # Mean drop 14 (Better)
    
    print(f"Group A Mean: {np.mean(group_a):.2f}")
    print(f"Group B Mean: {np.mean(group_b):.2f}")
    
    # Null Hypothesis (H0): Means are equal
    # Alt Hypothesis (H1): Means are different
    
    t_stat, p_val = stats.ttest_ind(group_a, group_b)
    
    print(f"T-Statistic: {t_stat:.4f}")
    print(f"P-Value: {p_val:.4f}")
    
    if p_val < 0.05:
        print("Result: Significant difference (Reject H0)")
    else:
        print("Result: No significant difference (Fail to reject H0)")

def distributions_demo():
    print("\n--- Probability Distributions ---")
    
    # 1. Normal (Gaussian)
    # Central Limit Theorem in action
    samples = np.random.uniform(0, 1, (1000, 10)) # 1000 sums of 10 uniform vars
    sums = np.sum(samples, axis=1)
    
    print(f"Uniform Sum Mean (approx Normal): {np.mean(sums):.2f}")
    print(f"Uniform Sum Std: {np.std(sums):.2f}")
    
    # 2. Poisson (Events per interval)
    # Rare events: e.g., genetic mutations per 1Mb
    lam = 3
    poisson_samples = np.random.poisson(lam, 1000)
    print(f"Poisson (lambda={lam}) Mean: {np.mean(poisson_samples):.2f}")

if __name__ == "__main__":
    hypothesis_testing_demo()
    distributions_demo()

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
