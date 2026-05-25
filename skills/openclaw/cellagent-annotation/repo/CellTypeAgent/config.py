# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = {
    'cell_type_data': os.path.join(PROJECT_ROOT, 'CellTypeAgent', 'data', 'GPTCellType'),
    'datasets': os.path.join(PROJECT_ROOT, 'CellTypeAgent', 'data', 'GPTCellType', 'datasets'),
    'logs': os.path.join(PROJECT_ROOT, 'CellTypeAgent', 'logs'),
    'analysis': os.path.join(PROJECT_ROOT, 'CellTypeAgent', 'analysis')
}

for path in DATA_DIR.values():
    os.makedirs(path, exist_ok=True)

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
