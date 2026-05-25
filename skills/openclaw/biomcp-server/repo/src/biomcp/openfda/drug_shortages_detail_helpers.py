# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

"""
Helper functions for formatting drug shortage details.
"""

from typing import Any


def format_shortage_status(shortage: dict[str, Any]) -> list[str]:
    """Format status information for shortage detail."""
    output = []

    status = shortage.get("status", "Unknown")
    status_emoji = "🔴" if "current" in status.lower() else "🟢"
    output.append(f"{status_emoji} **Status**: {status}")

    return output


def format_shortage_names(shortage: dict[str, Any]) -> list[str]:
    """Format drug names for shortage detail."""
    output = []

    if generic := shortage.get("generic_name"):
        output.append(f"**Generic Name**: {generic}")

    brands = shortage.get("brand_names")
    if brands and brands[0]:
        output.append(f"**Brand Names**: {', '.join(brands)}")

    return output


def format_shortage_timeline(shortage: dict[str, Any]) -> list[str]:
    """Format timeline information for shortage detail."""
    output = ["### Timeline"]

    if start_date := shortage.get("shortage_start_date"):
        output.append(f"**Shortage Started**: {start_date}")

    if resolution_date := shortage.get("resolution_date"):
        output.append(f"**Resolved**: {resolution_date}")
    elif estimated := shortage.get("estimated_resolution"):
        output.append(f"**Estimated Resolution**: {estimated}")
    else:
        output.append("**Estimated Resolution**: Unknown")

    return output


def format_shortage_details_section(shortage: dict[str, Any]) -> list[str]:
    """Format details section for shortage detail."""
    output = ["### Details"]

    if reason := shortage.get("reason"):
        output.append(f"**Reason for Shortage**:\n{reason}")

    if notes := shortage.get("notes"):
        from .utils import clean_text

        output.append(f"\n**Additional Notes**:\n{clean_text(notes)}")

    return output

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
