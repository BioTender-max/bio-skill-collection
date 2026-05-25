#!/usr/bin/env bash
# Example invocation: cholesterol-VLDL GWAS slice at SORT1 locus.

set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 -c "
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path('${DIR}').parent))

from gwas_catalog_region_fetch import GWASCatalogClient

with open('${DIR}/input.json') as f:
    cfg = json.load(f)

client = GWASCatalogClient()
result = client.fetch_region(
    accession=cfg['accession'],
    chromosome=cfg['chromosome'],
    start_bp=cfg['start_bp'],
    end_bp=cfg['end_bp'],
)
print(f'n_variants: {result.n_variants}')
print(f'release.accession: {result.release.accession}')
print(f'release.fetched_at_utc: {result.release.fetched_at_utc}')
print(f'first 3 variants:')
for v in result.variants[:3]:
    print(f'  {v.variant_id}\\tbeta={v.beta:.4f}\\tse={v.se:.4f}\\tp={v.p_value:.2e}')
"
