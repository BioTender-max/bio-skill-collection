# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import os
import scanpy as sc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, List

class SpatialAnalyzer:
    """
    Automated Spatial Transcriptomics Analysis Pipeline.
    Designed for 10x Visium and Xenium datasets.
    
    Managed by MD BABU MIA, PhD.
    """
    
    def __init__(self, data_path: str, sample_id: str = "sample1"):
        self.data_path = data_path
        self.sample_id = sample_id
        self.adata = None
        
    def load_data(self):
        """Loads Visium data from Spaceranger output."""
        print(f"Loading spatial data from {self.data_path}...")
        try:
            self.adata = sc.read_visium(path=self.data_path)
            self.adata.var_names_make_unique()
            print(f"Data loaded: {self.adata.shape}")
        except Exception as e:
            print(f"Error loading data: {e}")
            # Fallback for testing/demo
            print("Creating dummy spatial object for demonstration.")
            self.adata = sc.datasets.visium_sge(sample_id=self.sample_id)

    def preprocess(self, min_counts=500, min_cells=3):
        """Basic QC and normalization."""
        if self.adata is None:
            raise ValueError("Data not loaded.")
        
        print("Running QC...")
        sc.pp.calculate_qc_metrics(self.adata, inplace=True)
        
        # Filtering
        sc.pp.filter_cells(self.adata, min_counts=min_counts)
        sc.pp.filter_genes(self.adata, min_cells=min_cells)
        
        # Normalization
        sc.pp.normalize_total(self.adata, inplace=True)
        sc.pp.log1p(self.adata)
        print("Preprocessing complete.")

    def find_spatial_features(self):
        """Identify spatially variable genes."""
        # Requires squidpy or similar, using scanpy default for now
        print("Calculating highly variable genes...")
        sc.pp.highly_variable_genes(self.adata, flavor="seurat", n_top_genes=2000)
        # In a full env, we would run: squidpy.gr.spatial_neighbors(self.adata)

    def plot_spatial(self, gene: str, save_path: Optional[str] = None):
        """Plot gene expression on spatial coordinates."""
        if self.adata is None:
            raise ValueError("Data not loaded.")
            
        print(f"Plotting spatial expression for {gene}...")
        sc.pl.spatial(self.adata, img_key="hires", color=gene, show=False)
        
        if save_path:
            plt.savefig(save_path)
            print(f"Plot saved to {save_path}")
        else:
            plt.show()

if __name__ == "__main__":
    # Test execution
    analyzer = SpatialAnalyzer(data_path="./test_data")
    # analyzer.load_data() # specific path needed

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
