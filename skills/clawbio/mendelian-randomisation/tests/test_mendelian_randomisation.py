"""Tests for mendelian-randomisation skill.

Validates MR estimators (IVW, Egger, weighted median/mode), sensitivity
tests, instrument diagnostics, and end-to-end demo mode.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR))

from mendelian_randomisation import (
    Instrument,
    MREstimate,
    cochran_q,
    compute_i_squared_gx,
    generate_report,
    ivw,
    leave_one_out,
    load_demo_instruments,
    mr_egger,
    run_pipeline,
    run_sensitivity,
    steiger_test,
    weighted_median,
    weighted_mode,
)


@pytest.fixture
def demo_instruments():
    instruments, _, _ = load_demo_instruments()
    return instruments


@pytest.fixture
def known_causal():
    """Create instruments with a known causal effect of 0.5."""
    rng = np.random.default_rng(42)
    instruments = []
    for i in range(20):
        bx = rng.uniform(0.03, 0.07) * rng.choice([1, -1])
        se_x = abs(bx) / rng.uniform(5, 10)
        by = bx * 0.5 + rng.normal(0, se_x * 0.2)
        se_y = se_x * rng.uniform(1.5, 2.0)
        instruments.append(Instrument(
            snp=f"rs{i}", effect_allele="A", other_allele="G",
            eaf=rng.uniform(0.2, 0.8),
            beta_exposure=float(bx), se_exposure=float(se_x),
            pval_exposure=1e-10,
            beta_outcome=float(by), se_outcome=float(se_y),
            pval_outcome=0.01,
            f_statistic=float((bx / se_x) ** 2),
        ))
    return instruments


# ---------------------------------------------------------------------------
# Unit tests — estimators
# ---------------------------------------------------------------------------
class TestIVW:
    def test_returns_mr_estimate(self, demo_instruments):
        est = ivw(demo_instruments)
        assert isinstance(est, MREstimate)
        assert est.method == "IVW"
        assert est.n_snps == 30

    def test_recovers_true_effect(self, demo_instruments):
        est = ivw(demo_instruments)
        assert 0.3 < est.estimate < 0.9

    def test_significant_pvalue(self, demo_instruments):
        est = ivw(demo_instruments)
        assert est.pvalue < 0.05

    def test_ci_contains_estimate(self, demo_instruments):
        est = ivw(demo_instruments)
        assert est.ci_lower < est.estimate < est.ci_upper

    def test_known_causal_effect(self, known_causal):
        est = ivw(known_causal)
        assert abs(est.estimate - 0.5) < 0.3


class TestMREgger:
    def test_returns_estimate_and_intercept(self, demo_instruments):
        est, intercept, se_int, p_int = mr_egger(demo_instruments)
        assert est.method == "MR-Egger"
        assert isinstance(intercept, float)
        assert isinstance(p_int, float)

    def test_intercept_near_zero_when_no_pleiotropy(self, demo_instruments):
        _, intercept, _, p_int = mr_egger(demo_instruments)
        assert abs(intercept) < 0.1
        assert p_int > 0.05


class TestWeightedMedian:
    def test_returns_estimate(self, demo_instruments):
        est = weighted_median(demo_instruments)
        assert est.method == "Weighted Median"
        assert est.n_snps == 30

    def test_consistent_with_ivw(self, demo_instruments):
        ivw_est = ivw(demo_instruments)
        wm_est = weighted_median(demo_instruments)
        assert abs(ivw_est.estimate - wm_est.estimate) < 0.3


class TestWeightedMode:
    def test_returns_estimate(self, demo_instruments):
        est = weighted_mode(demo_instruments)
        assert est.method == "Weighted Mode"


# ---------------------------------------------------------------------------
# Unit tests — sensitivity
# ---------------------------------------------------------------------------
class TestSensitivity:
    def test_cochran_q_no_heterogeneity(self, demo_instruments):
        ivw_est = ivw(demo_instruments)
        q, p, df = cochran_q(demo_instruments, ivw_est)
        assert df == 29
        assert p > 0.05

    def test_steiger_correct_direction(self, demo_instruments):
        correct, p = steiger_test(demo_instruments)
        assert correct is True

    def test_i_squared_gx(self, demo_instruments):
        i2 = compute_i_squared_gx(demo_instruments)
        assert 0 <= i2 <= 1

    def test_leave_one_out_length(self, demo_instruments):
        loo = leave_one_out(demo_instruments)
        assert len(loo) == 30

    def test_run_sensitivity_returns_all_fields(self, demo_instruments):
        ivw_est = ivw(demo_instruments)
        sens = run_sensitivity(demo_instruments, ivw_est)
        assert sens.mean_f_statistic > 0
        assert sens.cochran_q >= 0


# ---------------------------------------------------------------------------
# Unit tests — instrument properties
# ---------------------------------------------------------------------------
class TestInstrumentProperties:
    def test_palindromic_AT(self):
        i = Instrument("rs1", "A", "T", 0.5, 0.05, 0.01, 1e-10, 0.03, 0.02, 0.1, 25.0)
        assert i.is_palindromic is True
        assert i.palindromic_ambiguous is True

    def test_palindromic_not_ambiguous(self):
        i = Instrument("rs1", "A", "T", 0.2, 0.05, 0.01, 1e-10, 0.03, 0.02, 0.1, 25.0)
        assert i.is_palindromic is True
        assert i.palindromic_ambiguous is False

    def test_not_palindromic(self):
        i = Instrument("rs1", "A", "C", 0.5, 0.05, 0.01, 1e-10, 0.03, 0.02, 0.1, 25.0)
        assert i.is_palindromic is False

    def test_weak_instrument(self):
        i = Instrument("rs1", "A", "G", 0.3, 0.05, 0.02, 1e-10, 0.03, 0.02, 0.1, 6.0)
        assert i.weak_instrument is True

    def test_strong_instrument(self):
        i = Instrument("rs1", "A", "G", 0.3, 0.05, 0.005, 1e-10, 0.03, 0.02, 0.1, 100.0)
        assert i.weak_instrument is False


# ---------------------------------------------------------------------------
# Integration tests — demo pipeline
# ---------------------------------------------------------------------------
class TestDemoPipeline:
    def test_demo_end_to_end(self, tmp_path):
        instruments, exposure, outcome = load_demo_instruments()
        summary = run_pipeline(instruments, exposure, outcome, tmp_path, demo=True)

        assert summary["n_instruments"] == 30
        assert 0.3 < summary["ivw_estimate"] < 0.9
        assert summary["ivw_pvalue"] < 0.05
        assert summary["n_weak"] == 0

        assert (tmp_path / "report.md").exists()
        assert (tmp_path / "result.json").exists()
        assert (tmp_path / "tables" / "mr_results.tsv").exists()
        assert (tmp_path / "tables" / "sensitivity.tsv").exists()
        assert (tmp_path / "tables" / "harmonised_instruments.tsv").exists()
        assert (tmp_path / "figures" / "scatter.png").exists()
        assert (tmp_path / "figures" / "forest.png").exists()
        assert (tmp_path / "figures" / "funnel.png").exists()
        assert (tmp_path / "figures" / "leave_one_out.png").exists()

    def test_demo_report_content(self, tmp_path):
        instruments, exposure, outcome = load_demo_instruments()
        run_pipeline(instruments, exposure, outcome, tmp_path, demo=True)

        report = (tmp_path / "report.md").read_text()
        assert "Mendelian Randomisation" in report
        assert "BMI" in report
        assert "T2D" in report
        assert "ClawBio is a research" in report
        assert "IVW" in report

        result = json.loads((tmp_path / "result.json").read_text())
        assert result["exposure"] == "Body mass index (BMI)"
        assert len(result["estimates"]) == 4
        assert result["sensitivity"]["n_weak"] == 0

    def test_all_methods_consistent(self, tmp_path):
        instruments, exposure, outcome = load_demo_instruments()
        run_pipeline(instruments, exposure, outcome, tmp_path, demo=True)

        result = json.loads((tmp_path / "result.json").read_text())
        estimates = {e["method"]: e["estimate"] for e in result["estimates"]}
        ivw_est = estimates["IVW"]
        for method, est in estimates.items():
            assert abs(est - ivw_est) < 0.2, f"{method} ({est:.3f}) diverges from IVW ({ivw_est:.3f})"
