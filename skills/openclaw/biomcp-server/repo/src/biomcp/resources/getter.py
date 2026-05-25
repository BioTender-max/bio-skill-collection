# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

from pathlib import Path

from .. import mcp_app

RESOURCES_ROOT = Path(__file__).parent


@mcp_app.resource("biomcp://instructions.md")
def get_instructions() -> str:
    return (RESOURCES_ROOT / "instructions.md").read_text(encoding="utf-8")


@mcp_app.resource("biomcp://researcher.md")
def get_researcher() -> str:
    return (RESOURCES_ROOT / "researcher.md").read_text(encoding="utf-8")

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
