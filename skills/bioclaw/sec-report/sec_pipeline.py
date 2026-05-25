#!/usr/bin/env python3
"""
SEC Chromatography Analysis Pipeline
=====================================
Analyzes SEC data files and images, generates annotated figures and PDF report.

Usage:
    python sec_pipeline.py --input /path/to/data_dir --output /path/to/output_dir
    python sec_pipeline.py --input /path/to/file.zip --output /path/to/output_dir

Input: Directory or ZIP containing:
    - SEC data files (CSV/TSV/XLSX with elution volume and absorbance)
    - SEC chromatogram images (PNG/JPG)

Output:
    - Annotated chromatogram figures (per construct)
    - Comparison overlay plot
    - Quality ranking chart
    - Comprehensive PDF report
    - Machine-readable JSON summary
"""

import os
import sys
import zipfile
import argparse
import json
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Tuple, Dict

import numpy as np
import pandas as pd
from scipy.signal import find_peaks, peak_widths, savgol_filter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Compat: numpy >=2.0 renamed trapz → trapezoid
_trapz = getattr(np, 'trapezoid', None) or np.trapz


# ─── Constants ──────────────────────────────────────────────────────────────────

CHAIN_A_AA = 481
CHAIN_B_AA = 243
AVG_DA_PER_AA = 110
CHAIN_A_MW = CHAIN_A_AA * AVG_DA_PER_AA / 1000  # ~52.9 kDa
CHAIN_B_MW = CHAIN_B_AA * AVG_DA_PER_AA / 1000  # ~26.7 kDa
HETERODIMER_MW = CHAIN_A_MW + CHAIN_B_MW         # ~79.6 kDa

DEFAULT_VOID_VOLUME = 8.0   # mL, typical Superdex 200 10/300 GL
DEFAULT_TOTAL_VOLUME = 24.0 # mL

DATA_EXTENSIONS = {'.csv', '.tsv', '.txt', '.xlsx', '.xls'}
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp', '.gif'}

REPORT_PROFILE_CHOICES = ('full', 'compact')
RENDERER_CHOICES = ('auto', 'typst', 'fpdf2')
DEFAULT_REPORT_PROFILE = 'compact'
DEFAULT_RENDERER = 'auto'


# ─── Data Classes ───────────────────────────────────────────────────────────────

@dataclass
class SECPeak:
    """A detected SEC peak."""
    peak_number: int
    elution_volume: float     # mL
    height: float             # mAU
    fwhm: float               # mL
    area: float               # mAU*mL
    relative_area_pct: float  # % of total
    classification: str       # aggregate/large_oligomer/oligomer/dimer/monomer/small_molecule
    confidence: str = "medium"


@dataclass
class ConstructResult:
    """Analysis result for one SEC construct."""
    name: str
    data_file: str
    n_data_points: int
    peaks: List[SECPeak]
    quality_score: float       # 0–10
    homogeneity: str           # monodisperse / predominantly_monodisperse / heterogeneous / polydisperse
    has_aggregation: bool
    aggregation_pct: float
    dominant_species: str
    notes: List[str]
    figure_path: Optional[str] = None
    original_image_path: Optional[str] = None
    cohort: str = "primary"
    cohort_year: Optional[int] = None

    # runtime-only, not serialized
    _volumes: Optional[object] = field(default=None, repr=False)
    _absorbance: Optional[object] = field(default=None, repr=False)

    def to_dict(self):
        d = {
            'name': self.name,
            'data_file': self.data_file,
            'n_data_points': self.n_data_points,
            'quality_score': round(self.quality_score, 2),
            'homogeneity': self.homogeneity,
            'has_aggregation': self.has_aggregation,
            'aggregation_pct': round(self.aggregation_pct, 1),
            'dominant_species': self.dominant_species,
            'cohort': self.cohort,
            'cohort_year': self.cohort_year,
            'notes': self.notes,
            'peaks': [
                {
                    'peak_number': p.peak_number,
                    'elution_volume_mL': round(p.elution_volume, 3),
                    'height_mAU': round(p.height, 2),
                    'fwhm_mL': round(p.fwhm, 3),
                    'relative_area_pct': round(p.relative_area_pct, 1),
                    'classification': p.classification,
                    'confidence': p.confidence,
                }
                for p in self.peaks
            ],
        }
        return d


@dataclass
class ReportBuildResult:
    """Metadata about the generated SEC report artifact."""
    pdf_path: str
    renderer: str
    report_profile: str
    requested_renderer: str
    fallback_used: bool = False
    fallback_reason: Optional[str] = None
    appendix_path: Optional[str] = None


# ─── Data Parser ────────────────────────────────────────────────────────────────

