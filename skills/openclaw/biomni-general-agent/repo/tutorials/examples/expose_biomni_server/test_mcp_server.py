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
Simple test script for testing a single Biomni MCP tool.
"""

import asyncio
import json
import sys

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

# Configuration - Change these to test different tools
TOOL_TO_TEST = "query_uniprot"  # Change this to the tool you want to test
TEST_ARGS = {"prompt": "Find information about human insulin protein"}

# Alternative test configurations - uncomment the one you want to test:

# TOOL_TO_TEST = "blast_sequence"
# TEST_ARGS = {
#     "sequence": "ATGAAACGCATTAGCACCACCATTACCACCACCATCACCATTACCACAGGTAACGGTGCGGGCTGA",
#     "program": "blastn",
#     "database": "nt"
# }

# TOOL_TO_TEST = "region_to_ccre_screen"
# TEST_ARGS = {
#     "coord_chrom": "chr1",
#     "coord_start": 1000000,
#     "coord_end": 1001000,
#     "assembly": "hg38"
# }

# TOOL_TO_TEST = "query_emdb"
# TEST_ARGS = {
#     "prompt": "Find cryo-EM structures of ribosomes"
# }


async def test_single_tool():
    """Test a single tool in the Biomni MCP server."""

    # Set up the server parameters
    # Use relative path from the current script's directory
    import os

    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_script = os.path.join(current_dir, "run_mcp_server.py")

    # Ensure environment variables are passed to the subprocess
    env = os.environ.copy()
    server_params = StdioServerParameters(command="python", args=[server_script], env=env)

    try:
        print("🔌 Connecting to MCP server...")

        # Connect to the server
        async with stdio_client(server_params) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                # Initialize the session
                await session.initialize()
                print("✅ Connected to MCP server")

                # List available tools
                response = await session.list_tools()
                tools = response.tools
                print(f"✅ Found {len(tools)} tools")

                # Find the specific tool
                target_tool = None
                for tool in tools:
                    if tool.name == TOOL_TO_TEST:
                        target_tool = tool
                        break

                if not target_tool:
                    print(f"❌ Tool '{TOOL_TO_TEST}' not found!")
                    print("Available tools:")
                    for tool in tools:
                        print(f"  - {tool.name}")
                    return False

                # Show tool details
                print(f"\n🔍 Testing tool: {target_tool.name}")
                print(f"📝 Description: {target_tool.description or 'No description'}")
                print(f"📋 Input Schema: {target_tool.inputSchema}")

                # Show expected parameters
                if isinstance(target_tool.inputSchema, dict) and "properties" in target_tool.inputSchema:
                    print("\n📊 Expected parameters:")
                    required = target_tool.inputSchema.get("required", [])
                    for param_name, param_info in target_tool.inputSchema["properties"].items():
                        param_type = param_info.get("type", "unknown")
                        is_required = param_name in required
                        req_str = " (required)" if is_required else " (optional)"
                        print(f"  - {param_name}: {param_type}{req_str}")

                # Test the tool
                print(f"\n🧪 Testing with arguments: {TEST_ARGS}")

                try:
                    result = await session.call_tool(TOOL_TO_TEST, TEST_ARGS)
                    print("✅ Tool call successful!")

                    # Parse and display result
                    result_text = result.content[0].text
                    print(f"\n📄 Raw result: {result_text}")

                    try:
                        # Try to parse as JSON for better formatting
                        result_data = json.loads(result_text)
                        if isinstance(result_data, dict):
                            print("\n📊 Parsed result:")
                            if "error" in result_data:
                                print(f"  ⚠️ Error: {result_data['error']}")
                            else:
                                print(f"  📋 Result keys: {list(result_data.keys())}")

                                # Show detailed content
                                for key, value in result_data.items():
                                    if isinstance(value, str | int | float | bool):
                                        print(f"    {key}: {value}")
                                    elif isinstance(value, list):
                                        print(f"    {key}: List with {len(value)} items")
                                        if value and len(value) > 0:
                                            print(f"      First item: {str(value[0])[:100]}...")
                                    elif isinstance(value, dict):
                                        print(f"    {key}: Dict with keys: {list(value.keys())}")
                                    else:
                                        print(f"    {key}: {type(value).__name__}")
                        else:
                            print(f"\n📄 Non-dict result: {result_data}")

                    except json.JSONDecodeError:
                        print("\n📄 Non-JSON result (showing first 500 chars):")
                        print(result_text[:500])
                        if len(result_text) > 500:
                            print("...")

                    return True

                except Exception as e:
                    print(f"❌ Tool call failed: {e}")

                    # Try to provide helpful debugging info
                    if "validation error" in str(e).lower():
                        print("\n💡 This looks like a parameter validation error.")
                        print("Check that your TEST_ARGS match the expected schema above.")

                    return False

    except Exception as e:
        print(f"❌ Failed to connect to MCP server: {e}")
        return False


if __name__ == "__main__":
    print(f"🧪 Testing single tool: {TOOL_TO_TEST}")
    print(f"📋 Test arguments: {TEST_ARGS}")
    print("-" * 50)

    success = asyncio.run(test_single_tool())

    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!")
        print("\n💡 To test a different tool:")
        print("1. Edit the TOOL_TO_TEST variable at the top of this script")
        print("2. Update the TEST_ARGS with appropriate parameters")
        print("3. Run the script again")

    sys.exit(0 if success else 1)

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
