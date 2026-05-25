#!/usr/bin/env python3
"""
Dremio REST API Client for JGI Lakehouse
Uses internal HTTP endpoint (requires LBNL network access)
"""

import os
import time
import requests
from typing import Dict, List, Any, Optional

# Configuration
DREMIO_HOST = os.getenv("DREMIO_HOST", "lakehouse-1.jgi.lbl.gov")
DREMIO_PORT = os.getenv("DREMIO_PORT", "9047")
DREMIO_BASE_URL = f"https://{DREMIO_HOST}:{DREMIO_PORT}/api/v3"

# Default timeout for job polling (seconds)
DEFAULT_JOB_TIMEOUT = 300


def _get_token() -> str:
    """
    Resolve token at call time.

    This avoids stale-token bugs when users set DREMIO_PAT after importing
    this module.
    """
    token = os.getenv("DREMIO_PAT")
    if not token:
        raise ValueError("DREMIO_PAT environment variable not set")
    return token


def _get_headers() -> Dict[str, str]:
    """Get headers for API requests"""
    return {
        "Authorization": f"Bearer {_get_token()}",
        "Content-Type": "application/json"
    }


def execute_sql(sql: str, context: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Execute SQL query and return job information

    Args:
        sql: SQL query to execute
        context: Optional context path (e.g., ["Phytozome", "genomics"])

    Returns:
        dict with job id and status
    """
    url = f"{DREMIO_BASE_URL}/sql"

    payload = {"sql": sql}
    if context:
        payload["context"] = context

    response = requests.post(url, headers=_get_headers(), json=payload, verify=False)
    response.raise_for_status()

    return response.json()


def get_job_status(job_id: str) -> Dict[str, Any]:
    """
    Get job status

    Args:
        job_id: Job ID from execute_sql

    Returns:
        dict with jobState and other metadata
    """
    url = f"{DREMIO_BASE_URL}/job/{job_id}"
    response = requests.get(url, headers=_get_headers(), verify=False)
    response.raise_for_status()
    return response.json()


def wait_for_job(job_id: str, timeout: int = DEFAULT_JOB_TIMEOUT, poll_interval: float = 1.0) -> Dict[str, Any]:
    """
    Poll job status until completion or timeout

    Args:
        job_id: Job ID to poll
        timeout: Maximum seconds to wait
        poll_interval: Seconds between polls

    Returns:
        Final job status dict

    Raises:
        TimeoutError: If job doesn't complete within timeout
        RuntimeError: If job fails or is canceled
    """
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout:
            raise TimeoutError(f"Job {job_id} did not complete within {timeout}s")

        status = get_job_status(job_id)
        job_state = status.get("jobState")

        if job_state == "COMPLETED":
            return status
        elif job_state in ("FAILED", "CANCELED", "CANCELLED"):
            error_msg = status.get("errorMessage", "Unknown error")
            raise RuntimeError(f"Job {job_state}: {error_msg}")

        time.sleep(poll_interval)


def get_job_results(job_id: str, offset: int = 0, limit: int = 100) -> Dict[str, Any]:
    """
    Get results from a completed job

    Args:
        job_id: Job ID from execute_sql
        offset: Starting row offset
        limit: Maximum rows to return (max 500)

    Returns:
        dict with rows and metadata
    """
    url = f"{DREMIO_BASE_URL}/job/{job_id}/results"
    params = {"offset": offset, "limit": min(limit, 500)}

    response = requests.get(url, headers=_get_headers(), params=params, verify=False)
    response.raise_for_status()

    return response.json()


def query(
    sql: str,
    context: Optional[List[str]] = None,
    limit: int = 100,
    timeout: int = DEFAULT_JOB_TIMEOUT
) -> List[Dict[str, Any]]:
    """
    Execute SQL query and return results (with job polling)

    Args:
        sql: SQL query
        context: Optional context path
        limit: Maximum rows to return
        timeout: Maximum seconds to wait for query completion

    Returns:
        list of row dictionaries
    """
    # Submit query
    job_info = execute_sql(sql, context)
    job_id = job_info.get("id")

    if not job_id:
        raise ValueError(f"No job ID in response: {job_info}")

    # Wait for completion
    wait_for_job(job_id, timeout=timeout)

    # Get results
    results = get_job_results(job_id, offset=0, limit=limit)

    return results.get("rows", [])


def query_all(
    sql: str,
    context: Optional[List[str]] = None,
    timeout: int = DEFAULT_JOB_TIMEOUT,
    batch_size: int = 500
) -> List[Dict[str, Any]]:
    """
    Execute SQL query and return ALL results (auto-pagination)

    Args:
        sql: SQL query
        context: Optional context path
        timeout: Maximum seconds to wait for query completion
        batch_size: Rows per page (max 500)

    Returns:
        list of all row dictionaries
    """
    # Submit query
    job_info = execute_sql(sql, context)
    job_id = job_info.get("id")

    if not job_id:
        raise ValueError(f"No job ID in response: {job_info}")

    # Wait for completion
    status = wait_for_job(job_id, timeout=timeout)
    total_rows = status.get("rowCount", 0)

    # Paginate through results
    all_rows = []
    offset = 0

    while offset < total_rows:
        results = get_job_results(job_id, offset=offset, limit=batch_size)
        rows = results.get("rows", [])
        if not rows:
            break
        all_rows.extend(rows)
        offset += len(rows)

    return all_rows


def list_catalogs() -> List[Dict[str, Any]]:
    """List available catalogs/sources"""
    url = f"{DREMIO_BASE_URL}/catalog"

    response = requests.get(url, headers=_get_headers(), verify=False)
    response.raise_for_status()

    data = response.json()
    return data.get("data", [])


def get_catalog_item(path: str) -> Dict[str, Any]:
    """
    Get catalog item details

    Args:
        path: Path to catalog item (e.g., "Phytozome.genomics.variants")

    Returns:
        dict with item metadata
    """
    from urllib.parse import quote
    encoded_path = quote(path, safe='')

    url = f"{DREMIO_BASE_URL}/catalog/{encoded_path}"

    response = requests.get(url, headers=_get_headers(), verify=False)
    response.raise_for_status()

    return response.json()


def show_schemas(limit: int = 2000) -> List[str]:
    """
    Convenience method to show all schemas.

    Args:
        limit: Max rows fetched from SHOW SCHEMAS.
               Use a value >100 to avoid truncation.
    """
    results = query("SHOW SCHEMAS", limit=limit)
    return [row.get("SCHEMA_NAME") for row in results if row.get("SCHEMA_NAME")]


# CLI usage
if __name__ == "__main__":
    import sys

    print("Dremio REST API Client Test")
    print("=" * 60)

    token = os.getenv("DREMIO_PAT")
    if not token:
        print("ERROR: DREMIO_PAT environment variable not set")
        print("Run: export DREMIO_PAT=$(cat ~/.secrets/dremio_pat)")
        sys.exit(1)

    print(f"Endpoint: {DREMIO_BASE_URL}")
    print(f"Token: {token[:20]}...")
    print()

    try:
        print("Testing: SHOW SCHEMAS")
        schemas = show_schemas()
        print(f"✓ Found {len(schemas)} schemas:")
        for schema in schemas[:10]:
            print(f"  - {schema}")
        if len(schemas) > 10:
            print(f"  ... and {len(schemas) - 10} more")

        print()
        print("✓ SUCCESS - REST API access is working!")

    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
