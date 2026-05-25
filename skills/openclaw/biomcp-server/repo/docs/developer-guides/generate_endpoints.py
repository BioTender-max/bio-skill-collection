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
Generate third-party endpoints documentation from the endpoint registry.

This script reads the endpoint registry and generates a markdown file
documenting all third-party API endpoints used by BioMCP.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from biomcp.utils.endpoint_registry import EndpointRegistry


def main():
    """Generate endpoints documentation."""
    # Initialize registry
    registry = EndpointRegistry()

    # Generate markdown report
    markdown_content = registry.generate_markdown_report()

    # Write to file
    output_path = Path(__file__).parent / "03-third-party-endpoints.md"
    output_path.write_text(markdown_content)

    print(f"Generated endpoints documentation: {output_path}")


if __name__ == "__main__":
    main()

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
