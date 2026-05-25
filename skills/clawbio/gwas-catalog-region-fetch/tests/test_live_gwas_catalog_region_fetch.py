"""Live smoke test for gwas-catalog-region-fetch.

Hits the real EBI GWAS Catalog harmonised tabix-on-FTP for a small
SORT1 cis-window slice (GCST90269602, cholesterol-VLDL at the Musunuru 2010
1p13.3 LDL/CHD locus). Gated by @pytest.mark.live and RUN_LIVE_TESTS=1
so the offline suite stays network-free.

Run locally with:
    RUN_LIVE_TESTS=1 pytest skills/gwas-catalog-region-fetch/tests/test_live_gwas_catalog_region_fetch.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from gwas_catalog_region_fetch import (  # noqa: E402
    GWASCatalogClient,
    RegionResult,
)


pytestmark = pytest.mark.live


@pytest.mark.skipif(
    os.getenv("RUN_LIVE_TESTS") != "1",
    reason="live tests gated on RUN_LIVE_TESTS=1",
)
def test_live_fetch_region_sort1_cholesterol_smoke() -> None:
    """Real harmonised tabix slice for SORT1 cis-window returns variants."""
    client = GWASCatalogClient()
    result = client.fetch_region(
        accession="GCST90269602",
        chromosome="1",
        start_bp=109_774_000,
        end_bp=109_775_000,
    )
    assert isinstance(result, RegionResult)
    assert result.variants, "expected non-empty tabix slice for SORT1 cis-window"
    v = result.variants[0]
    assert v.chromosome == "1"
    assert 109_774_000 <= v.position <= 109_775_000
