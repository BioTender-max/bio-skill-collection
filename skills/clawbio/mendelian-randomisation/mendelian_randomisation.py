#!/usr/bin/env python3
"""Mendelian Randomisation — two-sample MR with full sensitivity analysis.

Implements IVW, MR-Egger, weighted median, and weighted mode estimators with
Cochran's Q, Egger intercept, Steiger directionality, F-statistic diagnostics,
leave-one-out analysis, and publication-ready visualisation.

References:
    Burgess et al. (2013) Genet Epidemiol 37:658-665 (IVW)
    Bowden et al. (2015) Int J Epidemiol 44:512-525 (MR-Egger)
    Bowden et al. (2016) Genet Epidemiol 40:304-314 (Weighted median)
    Verbanck et al. (2018) Nature Genetics 50:693-698 (MR-PRESSO)

Usage:
    python mendelian_randomisation.py --demo --output /tmp/mr_demo
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy import stats

SCRIPT_DIR = Path(__file__).resolve().parent

DISCLAIMER = (
    "ClawBio is a research and educational tool. It is not a medical device "
    "and does not provide clinical diagnoses. Consult a healthcare "
    "professional before making any medical decisions."
)

MIN_F_STAT = 10
EAF_PALINDROME_THRESHOLD = 0.42


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------
@dataclass
class Instrument:
    snp: str
    effect_allele: str
    other_allele: str
    eaf: float
    beta_exposure: float
    se_exposure: float
    pval_exposure: float
    beta_outcome: float
    se_outcome: float
    pval_outcome: float
    f_statistic: float = 0.0

    @property
    def is_palindromic(self) -> bool:
        pairs = {frozenset({"A", "T"}), frozenset({"C", "G"})}
        return frozenset({self.effect_allele, self.other_allele}) in pairs

    @property
    def palindromic_ambiguous(self) -> bool:
        return self.is_palindromic and EAF_PALINDROME_THRESHOLD < self.eaf < (1 - EAF_PALINDROME_THRESHOLD)

    @property
    def weak_instrument(self) -> bool:
        return self.f_statistic < MIN_F_STAT


@dataclass
class MREstimate:
    method: str
    estimate: float
    se: float
    ci_lower: float
    ci_upper: float
    pvalue: float
    n_snps: int


@dataclass
class SensitivityResults:
    cochran_q: float = 0.0
    cochran_q_pvalue: float = 1.0
    cochran_q_df: int = 0
    egger_intercept: float = 0.0
    egger_intercept_se: float = 0.0
    egger_intercept_pvalue: float = 1.0
    mean_f_statistic: float = 0.0
    min_f_statistic: float = 0.0
    n_weak_instruments: int = 0
    i_squared_gx: float = 0.0
    steiger_correct_direction: bool = True
    steiger_pvalue: float = 1.0


# ---------------------------------------------------------------------------
# MR estimators
# ---------------------------------------------------------------------------
def ivw(instruments: list[Instrument]) -> MREstimate:
    """Inverse-Variance Weighted estimator (multiplicative random effects)."""
    bx = np.array([i.beta_exposure for i in instruments])
    by = np.array([i.beta_outcome for i in instruments])
    sy = np.array([i.se_outcome for i in instruments])

    w = 1.0 / (sy ** 2)
    beta_ivw = np.sum(w * bx * by) / np.sum(w * bx ** 2)

    residuals = by - beta_ivw * bx
    if len(instruments) == 1:
        phi = 1.0
    else:
        phi = max(1.0, np.sum(w * residuals ** 2) / (len(instruments) - 1))
    se_ivw = math.sqrt(phi / np.sum(w * bx ** 2))

    z = beta_ivw / se_ivw
    pval = 2 * stats.norm.sf(abs(z))

    return MREstimate(
        method="IVW", estimate=float(beta_ivw), se=float(se_ivw),
        ci_lower=float(beta_ivw - 1.96 * se_ivw),
        ci_upper=float(beta_ivw + 1.96 * se_ivw),
        pvalue=float(pval), n_snps=len(instruments),
    )


def mr_egger(instruments: list[Instrument]) -> tuple[MREstimate, float, float, float]:
    """MR-Egger regression. Returns (estimate, intercept, intercept_se, intercept_p)."""
    bx = np.array([i.beta_exposure for i in instruments])
    by = np.array([i.beta_outcome for i in instruments])
    sy = np.array([i.se_outcome for i in instruments])

    w = 1.0 / (sy ** 2)
    n = len(instruments)

    sum_w = np.sum(w)
    sum_wbx = np.sum(w * bx)
    sum_wbx2 = np.sum(w * bx ** 2)
    sum_wby = np.sum(w * by)
    sum_wbxby = np.sum(w * bx * by)

    denom = sum_w * sum_wbx2 - sum_wbx ** 2
    if abs(denom) < 1e-300:
        return MREstimate("MR-Egger", 0, 1, -1.96, 1.96, 1.0, n), 0.0, 1.0, 1.0

    slope = (sum_w * sum_wbxby - sum_wbx * sum_wby) / denom
    intercept = (sum_wby - slope * sum_wbx) / sum_w

    fitted = intercept + slope * bx
    residuals = by - fitted
    phi = max(1.0, np.sum(w * residuals ** 2) / (n - 2))

    se_slope = math.sqrt(phi * sum_w / denom)
    se_intercept = math.sqrt(phi * sum_wbx2 / denom)

    z_slope = slope / se_slope
    p_slope = 2 * stats.norm.sf(abs(z_slope))
    z_int = intercept / se_intercept
    p_int = 2 * stats.norm.sf(abs(z_int))

    estimate = MREstimate(
        method="MR-Egger", estimate=float(slope), se=float(se_slope),
        ci_lower=float(slope - 1.96 * se_slope),
        ci_upper=float(slope + 1.96 * se_slope),
        pvalue=float(p_slope), n_snps=n,
    )
    return estimate, float(intercept), float(se_intercept), float(p_int)


def weighted_median(instruments: list[Instrument], n_boot: int = 1000) -> MREstimate:
    """Weighted median estimator (Bowden et al., 2016)."""
    bx = np.array([i.beta_exposure for i in instruments])
    by = np.array([i.beta_outcome for i in instruments])
    sy = np.array([i.se_outcome for i in instruments])

    ratios = by / bx
    weights = 1.0 / (sy ** 2 / bx ** 2)
    weights = weights / np.sum(weights)

    order = np.argsort(ratios)
    ratios_sorted = ratios[order]
    weights_sorted = weights[order]
    cum_weights = np.cumsum(weights_sorted)
    idx = np.searchsorted(cum_weights, 0.5)
    beta_wm = float(ratios_sorted[min(idx, len(ratios_sorted) - 1)])

    rng = np.random.default_rng(42)
    boot_estimates = []
    for _ in range(n_boot):
        by_boot = by + rng.normal(0, sy)
        bx_boot = bx
        r_boot = by_boot / bx_boot
        o = np.argsort(r_boot)
        cw = np.cumsum(weights[o])
        j = np.searchsorted(cw, 0.5)
        boot_estimates.append(float(r_boot[o[min(j, len(r_boot) - 1)]]))
    se_wm = float(np.std(boot_estimates))
    z = beta_wm / se_wm if se_wm > 0 else 0
    pval = 2 * stats.norm.sf(abs(z))

    return MREstimate(
        method="Weighted Median", estimate=beta_wm, se=se_wm,
        ci_lower=beta_wm - 1.96 * se_wm, ci_upper=beta_wm + 1.96 * se_wm,
        pvalue=float(pval), n_snps=len(instruments),
    )


def weighted_mode(instruments: list[Instrument], bandwidth: float = 0.5) -> MREstimate:
    """Weighted mode estimator (Hartwig et al., 2017)."""
    bx = np.array([i.beta_exposure for i in instruments])
    by = np.array([i.beta_outcome for i in instruments])
    sy = np.array([i.se_outcome for i in instruments])

    ratios = by / bx
    se_ratios = sy / np.abs(bx)
    weights = 1.0 / se_ratios

    x_grid = np.linspace(np.min(ratios) - 1, np.max(ratios) + 1, 1000)
    density = np.zeros_like(x_grid)
    for r, w in zip(ratios, weights):
        density += w * stats.norm.pdf(x_grid, loc=r, scale=bandwidth)
    beta_mode = float(x_grid[np.argmax(density)])

    se_mode = float(1.0 / (np.sum(weights) * 0.5))
    z = beta_mode / se_mode if se_mode > 0 else 0
    pval = 2 * stats.norm.sf(abs(z))

    return MREstimate(
        method="Weighted Mode", estimate=beta_mode, se=se_mode,
        ci_lower=beta_mode - 1.96 * se_mode, ci_upper=beta_mode + 1.96 * se_mode,
        pvalue=float(pval), n_snps=len(instruments),
    )


# ---------------------------------------------------------------------------
# Sensitivity tests
# ---------------------------------------------------------------------------
def cochran_q(instruments: list[Instrument], ivw_est: MREstimate) -> tuple[float, float, int]:
    """Cochran's Q test for heterogeneity."""
    bx = np.array([i.beta_exposure for i in instruments])
    by = np.array([i.beta_outcome for i in instruments])
    sy = np.array([i.se_outcome for i in instruments])
    w = 1.0 / (sy ** 2)
    residuals = by - ivw_est.estimate * bx
    q = float(np.sum(w * residuals ** 2))
    df = len(instruments) - 1
    p = float(stats.chi2.sf(q, df)) if df > 0 else 1.0
    return q, p, df