class SECDataParser:
    """Parse SEC chromatogram data from CSV/TSV/XLSX."""

    _VOL_PAT = [r'vol', r'\bml\b', r'elution', r'retention', r'\bve\b', r'\bvr\b']
    _ABS_PAT = [r'abs', r'mau', r'\buv\b', r'a280', r'280\s*nm', r'signal', r'intensity', r'\bod\b']

    # Encodings to try in order — UTF-16 (BOM) is common for ÄKTA/UNICORN exports
    _ENCODINGS = ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'latin-1']

    @classmethod
    def parse(cls, filepath: str) -> Tuple[np.ndarray, np.ndarray, str]:
        """Return (volumes, absorbance, detector_label)."""
        ext = Path(filepath).suffix.lower()
        try:
            if ext in ('.xlsx', '.xls'):
                df = pd.read_excel(filepath)
            else:
                df = cls._read_text_file(filepath, ext)
        except Exception as e:
            raise ValueError(f"Cannot read {filepath}: {e}")

        # Drop fully-empty rows/columns that ÄKTA exports often include
        df = df.dropna(how='all').dropna(axis=1, how='all')

        df.columns = [str(c).strip() for c in df.columns]

        vol_col = cls._match_column(df.columns, cls._VOL_PAT)
        abs_col = cls._match_column(df.columns, cls._ABS_PAT)

        # Fallback: first two numeric columns
        numerics = df.select_dtypes(include=[np.number]).columns.tolist()
        if vol_col is None and len(numerics) >= 2:
            vol_col = numerics[0]
        if abs_col is None:
            remaining = [c for c in numerics if c != vol_col]
            if remaining:
                abs_col = remaining[0]

        if vol_col is None or abs_col is None:
            raise ValueError(f"Cannot identify volume/absorbance columns in {filepath}. "
                             f"Columns found: {list(df.columns)}")

        v = pd.to_numeric(df[vol_col], errors='coerce').dropna().values.astype(float)
        a = pd.to_numeric(df[abs_col], errors='coerce').dropna().values.astype(float)
        n = min(len(v), len(a))
        return v[:n], a[:n], str(abs_col)

    @classmethod
    def _read_text_file(cls, filepath: str, ext: str) -> pd.DataFrame:
        """Try multiple encodings and separators to read a text data file.

        Handles ÄKTA / UNICORN exports which are typically:
          - UTF-16 LE with BOM
          - Tab-separated
          - 3 header rows (instrument, detector, units) before numeric data
        """
        last_err = None
        for enc in cls._ENCODINGS:
            try:
                # --- Attempt 1: ÄKTA multi-header format ---
                # Read raw lines, look for the row that contains "ml" and "mAU"
                # (the units row), use it as header, skip everything above
                with open(filepath, encoding=enc) as fh:
                    lines = fh.readlines()

                header_idx = cls._find_akta_header(lines)
                if header_idx is not None:
                    df = pd.read_csv(
                        filepath, sep='\t', encoding=enc,
                        skiprows=header_idx, header=0,
                        on_bad_lines='skip',
                    )
                    # ÄKTA files interleave multiple detector columns; keep only
                    # the first ml + mAU pair (UV trace)
                    df = cls._extract_uv_pair(df)
                    if df is not None and len(df.columns) >= 2:
                        return df

                # --- Attempt 2: standard CSV/TSV with single header row ---
                if ext == '.csv':
                    df = pd.read_csv(filepath, encoding=enc, comment='#')
                    if len(df.columns) >= 2:
                        return df
                df = pd.read_csv(filepath, sep='\t', encoding=enc, comment='#')
                if len(df.columns) >= 2:
                    return df
                df = pd.read_csv(filepath, sep=None, engine='python',
                                 encoding=enc, comment='#')
                if len(df.columns) >= 2:
                    return df
            except Exception as e:
                last_err = e
                continue
        raise ValueError(str(last_err) if last_err else "No valid encoding found")

    @staticmethod
    def _find_akta_header(lines: list) -> Optional[int]:
        """Find the ÄKTA units header row (contains 'ml' and 'mAU' or 'mS/cm')."""
        for i, line in enumerate(lines[:10]):
            low = line.lower()
            if '\tml\t' in f'\t{low}\t' or low.startswith('ml\t') or low.startswith('ml,'):
                if 'mau' in low or 'ms/cm' in low or 'mau' in low:
                    return i
        return None

    @staticmethod
    def _extract_uv_pair(df: pd.DataFrame) -> Optional[pd.DataFrame]:
        """From an ÄKTA multi-detector dataframe, extract the first (ml, mAU) pair.

        ÄKTA exports repeat 'ml' for each detector. We want the UV column
        which is typically the first pair: col0=ml, col1=mAU.
        """
        if df is None or len(df.columns) < 2:
            return None
        cols = [str(c).strip().lower() for c in df.columns]
        # Find the first 'ml' column and the first 'mau' column
        ml_idx = None
        mau_idx = None
        for i, c in enumerate(cols):
            if c == 'ml' and ml_idx is None:
                ml_idx = i
            if c == 'mau' and mau_idx is None:
                mau_idx = i
        if ml_idx is not None and mau_idx is not None:
            result = df.iloc[:, [ml_idx, mau_idx]].copy()
            result.columns = ['ml', 'mAU']
            return result
        return None

    @staticmethod
    def _match_column(columns, patterns):
        for col in columns:
            low = str(col).lower()
            for pat in patterns:
                if re.search(pat, low):
                    return col
        return None


# ─── Peak Analyzer ──────────────────────────────────────────────────────────────

