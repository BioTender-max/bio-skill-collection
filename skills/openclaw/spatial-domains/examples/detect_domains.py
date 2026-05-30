# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

'''Detect spatial domains'''

import squidpy as sq
import scanpy as sc

adata = sc.read_h5ad('preprocessed.h5ad')
print(f'Loaded: {adata.n_obs} spots')

sc.pp.neighbors(adata, n_neighbors=15, n_pcs=30)
sc.tl.leiden(adata, resolution=0.5, key_added='leiden')
print(f"Expression clusters: {adata.obs['leiden'].nunique()}")

sq.gr.spatial_neighbors(adata, coord_type='generic', n_neighs=6)
sc.tl.leiden(adata, resolution=0.5, key_added='spatial_leiden', neighbors_key='spatial_neighbors')
print(f"Spatial clusters: {adata.obs['spatial_leiden'].nunique()}")

sc.tl.rank_genes_groups(adata, groupby='spatial_leiden', method='wilcoxon')
markers = sc.get.rank_genes_groups_df(adata, group=None)
print('\nTop markers per domain:')
print(markers.groupby('group').head(3)[['group', 'names', 'scores']])

adata.write_h5ad('with_domains.h5ad')
print('\nSaved to with_domains.h5ad')

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
