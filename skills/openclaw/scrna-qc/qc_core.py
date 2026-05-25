# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

#!/usr/bin/env python3
"""
Core utility functions for single-cell RNA-seq quality control.

This module provides building blocks for metrics calculation and filtering
while following scverse best practices from:
https://www.sc-best-practices.org/preprocessing_visualization/quality_control.html
"""

import anndata as ad
import scanpy as sc
import numpy as np
from scipy.stats import median_abs_deviation


def _apply_transform(values, transform):
    if transform is None:
        return values
    if transform == 'log1p':
        return np.log1p(values)
    raise ValueError(f"Unsupported transform: {transform}")


def calculate_qc_metrics(adata, mt_pattern='mt-,MT-', ribo_pattern='Rpl,Rps,RPL,RPS',
                        hb_pattern='^Hb[^(p)]|^HB[^(P)]', inplace=True):
    """
    Calculate QC metrics for single-cell RNA-seq data.

    Parameters
    ----------
    adata : AnnData
        Annotated data matrix
    mt_pattern : str
        Comma-separated mitochondrial gene prefixes (default: 'mt-,MT-')
    ribo_pattern : str
        Comma-separated ribosomal gene prefixes (default: 'Rpl,Rps,RPL,RPS')
    hb_pattern : str
        Regex pattern for hemoglobin genes (default: '^Hb[^(p)]|^HB[^(P)]')
    inplace : bool
        Modify adata in place (default: True)

    Returns
    -------
    AnnData or None
        If inplace=False, returns modified AnnData. Otherwise modifies in place.
    """
    if not inplace:
        adata = adata.copy()

    # Identify gene categories
    mt_prefixes = tuple(mt_pattern.split(','))
    adata.var['mt'] = adata.var_names.str.startswith(mt_prefixes)

    ribo_prefixes = tuple(ribo_pattern.split(','))
    adata.var['ribo'] = adata.var_names.str.startswith(ribo_prefixes)

    adata.var['hb'] = adata.var_names.str.match(hb_pattern)

    # Calculate QC metrics
    sc.pp.calculate_qc_metrics(
        adata,
        qc_vars=['mt', 'ribo', 'hb'],
        percent_top=None,
        log1p=False,
        inplace=True
    )

    if not inplace:
        return adata


def detect_outliers_mad(adata, metric, n_mads, transform=None, tail='both', verbose=True):
    """
    Detect outliers using Median Absolute Deviation (MAD).

    Parameters
    ----------
    adata : AnnData
        Annotated data matrix with QC metrics
    metric : str
        Column name in adata.obs to use for outlier detection
    n_mads : float
        Number of MADs to use as threshold
    transform : str or None
        Optional transform applied before MAD calculation (e.g., 'log1p')
    tail : str
        Which tail(s) to flag: 'both', 'high', or 'low'
    verbose : bool
        Print outlier statistics (default: True)

    Returns
    -------
    np.ndarray
        Boolean mask where True indicates outliers
    """
    metric_values = adata.obs[metric]
    transformed = _apply_transform(metric_values, transform)
    median = np.median(transformed)
    mad = median_abs_deviation(transformed)

    # Calculate bounds
    lower = median - n_mads * mad
    upper = median + n_mads * mad

    if tail == 'both':
        outlier_mask = (transformed < lower) | (transformed > upper)
    elif tail == 'high':
        outlier_mask = transformed > upper
    elif tail == 'low':
        outlier_mask = transformed < lower
    else:
        raise ValueError(f"Invalid tail: {tail}. Use 'both', 'high', or 'low'.")

    if verbose:
        print(f"  {metric}:")
        print(f"    Median: {median:.2f}, MAD: {mad:.2f}")
        print(f"    Bounds: [{lower:.2f}, {upper:.2f}] ({n_mads} MADs, tail={tail}, transform={transform})")
        print(f"    Outliers: {outlier_mask.sum()} cells ({outlier_mask.sum()/len(metric_values)*100:.2f}%)")

    return outlier_mask


def apply_hard_threshold(adata, metric, threshold, operator='>', verbose=True):
    """
    Apply a hard threshold filter.

    Parameters
    ----------
    adata : AnnData
        Annotated data matrix
    metric : str
        Column name in adata.obs to filter on
    threshold : float
        Threshold value
    operator : str
        Comparison operator: '>', '<', '>=', '<=' (default: '>')
    verbose : bool
        Print filtering statistics (default: True)

    Returns
    -------
    np.ndarray
        Boolean mask where True indicates cells to filter out
    """
    metric_values = adata.obs[metric]

    if operator == '>':
        mask = metric_values > threshold
    elif operator == '<':
        mask = metric_values < threshold
    elif operator == '>=':
        mask = metric_values >= threshold
    elif operator == '<=':
        mask = metric_values <= threshold
    else:
        raise ValueError(f"Invalid operator: {operator}. Use '>', '<', '>=', or '<='")

    if verbose:
        print(f"  {metric} {operator} {threshold}:")
        print(f"    Cells filtered: {mask.sum()} ({mask.sum()/len(metric_values)*100:.2f}%)")

    return mask