class SECPeakAnalyzer:
    """Detect and classify peaks in SEC chromatograms."""

    def __init__(self, void_volume: float = DEFAULT_VOID_VOLUME):
        self.v0 = void_volume

    def detect(self, volumes: np.ndarray, absorbance: np.ndarray,
               min_height_frac: float = 0.05,
               min_distance_ml: float = 0.5,
               prominence_frac: float = 0.03) -> List[SECPeak]:
        """Detect and classify peaks."""

        # Smooth
        smoothed = self._smooth(absorbance)
        amax = np.max(smoothed)
        if amax <= 0:
            return []

        # Spacing
        spacing = np.mean(np.diff(volumes)) if len(volumes) > 1 else 1.0
        min_dist_pts = max(1, int(min_distance_ml / spacing))

        indices, props = find_peaks(
            smoothed,
            height=amax * min_height_frac,
            distance=min_dist_pts,
            prominence=amax * prominence_frac,
            width=1,
        )
        if len(indices) == 0:
            return []

        widths_pts, wh, left_ips, right_ips = peak_widths(smoothed, indices, rel_height=0.5)

        # ── Non-overlapping area partitioning ──
        # Assign each data point to the nearest peak (valley-based split).
        # This ensures area percentages sum to ~100%.
        n_pts = len(volumes)
        boundaries = [0]  # start of first region
        for j in range(len(indices) - 1):
            # Find the valley (minimum) between consecutive peaks
            valley_region = smoothed[indices[j]:indices[j + 1] + 1]
            valley_idx = indices[j] + int(np.argmin(valley_region))
            boundaries.append(valley_idx)
        boundaries.append(n_pts - 1)  # end of last region

        total_area = _trapz(np.maximum(smoothed, 0), volumes)

        peaks = []
        for i, idx in enumerate(indices):
            fwhm_ml = widths_pts[i] * spacing

            # Area from valley to valley (non-overlapping)
            li = boundaries[i]
            ri = boundaries[i + 1]
            seg = np.maximum(smoothed[li:ri + 1], 0)
            area = _trapz(seg, volumes[li:ri + 1])
            rel = (area / total_area * 100) if total_area > 0 else 0

            cls_label, conf = self._classify(volumes[idx])

            peaks.append(SECPeak(
                peak_number=i + 1,
                elution_volume=float(volumes[idx]),
                height=float(smoothed[idx]),
                fwhm=float(fwhm_ml),
                area=float(area),
                relative_area_pct=float(rel),
                classification=cls_label,
                confidence=conf,
            ))

        return peaks

    def assess(self, peaks: List[SECPeak]) -> Tuple[float, str, bool, float, str]:
        """Return (quality_score, homogeneity, has_agg, agg_pct, dominant_species)."""
        if not peaks:
            return 0.0, "no_signal", False, 0.0, "none"

        has_agg = any(p.classification == "aggregate" for p in peaks)
        agg_pct = sum(p.relative_area_pct for p in peaks if p.classification == "aggregate")
        dominant = max(peaks, key=lambda p: p.relative_area_pct)

        # Homogeneity
        if len(peaks) == 1:
            hom = "monodisperse"
        elif dominant.relative_area_pct > 80:
            hom = "predominantly_monodisperse"
        elif dominant.relative_area_pct > 60:
            hom = "heterogeneous"
        else:
            hom = "polydisperse"

        # Score
        score = 10.0
        score -= min(3.0, agg_pct * 0.1)

        # Penalize when the dominant species is aggregate or no useful signal
        if dominant.classification == "aggregate":
            score -= 4.0   # aggregate-dominant is a bad sign, never high-quality
        elif dominant.classification == "small_molecule":
            score -= 1.5   # small molecule dominant is usually not the target

        if hom == "polydisperse":
            score -= 3.0
        elif hom == "heterogeneous":
            score -= 1.5
        elif hom == "predominantly_monodisperse":
            score -= 0.5

        for p in peaks:
            if p.fwhm > 3.0:
                score -= 1.0
            elif p.fwhm > 2.0:
                score -= 0.5

        if dominant.fwhm < 1.5 and dominant.relative_area_pct > 70:
            score += 1.0

        score = max(0.0, min(10.0, score))

        return score, hom, has_agg, agg_pct, dominant.classification

    # ── helpers ──

    def _classify(self, ve: float) -> Tuple[str, str]:
        delta = ve - self.v0
        if delta <= 0.5:
            return "aggregate", "high"
        elif delta <= 2.5:
            return "large_oligomer", "medium"
        elif delta <= 4.5:
            return "oligomer", "medium"
        elif delta <= 6.5:
            return "dimer", "medium"
        elif delta <= 9.0:
            return "monomer", "medium"
        else:
            return "small_molecule", "low"

    @staticmethod
    def _smooth(y: np.ndarray) -> np.ndarray:
        if len(y) < 20:
            return y.copy()
        win = min(15, len(y) // 4 * 2 + 1)
        if win < 5:
            return y.copy()
        return savgol_filter(y, win, 3)


# ─── Plotter ────────────────────────────────────────────────────────────────────

class SECPlotter:
    """Publication-quality SEC chromatogram figures."""

    PEAK_COLORS = {
        'aggregate':      '#d62728',
        'large_oligomer':  '#ff7f0e',
        'oligomer':       '#2ca02c',
        'dimer':          '#1f77b4',
        'monomer':        '#9467bd',
        'small_molecule': '#8c564b',
        'unknown':        '#7f7f7f',
    }
    NICE_LABELS = {
        'aggregate':      'Aggregate',
        'large_oligomer':  'Large Oligomer',
        'oligomer':       'Oligomer',
        'dimer':          'Dimer',
        'monomer':        'Monomer',
        'small_molecule': 'Small Mol.',
        'unknown':        'Unknown',
    }

    def __init__(self, void_volume: float = DEFAULT_VOID_VOLUME):
        self.v0 = void_volume
        self._apply_style()

    @staticmethod
    def _apply_style():
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
            'font.size': 10,
            'axes.labelsize': 12,
            'axes.titlesize': 13,
            'xtick.labelsize': 9,
            'ytick.labelsize': 9,
            'legend.fontsize': 9,
            'figure.dpi': 300,
            'savefig.dpi': 300,
            'savefig.bbox': 'tight',
            'axes.linewidth': 1.0,
            'axes.spines.top': False,
            'axes.spines.right': False,
        })

    def plot_chromatogram(self, result: ConstructResult, outpath: str):
        """Annotated SEC chromatogram for one construct."""
        fig, ax = plt.subplots(figsize=(8, 4.5))

        vol = result._volumes
        abso = result._absorbance
        ax.plot(vol, abso, 'k-', lw=1.2, alpha=0.85)
        ax.fill_between(vol, abso, alpha=0.04, color='gray')

        # Annotate peaks — only label peaks with ≥2% area to avoid clutter;
        # stagger vertical offsets to reduce label overlap.
        major_peaks = [pk for pk in result.peaks if pk.relative_area_pct >= 2.0]
        # Sort by elution volume for left-to-right offset alternation
        major_peaks.sort(key=lambda p: p.elution_volume)
        for pi, pk in enumerate(major_peaks):
            c = self.PEAK_COLORS.get(pk.classification, '#7f7f7f')
            lab = self.NICE_LABELS.get(pk.classification, pk.classification)
            ax.plot(pk.elution_volume, pk.height, 'v', color=c, ms=8, zorder=5)
            txt = f"{lab}\n{pk.elution_volume:.1f} mL ({pk.relative_area_pct:.0f}%)"
            # Alternate y-offset to reduce overlap between adjacent labels
            y_off = 18 + (pi % 3) * 14
            ax.annotate(txt, xy=(pk.elution_volume, pk.height),
                        xytext=(0, y_off), textcoords='offset points',
                        ha='center', va='bottom', fontsize=7, color=c, fontweight='bold',
                        arrowprops=dict(arrowstyle='-', color=c, alpha=0.4, lw=0.8),
                        bbox=dict(boxstyle='round,pad=0.2', fc='white', ec=c, alpha=0.85))
        # Show minor peaks as markers only (no label)
        for pk in result.peaks:
            if pk.relative_area_pct < 2.0:
                c = self.PEAK_COLORS.get(pk.classification, '#7f7f7f')
                ax.plot(pk.elution_volume, pk.height, 'v', color=c, ms=5, alpha=0.5, zorder=4)

        # Void volume marker
        ax.axvline(self.v0, color='red', ls='--', alpha=0.3, lw=0.8)
        ymax = ax.get_ylim()[1]
        ax.text(self.v0 + 0.15, ymax * 0.95, 'V\u2080', color='red', alpha=0.5, fontsize=8, va='top')

        ax.set_xlabel('Elution Volume (mL)')
        ax.set_ylabel('Absorbance (mAU)')
        ax.set_title(result.name, fontweight='bold', pad=10)

        # Quality badge
        qs = result.quality_score
        qc = '#2ca02c' if qs >= 7 else '#ff7f0e' if qs >= 4 else '#d62728'
        ax.text(0.98, 0.95, f'Quality: {qs:.1f}/10', transform=ax.transAxes,
                ha='right', va='top', fontsize=9, fontweight='bold', color=qc,
                bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=qc, alpha=0.85))

        plt.tight_layout()
        fig.savefig(outpath, dpi=300)
        plt.close(fig)

    # Zone definitions for shading
    ZONE_DEFS = [
        ('Void/Aggregate', 0.0, 0.0, '#d62728', 0.06),
        ('Very Large (HMW)', 0.0, 2.5, '#ff7f0e', 0.06),
        ('Large Oligomer', 2.5, 4.5, '#2ca02c', 0.06),
        ('Mid-size', 4.5, 6.5, '#1f77b4', 0.06),
        ('Small/Monomer', 6.5, 12.0, '#9467bd', 0.06),
    ]

    def _add_zone_shading(self, ax, ymax: float = 1.1):
        """Add colored zone shading to an axis."""
        short_labels = ['Void', 'HMW', 'Oligomer', 'Mid', 'Monomer']
        for (label, off_lo, off_hi, color, alpha), slabel in zip(self.ZONE_DEFS, short_labels):
            lo = self.v0 + off_lo if off_lo > 0 else 0
            hi = self.v0 + off_hi
            ax.axvspan(lo, hi, alpha=alpha, color=color, zorder=0)
            mid = (lo + hi) / 2
            ax.text(mid, ymax * 0.97, slabel, ha='center', va='top',
                    fontsize=6, color=color, alpha=0.6, fontstyle='italic')

    def plot_comparison(self, results: List[ConstructResult], outpath: str):
        """Overlay normalized chromatograms with zone shading."""
        fig, ax = plt.subplots(figsize=(10, 5.5))
        cmap = plt.cm.tab10(np.linspace(0, 1, min(10, len(results))))

        # Zone shading
        self._add_zone_shading(ax, ymax=1.1)

        for i, r in enumerate(results):
            mx = np.max(r._absorbance) if np.max(r._absorbance) > 0 else 1
            short = self._short_name(r.name, maxlen=28)
            ax.plot(r._volumes, r._absorbance / mx, lw=1.3, alpha=0.8,
                    color=cmap[i % len(cmap)],
                    label=f'{short} (Q={r.quality_score:.1f})')

        ax.axvline(self.v0, color='red', ls='--', alpha=0.3, lw=0.8)
        ax.set_xlabel('Elution Volume (mL)')
        ax.set_ylabel('Normalized UV Absorbance (A.U.)')
        ax.set_title('SEC Overlay: All Constructs (normalized, aligned)',
                      fontweight='bold', fontsize=11)
        ax.legend(loc='upper right', framealpha=0.92, fontsize=6,
                  edgecolor='#cccccc', ncol=1)
        ax.set_ylim(-0.02, 1.12)
        plt.tight_layout()
        fig.savefig(outpath, dpi=300)
        plt.close(fig)

    @staticmethod
    def _short_name(name: str, maxlen: int = 22) -> str:
        """Truncate long construct names for chart labels."""
        # Remove common suffixes
        s = name.replace(' 001', '').replace('_001', '').strip()
        if len(s) <= maxlen:
            return s
        return s[:maxlen - 1] + '…'

    def plot_zone_fractions(self, results: List[ConstructResult], outpath: str):
        """Stacked bar chart of zone fractions per construct (Biomni-style)."""
        zone_names = ['Void/Aggregate', 'Very Large (HMW)', 'Large Oligomer',
                      'Mid-size', 'Small/Monomer']
        zone_class = ['aggregate', 'large_oligomer', 'oligomer', 'dimer', 'monomer']
        zone_colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd']

        sr = sorted(results, key=lambda r: min(
            (p.elution_volume for p in r.peaks), default=20))

        names = [self._short_name(r.name) for r in sr]
        fractions = {z: [] for z in zone_class}

        for r in sr:
            total_area = sum(p.area for p in r.peaks) or 1
            for zc in zone_class:
                area = sum(p.area for p in r.peaks if p.classification == zc)
                fractions[zc].append(area / total_area)

        fig, ax = plt.subplots(figsize=(max(8, len(names) * 0.6 + 2), 5.5))
        x = np.arange(len(names))
        bottoms = np.zeros(len(names))

        for zn, zc, zcolor in zip(zone_names, zone_class, zone_colors):
            vals = np.array(fractions[zc])
            ax.bar(x, vals, bottom=bottoms, label=zn, color=zcolor, alpha=0.85,
                   edgecolor='white', linewidth=0.5)
            bottoms += vals

        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=55, ha='right', fontsize=6.5)
        ax.set_ylabel('Fraction of Total Peak Area')
        ax.set_title('Zone Fraction Breakdown per Construct',
                      fontweight='bold', fontsize=11)
        ax.legend(loc='upper right', fontsize=7, title='Elution Zone',
                  title_fontsize=7.5, framealpha=0.92, edgecolor='#cccccc')
        ax.set_ylim(0, 1.05)
        plt.tight_layout()
        fig.savefig(outpath, dpi=300)
        plt.close(fig)

    def plot_grid(self, results: List[ConstructResult], outpath: str,
                  max_cols: int = 4, title: str = "Individual SEC Chromatograms"):
        """Multi-panel grid of individual chromatograms (Biomni Figure 2 style)."""
        n = len(results)
        if n == 0:
            return
        cols = min(max_cols, n)
        rows = (n + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(4.4 * cols, 3.1 * rows),
                                  squeeze=False)

        zone_colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd']
        zone_offs = [(0.0, 0.0), (0.0, 2.5), (2.5, 4.5), (4.5, 6.5), (6.5, 12.0)]

        for idx, r in enumerate(results):
            row_i, col_i = divmod(idx, cols)
            ax = axes[row_i][col_i]

            mx = np.max(r._absorbance) if np.max(r._absorbance) > 0 else 1
            normed = r._absorbance / mx

            # Zone shading
            for (off_lo, off_hi), zc in zip(zone_offs, zone_colors):
                lo = self.v0 + off_lo if off_lo > 0 else 0
                hi = self.v0 + off_hi
                ax.axvspan(lo, hi, alpha=0.06, color=zc, zorder=0)

            ax.plot(r._volumes, normed, lw=1.0, alpha=0.85, color='#2c3e50')
            ax.fill_between(r._volumes, normed, alpha=0.04, color='#2c3e50')

            # Dominant peak marker
            dom = max(r.peaks, key=lambda p: p.relative_area_pct, default=None)
            if dom:
                dom_y = dom.height / mx if mx > 0 else 0
                c = self.PEAK_COLORS.get(dom.classification, '#7f7f7f')
                ax.axvline(dom.elution_volume, color=c, ls='--', alpha=0.5, lw=0.8)

            ax.set_title(r.name, fontsize=7, fontweight='bold', pad=3)
            ax.set_ylim(-0.02, 1.12)
            ax.tick_params(labelsize=6)
            if row_i == rows - 1:
                ax.set_xlabel('mL', fontsize=7)
            if col_i == 0:
                ax.set_ylabel('Norm. UV', fontsize=7)

        # Hide unused subplots
        for idx in range(n, rows * cols):
            row_i, col_i = divmod(idx, cols)
            axes[row_i][col_i].set_visible(False)

        fig.suptitle(title, fontsize=11, fontweight='bold', y=1.0)
        plt.tight_layout()
        fig.savefig(outpath, dpi=250)
        plt.close(fig)

    def plot_ranking(self, results: List[ConstructResult], outpath: str):
        """Horizontal bar chart ranking constructs by quality."""
        sr = sorted(results, key=lambda r: r.quality_score, reverse=True)
        fig, ax = plt.subplots(figsize=(9.2, max(3, len(sr) * 0.42 + 0.8)))

        names = [self._short_name(r.name, maxlen=28) for r in sr]
        scores = [r.quality_score for r in sr]
        colors = ['#2ca02c' if s >= 7 else '#ff7f0e' if s >= 4 else '#d62728' for s in scores]

        bars = ax.barh(range(len(names)), scores, color=colors, alpha=0.85, edgecolor='white')
        ax.set_yticks(range(len(names)))
        ax.set_yticklabels(names, fontsize=8)
        ax.set_xlabel('Quality Score (0–10)')
        ax.set_title('Construct Ranking by SEC Profile Quality', fontweight='bold')
        ax.set_xlim(0, 10.5)
        ax.invert_yaxis()

        for bar, sc in zip(bars, scores):
            ax.text(sc + 0.15, bar.get_y() + bar.get_height() / 2,
                    f'{sc:.1f}', va='center', fontsize=8.5, fontweight='bold')

        plt.tight_layout()
        fig.savefig(outpath, dpi=300)
        plt.close(fig)