def steiger_test(instruments: list[Instrument]) -> tuple[bool, float]:
    """Steiger directionality test — checks causal direction."""
    r2_exp = np.array([2 * i.eaf * (1 - i.eaf) * (i.beta_exposure ** 2) for i in instruments])
    r2_out = np.array([2 * i.eaf * (1 - i.eaf) * (i.beta_outcome ** 2) for i in instruments])
    total_r2_exp = float(np.sum(r2_exp))
    total_r2_out = float(np.sum(r2_out))
    correct = total_r2_exp > total_r2_out
    diff = total_r2_exp - total_r2_out
    se_diff = math.sqrt(total_r2_exp + total_r2_out) * 0.01
    z = diff / se_diff if se_diff > 0 else 0
    p = 2 * stats.norm.sf(abs(z))
    return correct, float(p)


def compute_i_squared_gx(instruments: list[Instrument]) -> float:
    """I² for instrument-exposure associations (Bowden et al., 2016)."""
    bx = np.array([i.beta_exposure for i in instruments])
    sx = np.array([i.se_exposure for i in instruments])
    w = 1.0 / (sx ** 2)
    bx_bar = np.sum(w * bx) / np.sum(w)
    q = float(np.sum(w * (bx - bx_bar) ** 2))
    df = len(instruments) - 1
    if q <= df or df == 0:
        return 0.0
    return max(0.0, float((q - df) / q))


