"""Unit tests for the GWAS Catalog harmonised region fetcher.

Mocks pysam.TabixFile so tests are offline. Live smoke goes in test_live_gwas_catalog_region_fetch.py.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from gwas_catalog_region_fetch import (
    GWASCatalogClient,
    GWASCatalogFetchError,
    RegionVariant,
    gcst_url_base,
    harmonised_file_url,
)


# ----------------------- URL construction -----------------------


def test_gcst_url_base_buckets_correctly():
    """GCST90475990 sits in bucket GCST90475001-GCST90476000."""
    base = gcst_url_base("GCST90475990")
    assert "GCST90475001-GCST90476000" in base
    assert base.endswith("/GCST90475990/harmonised")


def test_gcst_url_base_low_accession():
    """GCST000001 sits in bucket GCST000001-GCST001000."""
    base = gcst_url_base("GCST000001")
    assert "GCST000001-GCST001000" in base


@pytest.mark.parametrize("bad", [
    "../etc/passwd",
    "GCST90475990; rm -rf /",
    "GCST",
    "90475990",
    "gcst90475990",
    "GCST 90475990",
])
def test_gcst_url_base_rejects_malformed_accession(bad):
    """Reject anything that doesn't match ^GCST\\d+$ before URL formatting."""
    with pytest.raises(ValueError):
        gcst_url_base(bad)


def test_harmonised_file_url_appends_h_tsv_gz():
    url = harmonised_file_url("GCST90475990")
    assert url.endswith("GCST90475990.h.tsv.gz")


def test_gcst_url_rejects_non_numeric_accession():
    with pytest.raises(ValueError):
        gcst_url_base("not_a_gcst")


# ----------------------- TabixFile mocking -----------------------


def _mock_tabix(rows: list[str], header_cols: list[str]):
    """Build a MagicMock standing in for pysam.TabixFile."""
    tbx = MagicMock()
    tbx.header = ["\t".join(header_cols)]
    tbx.fetch.return_value = rows
    tbx.close = MagicMock()
    return tbx


HARMONISED_HEADER = [
    "hm_variant_id", "hm_rsid", "hm_chrom", "hm_pos",
    "hm_other_allele", "hm_effect_allele",
    "hm_beta", "hm_odds_ratio",
    "hm_effect_allele_frequency", "standard_error", "p_value",
]


def test_fetch_region_parses_harmonised_rows(monkeypatch):
    rows = [
        "\t".join(["2_36910110_C_T", "rs10748691", "2", "36910110", "C", "T",
                   "-0.05", "NA", "0.32", "0.008", "1.2e-9"]),
        "\t".join(["2_36932656_A_G", "rs99999",   "2", "36932656", "A", "G",
                   "-0.04", "NA", "0.31", "0.008", "5.4e-9"]),
    ]
    tbx = _mock_tabix(rows, HARMONISED_HEADER)
    monkeypatch.setattr("pysam.TabixFile", lambda url: tbx)

    client = GWASCatalogClient()
    result = client.fetch_region(
        accession="GCST90475990", chromosome="2",
        start_bp=36_410_000, end_bp=37_410_000,
    )
    assert result.accession == "GCST90475990"
    assert result.n_variants == 2
    v0 = result.variants[0]
    assert isinstance(v0, RegionVariant)
    assert v0.variant_id == "2_36910110_C_T"
    assert v0.chromosome == "2"
    assert v0.position == 36_910_110
    assert v0.ref == "C" and v0.alt == "T"
    assert v0.beta == pytest.approx(-0.05)
    assert v0.se == pytest.approx(0.008)
    assert v0.p_value == pytest.approx(1.2e-9)
    assert v0.effect_allele_frequency == pytest.approx(0.32)
    tbx.close.assert_called_once()


def test_fetch_region_skips_rows_with_missing_essentials(monkeypatch):
    rows = [
        "\t".join(["2_36910110_C_T", "rs1", "2", "36910110", "C", "T",
                   "-0.05", "NA", "0.32", "0.008", "1.2e-9"]),
        # missing chrom -> drop
        "\t".join(["2_X_C_T", "rs2", "", "36910200", "C", "T",
                   "0.01", "NA", "0.5", "0.005", "0.1"]),
    ]
    tbx = _mock_tabix(rows, HARMONISED_HEADER)
    monkeypatch.setattr("pysam.TabixFile", lambda url: tbx)

    client = GWASCatalogClient()
    result = client.fetch_region("GCST90475990", "2", 36_410_000, 37_410_000)
    assert result.n_variants == 1


def test_fetch_region_handles_chr_prefix_retry(monkeypatch):
    """Tabix indexes can have 'chr2' or '2'; client retries with the alt form."""
    rows = ["\t".join(["2_1_C_T", "rs1", "2", "1", "C", "T",
                       "-0.05", "NA", "0.32", "0.008", "1.2e-9"])]
    tbx = _mock_tabix(rows, HARMONISED_HEADER)

    call_count = {"n": 0}

    def flaky_fetch(*args, **kwargs):
        call_count["n"] += 1
        if call_count["n"] == 1:
            raise ValueError("Could not retrieve sequence: chrom not found")
        return rows
    tbx.fetch = flaky_fetch

    monkeypatch.setattr("pysam.TabixFile", lambda url: tbx)
    client = GWASCatalogClient()
    result = client.fetch_region("GCST90475990", "2", 1, 1000)
    assert call_count["n"] == 2
    assert result.n_variants == 1


def test_fetch_region_records_release(monkeypatch):
    tbx = _mock_tabix([], HARMONISED_HEADER)
    monkeypatch.setattr("pysam.TabixFile", lambda url: tbx)
    client = GWASCatalogClient()
    result = client.fetch_region("GCST90475990", "2", 1, 1000)
    assert result.release.accession == "GCST90475990"
    assert result.release.harmonised_url.endswith("GCST90475990.h.tsv.gz")
    assert result.release.fetched_at_utc.endswith("Z")


def test_fetch_region_raises_on_unopenable_index(monkeypatch):
    def boom(url):
        raise OSError("could not open tabix index")
    monkeypatch.setattr("pysam.TabixFile", boom)

    client = GWASCatalogClient()
    with pytest.raises(GWASCatalogFetchError):
        # Valid GCST format but the tabix open will fail (mocked).
        client.fetch_region("GCST99999999", "2", 1, 1000)