# ─── Helpers ────────────────────────────────────────────────────────────────────

def extract_zip(zip_path: str, dest: str) -> str:
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(dest)
    return dest


# Filename patterns that are NOT individual SEC chromatograms
_SKIP_STEMS = re.compile(
    r'(?i)'
    r'(^calibration)'               # calibration standards
    r'|(_CAL\d)'                     # e.g. S6_CAL29_700kDa
    r'|(all_peak_metrics)'           # summary tables
    r'|(combined_)'                  # combined/stacked tables
    r'|(^secprocess)'                # processing scripts (sometimes .txt)
    r'|(__pycache__)'                # Python cache artefacts
)


def discover_files(root: str) -> Tuple[List[str], List[str]]:
    """Walk tree, return (data_files, image_files) sorted.

    Applies three filters:
      1. Skip hidden/temp files
      2. Skip known non-chromatogram files (calibration, summary tables, etc.)
      3. Deduplicate: if the same sample appears as both raw and *_normalized_curve,
         keep only the raw file.  If the same sample appears in multiple directories,
         keep the first one found (alphabetical walk order).
    """
    raw_data: Dict[str, str] = {}   # stem -> path  (raw chromatograms)
    norm_data: Dict[str, str] = {}  # stem -> path  (normalized curves)
    imgs: List[str] = []

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip __pycache__ and __MACOSX entirely
        dirnames[:] = [d for d in dirnames if d not in ('__pycache__', '__MACOSX')]
        for fn in sorted(filenames):
            if fn.startswith('.') or fn.startswith('~'):
                continue
            stem = Path(fn).stem
            ext = Path(fn).suffix.lower()
            full = os.path.join(dirpath, fn)

            if ext in IMAGE_EXTENSIONS:
                imgs.append(full)
                continue

            if ext not in DATA_EXTENSIONS:
                continue

            # Skip known non-chromatogram files
            if _SKIP_STEMS.search(stem):
                continue

            # Separate raw vs normalized; deduplicate by a canonical key
            is_norm = '_normalized_curve' in stem
            if is_norm:
                canon = stem.replace('_normalized_curve', '')
                if canon not in norm_data:
                    norm_data[canon] = full
            else:
                canon = re.sub(r'[\s_-]+', '_', stem).lower()
                if canon not in raw_data:
                    raw_data[canon] = full

    # Prefer raw data; only fall back to normalized curves when NO raw files exist
    if raw_data:
        final_data = list(raw_data.values())
        n_skipped = len(norm_data)
        if n_skipped:
            print(f"      [filter] {len(raw_data)} raw files found; "
                  f"skipping {n_skipped} normalized-curve derivatives")
    else:
        # No raw files parsed — use normalized curves, deduplicated
        final_data = list(norm_data.values())
        print(f"      [filter] No raw data files; using {len(final_data)} "
              f"normalized-curve files")

    final_data.sort()
    imgs.sort()
    return final_data, imgs