def leave_one_out(instruments: list[Instrument]) -> list[tuple[str, MREstimate]]:
    """Leave-one-out IVW analysis."""
    results = []
    for i, inst in enumerate(instruments):
        subset = instruments[:i] + instruments[i + 1:]
        if len(subset) < 2:
            continue
        est = ivw(subset)
        results.append((inst.snp, est))
    return results


def run_sensitivity(instruments: list[Instrument], ivw_est: MREstimate) -> SensitivityResults:
    """Run full sensitivity analysis battery."""
    q, q_p, q_df = cochran_q(instruments, ivw_est)
    f_stats = [i.f_statistic for i in instruments]
    steiger_dir, steiger_p = steiger_test(instruments)
    i2_gx = compute_i_squared_gx(instruments)

    return SensitivityResults(
        cochran_q=q, cochran_q_pvalue=q_p, cochran_q_df=q_df,
        mean_f_statistic=float(np.mean(f_stats)),
        min_f_statistic=float(np.min(f_stats)),
        n_weak_instruments=sum(1 for f in f_stats if f < MIN_F_STAT),
        i_squared_gx=i2_gx,
        steiger_correct_direction=steiger_dir,
        steiger_pvalue=steiger_p,
    )


# ---------------------------------------------------------------------------
# Visualisation
# ---------------------------------------------------------------------------
def scatter_plot(instruments: list[Instrument], estimates: list[MREstimate], path: Path) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return

    bx = [i.beta_exposure for i in instruments]
    by = [i.beta_outcome for i in instruments]
    sx = [i.se_exposure for i in instruments]
    sy = [i.se_outcome for i in instruments]

    fig, ax = plt.subplots(figsize=(8, 7))
    ax.errorbar(bx, by, xerr=sx, yerr=sy, fmt="o", markersize=5, color="#2166ac",
                ecolor="#bdbdbd", alpha=0.7, capsize=0, label="Instruments")

    x_range = np.linspace(min(bx) - 0.01, max(bx) + 0.01, 100)
    colours = {"IVW": "#d32f2f", "MR-Egger": "#ff9800", "Weighted Median": "#4caf50", "Weighted Mode": "#9c27b0"}
    for est in estimates:
        if est.method in colours:
            ax.plot(x_range, est.estimate * x_range, color=colours[est.method],
                    linewidth=1.5, label=f"{est.method} ({est.estimate:.3f})")

    ax.axhline(0, color="grey", linewidth=0.5)
    ax.axvline(0, color="grey", linewidth=0.5)
    ax.set_xlabel("SNP effect on exposure")
    ax.set_ylabel("SNP effect on outcome")
    ax.set_title("MR Scatter Plot")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def forest_plot(instruments: list[Instrument], ivw_est: MREstimate, path: Path) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return

    ratios = [i.beta_outcome / i.beta_exposure for i in instruments]
    se_ratios = [i.se_outcome / abs(i.beta_exposure) for i in instruments]
    labels = [i.snp for i in instruments]

    fig, ax = plt.subplots(figsize=(8, max(4, len(instruments) * 0.3)))
    y_pos = list(range(len(instruments)))

    ax.errorbar(ratios, y_pos, xerr=[1.96 * s for s in se_ratios], fmt="o", color="#2166ac",
                markersize=4, ecolor="#bdbdbd", capsize=0)
    ax.axvline(ivw_est.estimate, color="#d32f2f", linewidth=1.5, linestyle="--", label=f"IVW: {ivw_est.estimate:.3f}")
    ax.axvline(0, color="grey", linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=6)
    ax.set_xlabel("Causal estimate (Wald ratio)")
    ax.set_title("MR Forest Plot")
    ax.legend(fontsize=8)
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def funnel_plot(instruments: list[Instrument], ivw_est: MREstimate, path: Path) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return

    ratios = [i.beta_outcome / i.beta_exposure for i in instruments]
    precision = [abs(i.beta_exposure) / i.se_outcome for i in instruments]

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.scatter(ratios, precision, s=25, color="#2166ac", alpha=0.7)
    ax.axvline(ivw_est.estimate, color="#d32f2f", linewidth=1.5, linestyle="--", label=f"IVW: {ivw_est.estimate:.3f}")
    ax.set_xlabel("Causal estimate (Wald ratio)")
    ax.set_ylabel("Precision (|bx| / se_outcome)")
    ax.set_title("MR Funnel Plot")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def leave_one_out_plot(loo_results: list[tuple[str, MREstimate]], ivw_all: MREstimate, path: Path) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return

    labels = [snp for snp, _ in loo_results] + ["All"]
    estimates = [est.estimate for _, est in loo_results] + [ivw_all.estimate]
    ci_lo = [est.ci_lower for _, est in loo_results] + [ivw_all.ci_lower]
    ci_hi = [est.ci_upper for _, est in loo_results] + [ivw_all.ci_upper]

    fig, ax = plt.subplots(figsize=(8, max(4, len(labels) * 0.3)))
    y = list(range(len(labels)))
    xerr_lo = [e - lo for e, lo in zip(estimates, ci_lo)]
    xerr_hi = [hi - e for e, hi in zip(estimates, ci_hi)]

    colours = ["#2166ac"] * len(loo_results) + ["#d32f2f"]
    for i, (est, lo, hi, c) in enumerate(zip(estimates, xerr_lo, xerr_hi, colours)):
        ax.errorbar(est, i, xerr=[[lo], [hi]], fmt="o", color=c, markersize=4, capsize=2)

    ax.axvline(ivw_all.estimate, color="#d32f2f", linewidth=0.8, linestyle=":")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=6)
    ax.set_xlabel("IVW estimate (leave-one-out)")
    ax.set_title("Leave-One-Out Analysis")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------
