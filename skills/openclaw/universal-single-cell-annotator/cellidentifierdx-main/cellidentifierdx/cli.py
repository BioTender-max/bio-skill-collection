# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import pandas as pd
import numpy as np
from .utils import load_data
from .scoring import bayesian_score

def annotate_cell_types(reference_file, expr_file, sheet_name):
    ref_df = pd.read_excel(reference_file, sheet_name=sheet_name)
    expr_df = pd.read_csv(expr_file)
    cell_type_annotations = []
    
    for cluster_idx in range(len(expr_df['Cluster'].unique())):
        cluster_data = expr_df[expr_df['Cluster'] == cluster_idx]
        cluster_genes = cluster_data['Gene'].tolist()
        cluster_pvals_adj = cluster_data.set_index('Gene')['Adjusted P-value'].to_dict()

        cell_type_scores = {}
        for _, row in ref_df.iterrows():
            cell_type = row["CELL TYPES"]
            ref_genes = row["Markers"].split(",")
            cell_type_scores[cell_type] = bayesian_score(cluster_genes, ref_genes, cluster_pvals_adj)

        if cell_type_scores:  # Check if dictionary is not empty
            best_cell_type = max(cell_type_scores, key=cell_type_scores.get)
            cell_type_annotations.append((cluster_idx, best_cell_type, np.mean(list(cell_type_scores.values()))))

    return sheet_name, cell_type_annotations



__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