def match_image(construct_name: str, images: List[str]) -> Optional[str]:
    """Fuzzy-match an image file to a construct name."""
    name_low = construct_name.lower()
    for img in images:
        stem = Path(img).stem.lower()
        if name_low in stem or stem in name_low:
            return img
    # try partial
    for img in images:
        stem = Path(img).stem.lower()
        tokens = re.split(r'[_\-\s.]+', name_low)
        if any(t in stem for t in tokens if len(t) > 2):
            return img
    return None


def _normalize_report_profile(report_profile: str) -> str:
    profile = (report_profile or DEFAULT_REPORT_PROFILE).strip().lower()
    if profile not in REPORT_PROFILE_CHOICES:
        raise ValueError(
            f"Unsupported report profile '{report_profile}'. "
            f"Choose from: {', '.join(REPORT_PROFILE_CHOICES)}"
        )
    return profile


def _normalize_renderer(renderer: str) -> str:
    mode = (renderer or DEFAULT_RENDERER).strip().lower()
    if mode not in RENDERER_CHOICES:
        raise ValueError(
            f"Unsupported renderer '{renderer}'. "
            f"Choose from: {', '.join(RENDERER_CHOICES)}"
        )
    return mode


def _build_sec_report(
    results: List[ConstructResult],
    image_files: List[str],
    figs_dir: str,
    output_dir: str,
    void_volume: float,
    report_profile: str,
    renderer: str,
) -> ReportBuildResult:
    """Build the SEC PDF report and capture renderer metadata."""
    report_profile = _normalize_report_profile(report_profile)
    renderer = _normalize_renderer(renderer)

    pdf_path = os.path.join(output_dir, 'SEC_Analysis_Report.pdf')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    print(f"      Report profile   : {report_profile}")
    print(f"      Renderer mode    : {renderer}")

    if renderer == 'fpdf2':
        from sec_report_pdf import SECReportPDF
        report = SECReportPDF(void_volume=void_volume, report_profile=report_profile)
        report.build(results, image_files, figs_dir, pdf_path)
        print(f"      → {pdf_path} (fpdf2)")
        return ReportBuildResult(
            pdf_path=pdf_path,
            renderer='fpdf2',
            report_profile=report_profile,
            requested_renderer=renderer,
        )

    try:
        from sec_report_typst import build_typst_report
        build_typst_report(
            results,
            image_files,
            figs_dir,
            pdf_path,
            void_volume=void_volume,
            report_profile=report_profile,
        )
        print(f"      → {pdf_path} (Typst)")
        return ReportBuildResult(
            pdf_path=pdf_path,
            renderer='typst',
            report_profile=report_profile,
            requested_renderer=renderer,
        )
    except Exception as e:
        reason = f"{type(e).__name__}: {e}"
        print(f"      Typst renderer unavailable ({reason})")
        if renderer == 'typst':
            raise RuntimeError(
                "Typst renderer was required but could not be used. "
                f"Reason: {reason}"
            ) from e

        print("      Falling back to fpdf2 renderer …")
        from sec_report_pdf import SECReportPDF
        report = SECReportPDF(void_volume=void_volume, report_profile=report_profile)
        report.build(results, image_files, figs_dir, pdf_path)
        print(f"      → {pdf_path} (fpdf2 fallback)")
        return ReportBuildResult(
            pdf_path=pdf_path,
            renderer='fpdf2',
            report_profile=report_profile,
            requested_renderer=renderer,
            fallback_used=True,
            fallback_reason=reason,
        )


