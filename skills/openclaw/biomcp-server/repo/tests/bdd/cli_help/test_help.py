# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import shlex

from pytest_bdd import given, parsers, scenarios, then
from typer.testing import CliRunner

from biomcp.cli.main import app

# Link to the feature file
scenarios("help.feature")

runner = CliRunner()


@given(parsers.parse('I run "{command}"'), target_fixture="cli_result")
def cli_result(command):
    """
    Run the given CLI command and return the result.
    """
    # Remove the initial token ("biomcp") if present
    args = (
        shlex.split(command)[1:]
        if command.startswith("biomcp")
        else shlex.split(command)
    )
    result = runner.invoke(app, args)
    assert result.exit_code == 0, f"CLI command failed: {result.stderr}"
    return result


@then(parsers.parse('the output should contain "{expected}"'))
def output_should_contain(cli_result, expected):
    """
    Verify that the output contains the expected text.
    This helper handles both plain text and rich-formatted text outputs.
    """
    # Check if the expected text is in the output, ignoring case
    assert (
        expected.lower() in cli_result.stdout.lower()
    ), f"Expected output to contain '{expected}', but it did not.\nActual output: {cli_result.stdout}"

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
