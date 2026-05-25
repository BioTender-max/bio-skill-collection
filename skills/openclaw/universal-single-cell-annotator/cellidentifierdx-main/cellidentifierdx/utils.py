# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import pandas as pd
import openpyxl

def load_data(reference_file, expr_file):
    wb = openpyxl.load_workbook(reference_file)
    sheet_names = wb.sheetnames
    expr_df = pd.read_csv(expr_file, header=0)
    expr_df.columns = expr_df.columns.str.strip()
    return sheet_names, expr_df


__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
