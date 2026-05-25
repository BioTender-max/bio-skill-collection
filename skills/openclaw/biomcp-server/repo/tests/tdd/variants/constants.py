# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

"""Constants for variant tests."""

# API retry settings
API_RETRY_DELAY_SECONDS = 1.0
MAX_RETRY_ATTEMPTS = 2

# Test data settings
DEFAULT_MAX_STUDIES = 10  # Number of studies to query in integration tests
STRUCTURE_CHECK_LIMIT = (
    3  # Number of items to check when verifying data structures
)

# Timeout settings
INTEGRATION_TEST_TIMEOUT = 30.0  # Maximum time for integration tests

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
