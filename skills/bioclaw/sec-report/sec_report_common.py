#!/usr/bin/env python3
"""
Shared helper utilities for SEC report generation.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional


def dominant_peak(result):
    return max(result.peaks, key=lambda p: p.relative_area_pct, default=None)


def has_broad_peaks(result, threshold: float = 2.5) -> bool:
    return any(getattr(p, "fwhm", 0.0) > threshold for p in getattr(result, "peaks", []))


def _ranked(results: List[object]) -> List[object]:
    return sorted(
        results,
        key=lambda r: (-getattr(r, "quality_score", 0.0), getattr(r, "aggregation_pct", 0.0), getattr(r, "name", "")),
    )


def select_representative_constructs(results: List[object], max_items: int = 6) -> List[object]:
    """Pick a deterministic, diverse subset for compact reports."""
    ranked = _ranked(results)
    if len(ranked) <= max_items:
        return ranked

    rings = _ranked([
        r for r in ranked
        if getattr(r, "dominant_species", None) in ("large_oligomer", "oligomer")
        and getattr(r, "quality_score", 0.0) >= 5.0
    ])
    monodisperse_controls = _ranked([
        r for r in ranked
        if getattr(r, "dominant_species", None) in ("dimer", "monomer")
        and getattr(r, "homogeneity", None) in ("monodisperse", "predominantly_monodisperse")
        and getattr(r, "quality_score", 0.0) >= 6.0
    ])
    heterogeneous = sorted(
        [
            r for r in ranked
            if (
                getattr(r, "homogeneity", None) == "polydisperse"
                or has_broad_peaks(r)
            )
            and getattr(r, "quality_score", 0.0) >= 3.0
            and getattr(r, "aggregation_pct", 0.0) < 30.0
        ],
        key=lambda r: (abs(getattr(r, "quality_score", 0.0) - 5.0), getattr(r, "aggregation_pct", 0.0), getattr(r, "name", "")),
    )
    failures = sorted(
        [
            r for r in ranked
            if getattr(r, "aggregation_pct", 0.0) >= 15.0 or getattr(r, "quality_score", 0.0) < 4.0
        ],
        key=lambda r: (-getattr(r, "aggregation_pct", 0.0), getattr(r, "quality_score", 0.0), getattr(r, "name", "")),
    )

    buckets = [
        ("ring", rings),
        ("control", monodisperse_controls),
        ("heterogeneous", heterogeneous),
        ("failure", failures),
    ]

    selected: List[object] = []
    seen = set()
    positions = {name: 0 for name, _ in buckets}

    def add_item(item) -> bool:
        if item is None:
            return False
        name = getattr(item, "name", None)
        if not name or name in seen:
            return False
        selected.append(item)
        seen.add(name)
        return True

    for _, bucket in buckets:
        for item in bucket:
            if add_item(item):
                break
        if len(selected) >= max_items:
            return selected[:max_items]

    while len(selected) < max_items:
        progressed = False
        for bucket_name, bucket in buckets:
            idx = positions[bucket_name]
            while idx < len(bucket) and getattr(bucket[idx], "name", None) in seen:
                idx += 1
            positions[bucket_name] = idx
            if idx < len(bucket) and add_item(bucket[idx]):
                positions[bucket_name] += 1
                progressed = True
                if len(selected) >= max_items:
                    return selected[:max_items]
        if not progressed:
            break

    for item in ranked:
        if add_item(item) and len(selected) >= max_items:
            break

    return selected[:max_items]


# ── Cohort detection ──────────────────────────────────────────────────────────

_FILENAME_DATE_RE = re.compile(r"^(\d{4})\d{2,4}")


def detect_cohort_year(filepath: str) -> Optional[int]:
    """Extract a 4-digit year from directory components or filename prefix."""
    for part in Path(filepath).parts:
        if re.fullmatch(r"\d{4}", part):
            year = int(part)
            if 2000 <= year <= 2099:
                return year
    m = _FILENAME_DATE_RE.match(Path(filepath).stem)
    if m:
        year = int(m.group(1))
        if 2000 <= year <= 2099:
            return year
    return None


def assign_cohorts(
    results: list,
    data_file_attr: str = "data_file",
) -> Dict[str, str]:
    """Detect cohort years and set *cohort* / *cohort_year* on each result.

    The most-recent year becomes ``primary``; older years become ``context``.
    Returns ``{name: label}`` for logging.  No-op when only one year is found.
    """
    year_map: Dict[str, Optional[int]] = {}
    for r in results:
        fp = getattr(r, data_file_attr, None)
        year_map[r.name] = detect_cohort_year(fp) if fp else None

    years_found = {y for y in year_map.values() if y is not None}
    if len(years_found) <= 1:
        return {r.name: "primary" for r in results}

    primary_year = max(years_found)
    labels: Dict[str, str] = {}
    for r in results:
        y = year_map.get(r.name)
        if y is not None and y < primary_year:
            r.cohort = "context"
            r.cohort_year = y
            labels[r.name] = f"context ({y})"
        else:
            r.cohort = "primary"
            r.cohort_year = y
            labels[r.name] = f"primary ({y})" if y else "primary"
    return labels
