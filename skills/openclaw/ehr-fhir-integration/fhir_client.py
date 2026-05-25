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
fhir_client.py

A command-line tool and Python library for interacting with HL7 FHIR servers.
Part of the Biomedical OS Skills Library.
"""

import argparse
import json
import os
import sys
from typing import Optional, List, Dict, Any

try:
    from fhir.resources.patient import Patient
    from fhir.resources.bundle import Bundle
    import fhirpy
except ImportError:
    # Fallback for environments without dependencies installed
    # We will just print a message if run directly, or mocking for strict envs
    pass

def get_client(url: str, token: Optional[str] = None):
    """Initializes and returns a FHIR client."""
    try:
        return fhirpy.SyncFHIRClient(
            url=url,
            authorization=f"Bearer {token}" if token else None
        )
    except NameError:
        print("Error: 'fhirpy' not installed. Please install with: pip install fhirpy")
        sys.exit(1)

def search_resource(
    client, 
    resource_type: str, 
    search_params: str
) -> List[Dict[str, Any]]:
    """
    Searches for resources of a given type.
    search_params should be a query string like 'name=Smith&active=true'
    """
    # Parse query string into dict
    params = {}
    if search_params:
        for pair in search_params.split('&'):
            if '=' in pair:
                key, value = pair.split('=', 1)
                params[key] = value
    
    print(f"Searching {resource_type} with params: {params}...")
    
    try:
        resources = client.resources(resource_type).search(**params).fetch_all()
        return [r.serialize() for r in resources]
    except Exception as e:
        print(f"Error searching resources: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="FHIR Client for Biomedical OS")
    parser.add_argument("--server", required=True, help="FHIR server base URL")
    parser.add_argument("--resource", required=True, help="FHIR resource type (e.g., Patient, Observation)")
    parser.add_argument("--search", help="Search parameters (key=value&key2=val2)")
    parser.add_argument("--token", help="Bearer token for authentication")
    parser.add_argument("--output", help="Output file path (JSON)")
    
    args = parser.parse_args()
    
    # Check dependencies
    if 'fhirpy' not in sys.modules:
        print("Warning: 'fhirpy' module not found. Install it to run this script.")
        print("pip install fhirpy fhir.resources")
        # For demonstration purposes in a restricted env, we might mock output if requested
        # But properly we should exit or fail.
        # We'll continue to try to init the client which handles the error.

    client = get_client(args.server, args.token)
    
    results = search_resource(client, args.resource, args.search)
    
    print(f"Found {len(results)} resources.")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Results saved to {args.output}")
    else:
        print(json.dumps(results, indent=2, default=str))

if __name__ == "__main__":
    main()

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
