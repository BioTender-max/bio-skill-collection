# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

"""Adapter for using centralized HTTP client with cBioPortal API.

This module provides a thin wrapper around the centralized HTTP client
specifically for cBioPortal API calls. It handles:
- Authorization header injection for authenticated requests
- Consistent error handling and response formatting
- Endpoint-specific caching and rate limiting
- Seamless migration from direct httpx usage

Example:
    adapter = CBioHTTPAdapter()
    data, error = await adapter.get("/genes/BRAF")
    if error:
        print(f"Failed to fetch gene: {error}")
    else:
        print(f"Gene ID: {data.get('entrezGeneId')}")
"""

import json
from typing import Any

from ..http_client import RequestError, request_api
from ..variants.constants import CBIO_BASE_URL, CBIO_TOKEN


class CBioHTTPAdapter:
    """Adapter for cBioPortal API calls using centralized HTTP client."""

    def __init__(self):
        self.base_url = CBIO_BASE_URL
        self.headers = self._build_headers()

    def _build_headers(self) -> dict[str, str]:
        """Build authorization headers if token is available."""
        headers = {}
        if CBIO_TOKEN:
            if not CBIO_TOKEN.startswith("Bearer "):
                headers["Authorization"] = f"Bearer {CBIO_TOKEN}"
            else:
                headers["Authorization"] = CBIO_TOKEN
        return headers

    async def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        endpoint_key: str = "cbioportal_api",
        cache_ttl: int = 900,  # 15 minutes default
    ) -> tuple[dict[str, Any] | None, RequestError | None]:
        """Make a GET request to cBioPortal API.

        Args:
            path: API path (e.g., "/genes/BRAF")
            params: Query parameters
            endpoint_key: Registry key for endpoint tracking
            cache_ttl: Cache time-to-live in seconds

        Returns:
            Tuple of (response_data, error)
        """
        url = f"{self.base_url}{path}"

        # Prepare request with headers
        request_params = params or {}
        if self.headers:
            # Need to pass headers through params for centralized client
            request_params["_headers"] = json.dumps(self.headers)

        result, error = await request_api(
            url=url,
            request=request_params,
            method="GET",
            domain="cbioportal",  # For rate limiting
            endpoint_key=endpoint_key,
            cache_ttl=cache_ttl,
            enable_retry=True,
        )

        return result, error

    async def post(
        self,
        path: str,
        data: dict[str, Any],
        endpoint_key: str = "cbioportal_api",
        cache_ttl: int = 0,  # No caching for POST by default
    ) -> tuple[dict[str, Any] | None, RequestError | None]:
        """Make a POST request to cBioPortal API.

        Args:
            path: API path
            data: Request body data
            endpoint_key: Registry key for endpoint tracking
            cache_ttl: Cache time-to-live in seconds

        Returns:
            Tuple of (response_data, error)
        """
        url = f"{self.base_url}{path}"

        # Add headers to request
        if self.headers:
            data["_headers"] = json.dumps(self.headers)

        result, error = await request_api(
            url=url,
            request=data,
            method="POST",
            domain="cbioportal",
            endpoint_key=endpoint_key,
            cache_ttl=cache_ttl,
            enable_retry=True,
        )

        return result, error

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
