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
from scipy.stats import dirichlet

def bayesian_score(cluster_genes, ref_genes, cluster_pvals_adj):
    alpha = np.array([1.0] * len(cluster_genes))
    pvals_adj = np.array([cluster_pvals_adj[gene] if gene in ref_genes else 1 for gene in cluster_genes])
    gene_expr_prob = 1 - pvals_adj
    alpha += gene_expr_prob
    posterior_mean = dirichlet.mean(alpha)
    matched_genes = len(set(cluster_genes) & set(ref_genes))
    proportion_matched_genes = matched_genes / len(ref_genes)
    bayesian_score = np.sum(posterior_mean) * proportion_matched_genes
    return bayesian_score


__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