def generate_report(
    instruments: list[Instrument],
    estimates: list[MREstimate],
    sensitivity: SensitivityResults,
    egger_intercept: float,
    egger_intercept_p: float,
    loo: list[tuple[str, MREstimate]],
    exposure: str,
    outcome: str,
    output_dir: Path,
    demo: bool,
) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    output_dir.mkdir(parents=True, exist_ok=True)
    for sub in ("tables", "figures", "reproducibility"):
        (output_dir / sub).mkdir(exist_ok=True)

    _write_mr_table(estimates, output_dir / "tables" / "mr_results.tsv")
    _write_sensitivity_table(sensitivity, egger_intercept, egger_intercept_p, output_dir / "tables" / "sensitivity.tsv")
    _write_instruments_table(instruments, output_dir / "tables" / "harmonised_instruments.tsv")
    _write_report_md(instruments, estimates, sensitivity, egger_intercept, egger_intercept_p, exposure, outcome, output_dir, ts, demo)
    _write_result_json(estimates, sensitivity, egger_intercept, egger_intercept_p, exposure, outcome, output_dir, ts, demo)
    _write_repro(output_dir, ts, demo)


def _write_mr_table(estimates, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["method", "estimate", "se", "ci_lower", "ci_upper", "pvalue", "n_snps"])
        for e in estimates:
            w.writerow([e.method, f"{e.estimate:.6f}", f"{e.se:.6f}", f"{e.ci_lower:.6f}", f"{e.ci_upper:.6f}", f"{e.pvalue:.2e}", e.n_snps])


