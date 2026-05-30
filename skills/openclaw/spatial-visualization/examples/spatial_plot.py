# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

'''Visualize spatial transcriptomics data'''

import squidpy as sq
import scanpy as sc
import matplotlib.pyplot as plt

adata = sc.read_h5ad('clustered.h5ad')
print(f'Loaded: {adata.n_obs} spots')

fig, axes = plt.subplots(2, 2, figsize=(12, 12))

sc.pl.spatial(adata, color='leiden', ax=axes[0, 0], show=False, title='Clusters', spot_size=1.5)

sc.pl.spatial(adata, color='total_counts', ax=axes[0, 1], show=False, title='Total counts', cmap='viridis')

sc.pl.spatial(adata, color='CD3D', ax=axes[1, 0], show=False, title='CD3D (T cells)', cmap='Reds', vmin=0)

sc.pl.spatial(adata, color='MS4A1', ax=axes[1, 1], show=False, title='MS4A1 (B cells)', cmap='Blues', vmin=0)

plt.tight_layout()
plt.savefig('spatial_overview.png', dpi=300, bbox_inches='tight')
print('Saved to spatial_overview.png')

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