def _build_sec_appendix(
    results: List[ConstructResult],
    image_files: List[str],
    figs_dir: str,
    output_path: str,
    void_volume: float,
    renderer: str,
) -> str:
    """Generate the appendix PDF with exhaustive per-construct detail."""
    renderer = _normalize_renderer(renderer)

    if renderer == 'fpdf2':
        from sec_report_pdf import SECReportPDF
        report = SECReportPDF(void_volume=void_volume, report_profile='full')
        report.build_appendix(results, image_files, figs_dir, output_path)
        return output_path

    try:
        from sec_report_typst import build_typst_appendix
        build_typst_appendix(results, image_files, figs_dir, output_path,
                             void_volume=void_volume)
        return output_path
    except Exception:
        from sec_report_pdf import SECReportPDF
        report = SECReportPDF(void_volume=void_volume, report_profile='full')
        report.build_appendix(results, image_files, figs_dir, output_path)
        return output_path


# ─── Main Pipeline ──────────────────────────────────────────────────────────────

def run_pipeline(input_path: str, output_dir: str,
                 void_volume: float = DEFAULT_VOID_VOLUME,
                 report_profile: str = DEFAULT_REPORT_PROFILE,
                 renderer: str = DEFAULT_RENDERER) -> str:
    """
    Full SEC analysis pipeline.

    Args:
        input_path: Directory with SEC files, or a .zip archive.
        output_dir: Where to write figures and PDF.
        void_volume: Column void volume in mL.
        report_profile: Report verbosity/profile selector.
        renderer: Renderer mode: auto, typst, or fpdf2.

    Returns:
        Path to generated PDF report.
    """
    os.makedirs(output_dir, exist_ok=True)
    figs_dir = os.path.join(output_dir, 'figures')
    os.makedirs(figs_dir, exist_ok=True)

    # ── 1. Input resolution ─────────────────────────────────────────────────
    print("=" * 64)
    print("  SEC Analysis Pipeline")
    print("=" * 64)

    data_root = input_path
    if os.path.isfile(input_path) and input_path.lower().endswith('.zip'):
        print(f"\n[1/5] Extracting ZIP …")
        data_root = os.path.join(output_dir, '_extracted')
        extract_zip(input_path, data_root)
    else:
        print(f"\n[1/5] Reading input directory …")

    data_files, image_files = discover_files(data_root)
    print(f"      Data files  : {len(data_files)}")
    print(f"      Image files : {len(image_files)}")

    if not data_files:
        print("\n  ERROR  No SEC data files found.")
        print("         Supported: .csv .tsv .txt .xlsx .xls")
        sys.exit(1)

    # ── 2. Per-construct analysis ────────────────────────────────────────────
    print(f"\n[2/5] Analyzing constructs …")
    analyzer = SECPeakAnalyzer(void_volume)
    plotter = SECPlotter(void_volume)
    results: List[ConstructResult] = []

    for i, df_path in enumerate(data_files):
        name = Path(df_path).stem
        print(f"      [{i + 1}/{len(data_files)}] {name}")

        try:
            volumes, absorbance, detector = SECDataParser.parse(df_path)
        except Exception as e:
            print(f"          SKIP – parse error: {e}")
            continue

        if len(volumes) < 10:
            print(f"          SKIP – too few data points ({len(volumes)})")
            continue

        # Clip to SEC separation range: ÄKTA raw exports may include
        # equilibration, wash, and CIP phases far beyond the column volume.
        # Keep only [0, total_volume * 1.2] — anything beyond is not SEC.
        max_vol = DEFAULT_TOTAL_VOLUME * 1.2   # ~28.8 mL for a 24 mL column
        mask = (volumes >= 0) & (volumes <= max_vol)
        if mask.sum() < 10:
            print(f"          SKIP – too few data points in SEC range "
                  f"(0–{max_vol:.0f} mL)")
            continue
        volumes = volumes[mask]
        absorbance = absorbance[mask]

        peaks = analyzer.detect(volumes, absorbance)
        score, hom, has_agg, agg_pct, dominant = analyzer.assess(peaks)

        notes: List[str] = []
        if has_agg:
            notes.append(f"Aggregation detected ({agg_pct:.0f}% of total area)")
        if hom == "polydisperse":
            notes.append("Polydisperse — multiple species present")
        if any(p.fwhm > 2.5 for p in peaks):
            notes.append("Broad peak(s) — possible conformational heterogeneity")
        if dominant in ("oligomer", "large_oligomer"):
            notes.append("Higher-order oligomer dominant — promising for ring assembly")

        orig_img = match_image(name, image_files)

        cr = ConstructResult(
            name=name,
            data_file=df_path,
            n_data_points=len(volumes),
            peaks=peaks,
            quality_score=score,
            homogeneity=hom,
            has_aggregation=has_agg,
            aggregation_pct=agg_pct,
            dominant_species=dominant,
            notes=notes,
            original_image_path=orig_img,
            _volumes=volumes,
            _absorbance=absorbance,
        )

        fig_path = os.path.join(figs_dir, f'{name}_annotated.png')
        plotter.plot_chromatogram(cr, fig_path)
        cr.figure_path = fig_path

        results.append(cr)
        print(f"          → Q={score:.1f}  dominant={dominant}  peaks={len(peaks)}")

    if not results:
        print("\n  ERROR  No constructs could be analyzed.")
        sys.exit(1)

    # ── 2b. Cohort assignment ───────────────────────────────────────────────
    from sec_report_common import assign_cohorts, select_representative_constructs
    cohort_labels = assign_cohorts(results)
    if any("context" in v for v in cohort_labels.values()):
        print(f"      Cohorts detected:")
        for cname, label in cohort_labels.items():
            print(f"        {cname:30s} → {label}")
    else:
        print(f"      Cohort: all primary")

    # ── 3. Comparison figures ────────────────────────────────────────────────
    print(f"\n[3/5] Generating comparison figures …")
    if len(results) > 1:
        plotter.plot_comparison(results, os.path.join(figs_dir, 'comparison_overlay.png'))
        plotter.plot_zone_fractions(results, os.path.join(figs_dir, 'zone_fractions.png'))
        plotter.plot_grid(results, os.path.join(figs_dir, 'individual_grid.png'))
    plotter.plot_ranking(results, os.path.join(figs_dir, 'ranking_summary.png'))

    primary_results = [r for r in results if getattr(r, 'cohort', 'primary') == 'primary']
    if report_profile == 'compact':
        figure_pool = primary_results or results
        if len(figure_pool) > 1:
            plotter.plot_comparison(
                figure_pool,
                os.path.join(figs_dir, 'comparison_overlay_primary.png'),
            )
            plotter.plot_zone_fractions(
                figure_pool,
                os.path.join(figs_dir, 'zone_fractions_primary.png'),
            )
            plotter.plot_ranking(
                figure_pool,
                os.path.join(figs_dir, 'ranking_summary_primary.png'),
            )
        selected = select_representative_constructs(figure_pool, max_items=4)
        if selected:
            plotter.plot_grid(
                selected,
                os.path.join(figs_dir, 'selected_grid.png'),
                max_cols=2,
                title='Representative SEC Chromatograms',
            )

    # ── 4. PDF report ────────────────────────────────────────────────────────
    print(f"\n[4/5] Building PDF report …")

    report_build = _build_sec_report(
        results,
        image_files,
        figs_dir,
        output_dir,
        void_volume=void_volume,
        report_profile=report_profile,
        renderer=renderer,
    )
    pdf_path = report_build.pdf_path

    # ── 4b. Appendix (compact mode) ────────────────────────────────────────
    if report_profile == 'compact':
        appendix_path = os.path.join(output_dir, 'SEC_Analysis_Appendix.pdf')
        try:
            _build_sec_appendix(
                results, image_files, figs_dir, appendix_path,
                void_volume=void_volume, renderer=renderer,
            )
            report_build.appendix_path = appendix_path
            print(f"      → Appendix: {appendix_path}")
        except Exception as e:
            print(f"      Appendix generation failed: {e}")

    # ── 5. JSON summary ─────────────────────────────────────────────────────
    print(f"\n[5/5] Writing summary …")
    sr_final = sorted(results, key=lambda x: x.quality_score, reverse=True)
    selected_pool = primary_results if report_profile == 'compact' and primary_results else sr_final
    selected_names = [r.name for r in select_representative_constructs(selected_pool, max_items=4)]

    summary = {
        'generated': datetime.now().isoformat(),
        'n_constructs': len(results),
        'void_volume_mL': void_volume,
        'report_profile': report_build.report_profile,
        'renderer': report_build.renderer,
        'requested_renderer': report_build.requested_renderer,
        'fallback_used': report_build.fallback_used,
        'fallback_reason': report_build.fallback_reason,
        'appendix_path': report_build.appendix_path,
        'selected_constructs': selected_names,
        'constructs': [r.to_dict() for r in sr_final],
    }
    json_path = os.path.join(output_dir, 'analysis_summary.json')
    with open(json_path, 'w') as f:
        json.dump(summary, f, indent=2)

    # ── Done ─────────────────────────────────────────────────────────────────
    sr = sorted(results, key=lambda r: r.quality_score, reverse=True)
    print("\n" + "─" * 64)
    print("  RESULTS SUMMARY")
    print("─" * 64)
    for r in sr:
        icon = "★" if r.quality_score >= 7 else "◆" if r.quality_score >= 4 else "✗"
        print(f"  {icon}  {r.name:25s}  Q={r.quality_score:.1f}  "
              f"{r.dominant_species:18s}  {r.homogeneity}")

    top = [r for r in sr if r.quality_score >= 7]
    print(f"\n  Top candidate(s):")
    if top:
        for r in top:
            print(f"    → {r.name} (Q={r.quality_score:.1f})")
    else:
        print(f"    → {sr[0].name} (Q={sr[0].quality_score:.1f})  [best available]")

    print(f"\n  PDF report : {pdf_path}")
    if report_build.appendix_path:
        print(f"  Appendix   : {report_build.appendix_path}")
    print(f"  JSON data  : {json_path}")
    print(f"  Renderer   : {report_build.renderer} (requested={report_build.requested_renderer})")
    print(f"  Profile    : {report_build.report_profile}")
    if report_build.fallback_used and report_build.fallback_reason:
        print(f"  Fallback   : yes ({report_build.fallback_reason})")
    print("=" * 64)

    return pdf_path