def filter_cells(adata, mask, inplace=False):
    """
    Filter cells based on a boolean mask.

    Parameters
    ----------
    adata : AnnData
        Annotated data matrix
    mask : np.ndarray or pd.Series
        Boolean mask where True indicates cells to KEEP
    inplace : bool
        Modify adata in place (default: False)

    Returns
    -------
    AnnData
        Filtered AnnData object
    """
    if inplace:
        # This is actually a bit tricky - AnnData doesn't support true inplace filtering
        # Return filtered copy which caller should reassign
        return adata[mask].copy()
    else:
        return adata[mask].copy()


def build_qc_masks(
    adata,
    mad_counts=5,
    mad_genes=5,
    mad_mt=3,
    mt_threshold=8,
    counts_transform='log1p',
    genes_transform='log1p',
    mt_transform=None,
    verbose=True
):
    """
    Generate QC outlier masks and the combined pass/fail mask.

    Returns a dict with outlier masks and a 'pass_qc' boolean mask.
    """
    outlier_counts = detect_outliers_mad(
        adata, 'total_counts', mad_counts,
        transform=counts_transform, tail='both', verbose=verbose
    )
    outlier_genes = detect_outliers_mad(
        adata, 'n_genes_by_counts', mad_genes,
        transform=genes_transform, tail='both', verbose=verbose
    )
    outlier_mt = detect_outliers_mad(
        adata, 'pct_counts_mt', mad_mt,
        transform=mt_transform, tail='high', verbose=verbose
    )

    if verbose:
        print(f"\n  Applying hard threshold for mitochondrial content (>{mt_threshold}%):")
    high_mt_mask = apply_hard_threshold(
        adata, 'pct_counts_mt', mt_threshold, operator='>', verbose=verbose
    )
    outlier_mt = outlier_mt | high_mt_mask

    pass_qc = ~(outlier_counts | outlier_genes | outlier_mt)
    return {
        'outlier_counts': outlier_counts,
        'outlier_genes': outlier_genes,
        'outlier_mt': outlier_mt,
        'high_mt': high_mt_mask,
        'pass_qc': pass_qc
    }


def filter_genes(adata, min_cells=20, min_counts=None, inplace=True):
    """
    Filter genes based on detection thresholds.

    Parameters
    ----------
    adata : AnnData
        Annotated data matrix
    min_cells : int
        Minimum number of cells a gene must be detected in (default: 20)
    min_counts : int, optional
        Minimum total counts across all cells
    inplace : bool
        Modify adata in place (default: True)

    Returns
    -------
    AnnData or None
        If inplace=False, returns filtered AnnData
    """
    if not inplace:
        adata = adata.copy()

    if min_cells is not None:
        sc.pp.filter_genes(adata, min_cells=min_cells)

    if min_counts is not None:
        sc.pp.filter_genes(adata, min_counts=min_counts)

    if not inplace:
        return adata


def print_qc_summary(adata, label=''):
    """
    Print summary statistics for QC metrics.

    Parameters
    ----------
    adata : AnnData
        Annotated data matrix with QC metrics
    label : str
        Label to prepend to output (e.g., 'Before filtering', 'After filtering')
    """
    if label:
        print(f"\n{label}:")
    print(f"  Cells: {adata.n_obs}")
    print(f"  Genes: {adata.n_vars}")

    if 'total_counts' in adata.obs:
        print(f"  Mean counts per cell: {adata.obs['total_counts'].mean():.0f}")
        print(f"  Median counts per cell: {adata.obs['total_counts'].median():.0f}")

    if 'n_genes_by_counts' in adata.obs:
        print(f"  Mean genes per cell: {adata.obs['n_genes_by_counts'].mean():.0f}")
        print(f"  Median genes per cell: {adata.obs['n_genes_by_counts'].median():.0f}")

    if 'pct_counts_mt' in adata.obs:
        print(f"  Mean mitochondrial %: {adata.obs['pct_counts_mt'].mean():.2f}%")

    if 'pct_counts_ribo' in adata.obs:
        print(f"  Mean ribosomal %: {adata.obs['pct_counts_ribo'].mean():.2f}%")

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
