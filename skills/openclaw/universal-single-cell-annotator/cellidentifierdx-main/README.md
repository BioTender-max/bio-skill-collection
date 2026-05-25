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

1. **Project Name**: Single Cell Annotation by cellidentifierdx.
2. **Description**: Annotate your single cell using cellidentifierd.
3. **Installation**: Instructions for how to install your project.
4. **Usage**: Instructions for how to use your project after it's installed.
5. **License**: The license your project is distributed under.
6. Note: This software package is yet to be published (unpublished)! If you have used it for publication purpose, please share authorship with MD. BABU MIA, PHD; ICAHN SCHOOL OF MEDICINE AT MOUNT SINAI. Contact for detials: md.babu.mia@mssm.edu
# CellIdentifierDX

CellIdentifierDX is a Python package for identifying cell types using Bayesian scoring.

## Installation

You can install CellIdentifierDX using pip:

```bash
pip install cellidentifierdx
```

## Usage

Here's a basic example of how to use 
--> Extract 250 genes per cluster: 
#getting to gene lists - step 2 continue
import os
import numpy as np
import pandas as pd
import anndata
import scanpy as sc
import scvi
import scipy.io
import matplotlib.pyplot as plt



# Perform differential expression analysis
sc.tl.rank_genes_groups(combined_adata, groupby="leiden_scvi", key_added="rank_genes", method="t-test_overestim_var", n_genes=250)

# Extract marker genes for each cluster along with their scores, fold changes, and p-values
marker_genes_250 = pd.DataFrame(combined_adata.uns['rank_genes']['names']).head(250)
marker_scores_250 = pd.DataFrame(combined_adata.uns['rank_genes']['scores']).head(250)
marker_logfoldchanges_250 = pd.DataFrame(combined_adata.uns['rank_genes']['logfoldchanges']).head(250)
marker_pvals_250 = pd.DataFrame(combined_adata.uns['rank_genes']['pvals']).head(250)
marker_pvals_adj_250 = pd.DataFrame(combined_adata.uns['rank_genes']['pvals_adj']).head(250)

# Melt each DataFrame to create a long format and add cluster information
melted_dataframes = []
for cluster_idx in marker_genes_250.columns:
    cluster_df = pd.DataFrame(
        {
            "Cluster": cluster_idx,
            "Gene": marker_genes_250[cluster_idx],
            "Score": marker_scores_250[cluster_idx],
            "Log2FoldChange": marker_logfoldchanges_250[cluster_idx],
            "P-value": marker_pvals_250[cluster_idx],
            "Adjusted P-value": marker_pvals_adj_250[cluster_idx],
        }
    )
    melted_dataframes.append(cluster_df)
    
# Concatenate the melted_dataframes into a single DataFrame
marker_genes_info_250 = pd.concat(melted_dataframes, axis=0, ignore_index=True)

# Set the dataset identifier
dataset_identifier = "dataset name"

# Save the detailed information for the top 250 genes to a CSV file
marker_genes_info_250.to_csv(f"pathtosave/{dataset_identifier}_marker_genes_details_250.csv", index=False)

# Save the gene names only for the top 250 genes to a separate CSV file
marker_genes_250.to_csv(f"pathtosave/{dataset_identifier}_marker_genes_only_250.csv", index=False)

--> CellIdentifierDX:

```python
from cellidentifierdx import annotate_cell_types

reference_file = "/path/to/your/reference_file.xlsx"
expr_file = "/path/to/your/expr_file.csv"
tissue, cell_type_annotations = annotate_cell_types(reference_file, expr_file, 'sheetname')

for cluster_idx, cell_type, avg_score in cell_type_annotations:
    print(f"Cluster {cluster_idx} is annotated as {cell_type} with average Bayesian score of {avg_score}.")

```

## License

MIT
```


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->