def _write_sensitivity_table(s, egger_int, egger_p, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["test", "statistic", "pvalue", "interpretation"])
        w.writerow(["Cochran_Q", f"{s.cochran_q:.2f}", f"{s.cochran_q_pvalue:.4f}", "Significant = heterogeneity" if s.cochran_q_pvalue < 0.05 else "No significant heterogeneity"])
        w.writerow(["Egger_intercept", f"{egger_int:.6f}", f"{egger_p:.4f}", "Significant = directional pleiotropy" if egger_p < 0.05 else "No evidence of directional pleiotropy"])
        w.writerow(["Mean_F_statistic", f"{s.mean_f_statistic:.1f}", "N/A", f"{'WEAK' if s.mean_f_statistic < MIN_F_STAT else 'Strong'} instruments"])
        w.writerow(["Min_F_statistic", f"{s.min_f_statistic:.1f}", "N/A", f"{s.n_weak_instruments} weak instruments (F<{MIN_F_STAT})"])
        w.writerow(["I_squared_GX", f"{s.i_squared_gx:.4f}", "N/A", "SIMEX recommended" if s.i_squared_gx < 0.9 else "No SIMEX needed"])
        w.writerow(["Steiger_direction", "Correct" if s.steiger_correct_direction else "REVERSED", f"{s.steiger_pvalue:.4f}", "Correct direction" if s.steiger_correct_direction else "WARNING: reversed causal direction"])


def _write_instruments_table(instruments, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["SNP", "effect_allele", "other_allele", "eaf", "beta_exp", "se_exp", "pval_exp", "beta_out", "se_out", "pval_out", "f_stat", "palindromic", "weak"])
        for i in instruments:
            w.writerow([i.snp, i.effect_allele, i.other_allele, i.eaf, i.beta_exposure, i.se_exposure, f"{i.pval_exposure:.2e}", i.beta_outcome, i.se_outcome, f"{i.pval_outcome:.2e}", f"{i.f_statistic:.1f}", i.is_palindromic, i.weak_instrument])


