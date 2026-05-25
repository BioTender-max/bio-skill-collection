# Arrow Flight (Python)

This guide documents the JGI Lakehouse Arrow Flight Python setup described by Georg Rath (Nov 26, 2025), and a validated local test run.

## Purpose

Use Arrow Flight for fast programmatic query access to Dremio/Lakehouse when you want lower-overhead retrieval than REST.

## Prerequisites

- Network access to `lakehouse-1.jgi.lbl.gov`
- Valid lakehouse credentials
- Python 3 with `venv`

## Quick Start (Username/Password)

```bash
python3 -m venv venv
. venv/bin/activate
pip install \
  https://github.com/dremio-hub/arrow-flight-client-examples/releases/download/dremio-flight-python-v1.1.0/dremio_flight-1.1.0-py3-none-any.whl
```

Create `config.yaml`:

```yaml
hostname: lakehouse-1.jgi.lbl.gov
username: my_user
password: my_password
query: SELECT 1
```

Create `example.py`:

```python
import logging
import yaml
from dremio.flight.connection import DremioFlightEndpointConnection

logging.basicConfig(level=logging.INFO)

with open("config.yaml", "r", encoding="utf-8") as fh:
    cfg = yaml.safe_load(fh)

conn = DremioFlightEndpointConnection({
    "hostname": cfg["hostname"],
    "username": cfg["username"],
    "password": cfg["password"],
})
df = conn.query(cfg["query"])
print(df)
```

Run:

```bash
python example.py
```

Expected output shape:

```text
INFO:root:Authentication was successful
INFO:root:GetFlightInfo was successful
   EXPR$0
0       1
```

## PAT/Token Note

If your environment uses Personal Access Tokens (`DREMIO_PAT`) for REST, keep in mind this example is username/password-based. If token auth is required for Flight in your deployment, adapt connection parameters according to the installed package API.

## Operational Notes

- Default Flight port in this package flow is `32010` unless overridden.
- Keep credentials out of git. Do not commit `config.yaml` with real usernames/passwords/tokens.
- Prefer short-lived or scoped credentials where possible.

## References

- Arrow Flight client examples: https://github.com/dremio-hub/arrow-flight-client-examples
- Dremio Arrow Flight docs: https://docs.dremio.com/current/developer/arrow-flight/