# ─── CLI ────────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description='SEC Chromatography Analysis Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sec_pipeline.py -i ./sec_data/ -o ./sec_report/
  python sec_pipeline.py -i experiment.zip -o ./sec_report/
  python sec_pipeline.py -i ./data/ -o ./out/ --void-volume 7.5
  python sec_pipeline.py -i ./data/ -o ./out/ --renderer typst --report-profile compact
        """)
    ap.add_argument('-i', '--input', required=True,
                    help='Input directory or ZIP with SEC data files and images')
    ap.add_argument('-o', '--output', required=True,
                    help='Output directory for figures and PDF report')
    ap.add_argument('--void-volume', type=float, default=DEFAULT_VOID_VOLUME,
                    help=f'Column void volume in mL (default: {DEFAULT_VOID_VOLUME})')
    ap.add_argument(
        '--report-profile',
        choices=REPORT_PROFILE_CHOICES,
        default=DEFAULT_REPORT_PROFILE,
        help=(
            'Report output profile. "compact" is the default user-facing concise report; '
            '"full" preserves the exhaustive legacy-style output.'
        ),
    )
    ap.add_argument(
        '--renderer',
        choices=RENDERER_CHOICES,
        default=DEFAULT_RENDERER,
        help=(
            'Renderer mode: "auto" tries Typst first and falls back to fpdf2; '
            '"typst" requires Typst and fails if unavailable; '
            '"fpdf2" skips Typst and uses the fallback renderer directly.'
        ),
    )
    args = ap.parse_args()
    run_pipeline(
        args.input,
        args.output,
        args.void_volume,
        report_profile=args.report_profile,
        renderer=args.renderer,
    )


if __name__ == '__main__':
    main()