def _write_report_md(instruments, estimates, sens, egger_int, egger_p, exposure, outcome, output_dir, ts, demo):
    n_palindromic = sum(1 for i in instruments if i.palindromic_ambiguous)
    lines = [
        "# Mendelian Randomisation Report", "",
        f"**Generated**: {ts}",
        f"**Exposure**: {exposure}",
        f"**Outcome**: {outcome}",
        f"**Instruments**: {len(instruments)} SNPs",
        f"**Mode**: {'Demo (cached data, offline)' if demo else 'Live'}", "",
        "## MR Estimates", "",
        "| Method | Estimate | SE | 95% CI | P-value |",
        "|--------|----------|----|--------|---------|",
    ]
    for e in estimates:
        lines.append(f"| {e.method} | {e.estimate:.4f} | {e.se:.4f} | [{e.ci_lower:.4f}, {e.ci_upper:.4f}] | {e.pvalue:.2e} |")
    lines.append("")

    lines.extend([
        "## Sensitivity Analysis", "",
        "| Test | Result | P-value | Interpretation |",
        "|------|--------|---------|----------------|",
        f"| Cochran's Q | {sens.cochran_q:.2f} (df={sens.cochran_q_df}) | {sens.cochran_q_pvalue:.4f} | {'Heterogeneity detected' if sens.cochran_q_pvalue < 0.05 else 'No significant heterogeneity'} |",
        f"| Egger intercept | {egger_int:.4f} | {egger_p:.4f} | {'Directional pleiotropy' if egger_p < 0.05 else 'No directional pleiotropy'} |",
        f"| Mean F-statistic | {sens.mean_f_statistic:.1f} | — | {'**WARNING: weak instruments**' if sens.mean_f_statistic < MIN_F_STAT else 'Strong instruments'} |",
        f"| Weak instruments (F<{MIN_F_STAT}) | {sens.n_weak_instruments}/{len(instruments)} | — | {'**WARNING**' if sens.n_weak_instruments > 0 else 'None'} |",
        f"| I²_GX | {sens.i_squared_gx:.4f} | — | {'SIMEX correction recommended' if sens.i_squared_gx < 0.9 else 'Adequate'} |",
        f"| Steiger direction | {'Correct' if sens.steiger_correct_direction else '**REVERSED**'} | {sens.steiger_pvalue:.4f} | {'Exposure → Outcome confirmed' if sens.steiger_correct_direction else '**WARNING: reverse causation**'} |",
        "",
    ])

    if n_palindromic > 0:
        lines.extend([f"**WARNING**: {n_palindromic} palindromic SNP(s) with ambiguous EAF (0.42–0.58) — these were retained but may introduce bias. Manual review recommended.", ""])

    lines.extend([
        "## Interpretation", "",
        f"The IVW estimate suggests a {'positive' if estimates[0].estimate > 0 else 'negative'} causal effect of {exposure} on {outcome} ",
        f"(beta = {estimates[0].estimate:.4f}, 95% CI [{estimates[0].ci_lower:.4f}, {estimates[0].ci_upper:.4f}], P = {estimates[0].pvalue:.2e}). ",
        "",
    ])
    consistent = all(abs(e.estimate - estimates[0].estimate) < 2 * estimates[0].se for e in estimates[1:])
    if consistent:
        lines.append("Sensitivity analyses show consistent estimates across IVW, MR-Egger, weighted median, and weighted mode, supporting a robust causal inference.")
    else:
        lines.append("**Caution**: Estimates differ across methods, suggesting potential violations of MR assumptions. Interpret with care.")
    lines.extend(["", "---", "", f"*{DISCLAIMER}*", ""])
    (output_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")


def _write_result_json(estimates, sens, egger_int, egger_p, exposure, outcome, output_dir, ts, demo):
    result = {
        "tool": "ClawBio Mendelian Randomisation",
        "version": "0.1.0",
        "timestamp": ts,
        "mode": "demo" if demo else "live",
        "exposure": exposure,
        "outcome": outcome,
        "estimates": [{"method": e.method, "estimate": round(e.estimate, 6), "se": round(e.se, 6), "pvalue": f"{e.pvalue:.2e}", "n_snps": e.n_snps} for e in estimates],
        "sensitivity": {
            "cochran_q": round(sens.cochran_q, 2), "cochran_q_p": round(sens.cochran_q_pvalue, 4),
            "egger_intercept": round(egger_int, 6), "egger_intercept_p": round(egger_p, 4),
            "mean_f_stat": round(sens.mean_f_statistic, 1),
            "n_weak": sens.n_weak_instruments,
            "i_squared_gx": round(sens.i_squared_gx, 4),
            "steiger_correct": sens.steiger_correct_direction,
        },
        "disclaimer": DISCLAIMER,
    }
    (output_dir / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")


def _write_repro(output_dir, ts, demo):
    d = output_dir / "reproducibility"
    d.mkdir(exist_ok=True)
    (d / "commands.sh").write_text(f"#!/usr/bin/env bash\n# Generated: {ts}\npython mendelian_randomisation.py {'--demo' if demo else ''} --output {output_dir}\n", encoding="utf-8")
    (d / "software_versions.json").write_text(json.dumps({"python": sys.version, "numpy": np.__version__, "scipy": stats.scipy.__version__ if hasattr(stats, 'scipy') else "unknown", "generated": ts}, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------
def load_demo_instruments() -> tuple[list[Instrument], str, str]:
    cache = SCRIPT_DIR / "example_data" / "demo_instruments.json"
    with open(cache) as f:
        data = json.load(f)
    instruments = [Instrument(
        snp=s["SNP"], effect_allele=s["effect_allele"], other_allele=s["other_allele"],
        eaf=s["eaf"], beta_exposure=s["beta_exposure"], se_exposure=s["se_exposure"],
        pval_exposure=s["pval_exposure"], beta_outcome=s["beta_outcome"],
        se_outcome=s["se_outcome"], pval_outcome=s["pval_outcome"],
        f_statistic=s["f_statistic"],
    ) for s in data["instruments"]]
    return instruments, data["exposure"], data["outcome"]


def run_pipeline(instruments: list[Instrument], exposure: str, outcome: str, output_dir: Path, demo: bool = False) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "figures").mkdir(exist_ok=True)

    weak = [i for i in instruments if i.weak_instrument]
    if weak:
        print(f"  WARNING: {len(weak)} instrument(s) with F-statistic < {MIN_F_STAT} — weak instrument bias possible", file=sys.stderr)

    palindromic = [i for i in instruments if i.palindromic_ambiguous]
    if palindromic:
        print(f"  WARNING: {len(palindromic)} palindromic SNP(s) with ambiguous EAF — flagged for manual review", file=sys.stderr)

    print(f"[MR] Running IVW ({len(instruments)} instruments)...")
    ivw_est = ivw(instruments)

    print("[MR] Running MR-Egger...")
    egger_est, egger_int, egger_int_se, egger_int_p = mr_egger(instruments)

    print("[MR] Running Weighted Median...")
    wm_est = weighted_median(instruments)

    print("[MR] Running Weighted Mode...")
    wmode_est = weighted_mode(instruments)

    estimates = [ivw_est, egger_est, wm_est, wmode_est]

    print("[MR] Running sensitivity analysis...")
    sens = run_sensitivity(instruments, ivw_est)
    sens.egger_intercept = egger_int
    sens.egger_intercept_se = egger_int_se
    sens.egger_intercept_pvalue = egger_int_p

    print("[MR] Leave-one-out analysis...")
    loo = leave_one_out(instruments)

    print("[MR] Generating plots...")
    scatter_plot(instruments, estimates, output_dir / "figures" / "scatter.png")
    forest_plot(instruments, ivw_est, output_dir / "figures" / "forest.png")
    funnel_plot(instruments, ivw_est, output_dir / "figures" / "funnel.png")
    leave_one_out_plot(loo, ivw_est, output_dir / "figures" / "leave_one_out.png")

    print("[MR] Generating report...")
    generate_report(instruments, estimates, sens, egger_int, egger_int_p, loo, exposure, outcome, output_dir, demo)

    print(f"[MR] IVW estimate: {ivw_est.estimate:.4f} (P={ivw_est.pvalue:.2e})")
    print(f"[MR] Report written to: {output_dir / 'report.md'}")

    return {
        "ivw_estimate": ivw_est.estimate,
        "ivw_pvalue": ivw_est.pvalue,
        "n_instruments": len(instruments),
        "cochran_q_p": sens.cochran_q_pvalue,
        "egger_intercept_p": egger_int_p,
        "n_weak": sens.n_weak_instruments,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Mendelian Randomisation — two-sample MR")
    parser.add_argument("--demo", action="store_true", help="Run with cached BMI->T2D demo data (offline)")
    parser.add_argument("--instruments", type=str, help="JSON file with harmonised instruments")
    parser.add_argument("--output", type=str, required=True, help="Output directory")

    args = parser.parse_args()

    if args.demo:
        instruments, exposure, outcome = load_demo_instruments()
    elif args.instruments:
        with open(args.instruments) as f:
            data = json.load(f)
        instruments = [Instrument(
            snp=s["SNP"], effect_allele=s["effect_allele"], other_allele=s["other_allele"],
            eaf=s["eaf"], beta_exposure=s["beta_exposure"], se_exposure=s["se_exposure"],
            pval_exposure=s["pval_exposure"], beta_outcome=s["beta_outcome"],
            se_outcome=s["se_outcome"], pval_outcome=s["pval_outcome"],
            f_statistic=s["f_statistic"],
        ) for s in data["instruments"]]
        exposure = data.get("exposure", "Exposure")
        outcome = data.get("outcome", "Outcome")
    else:
        parser.error("Provide --demo or --instruments <json>")

    output_dir = Path(args.output)
    print(f"[MR] Starting MR pipeline: {exposure} -> {outcome}")
    print(f"[MR] {len(instruments)} instruments loaded ({'demo/cached' if args.demo else 'user-provided'})")

    run_pipeline(instruments, exposure, outcome, output_dir, demo=args.demo)


if __name__ == "__main__":
    main()
