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
from cellidentifierdx.scoring import bayesian_score

def test_bayesian_score():
    cluster_genes = ['gene1', 'gene2', 'gene3']
    ref_genes = ['gene1', 'gene3']
    cluster_pvals_adj = {'gene1': 0.01, 'gene2': 0.05, 'gene3': 0.001}
    score = bayesian_score(cluster_genes, ref_genes, cluster_pvals_adj)
    assert np.isclose(score, 0.66666666, atol=1e-08)


__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
