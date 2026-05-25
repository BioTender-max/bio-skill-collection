# Lakehouse Scripts

Core scripts for JGI Lakehouse access and data exploration.

## Available Scripts

### `get_dremio_token.sh`
Generate authentication token from username/password.

**Usage:**
```bash
# Interactive (prompts for password)
./get_dremio_token.sh

# Non-interactive
./get_dremio_token.sh username password

# Store in environment
export DREMIO_PAT=$(./get_dremio_token.sh username password)
```

**Requirements:**
- Must run from LBNL network (port 9047 access)
- Token lifetime: 30 hours

### `rest_client.py`
Python REST API client for Dremio.

**Usage:**
```python
from rest_client import query, show_schemas, list_catalogs

# List schemas
schemas = show_schemas(limit=2000)

# Execute SQL
results = query("SELECT * FROM GOLD.PROJECT LIMIT 10")

# With context
results = query(
    "SELECT * FROM genomics LIMIT 10",
    context=["Phytozome"]
)
```

**Requirements:**
- DREMIO_PAT environment variable
- LBNL network access (or SSH tunnel)

**Important behavior:**
- `rest_client` resolves `DREMIO_PAT` at call time. Set/export token before query calls.
- `show_schemas()` should use a high limit (for example `2000`) to avoid truncation.

### Arrow Flight Python Example (Optional)
For a performant Arrow Flight workflow, see:

- `../docs/arrow-flight-python.md`

This includes:
- venv setup
- wheel install command
- `config.yaml` + `example.py`
- `SELECT 1` connectivity check

### `explore_gold_database.sh`
Comprehensive GOLD database exploration script.

**Usage:**
```bash
export DREMIO_PAT=$(cat ~/.secrets/dremio_pat)
bash explore_gold_database.sh > gold_catalog.txt
```

**Output:**
- All available schemas
- All GOLD tables
- Column schemas and types
- Row counts
- Sample data

### `download_img_genomes.py`
Download genomes with IMG taxon OIDs from JGI filesystem.

**Usage:**
```bash
export DREMIO_PAT=$(cat ~/.secrets/dremio_pat)
python download_img_genomes.py --domain Bacteria --limit 5 --output ./genomes
```

**Features:**
- Queries Lakehouse for genomes matching criteria
- Checks file availability on JGI filesystem
- Downloads/extracts genome packages
- Returns metadata with taxon OIDs

**Requirements:**
- DREMIO_PAT environment variable
- JGI cluster account with filesystem access
- Access to `/clusterfs/jgi/img_merfs-ro/`

## Authentication Setup

### 1. Generate Token (from LBNL server)

```bash
ssh <lbnl-server>
cd ~/.agents/skills/jgi-lakehouse/scripts
./get_dremio_token.sh username password
```

### 2. Store Token Securely

```bash
# On your workstation
echo "your-token" > ~/.secrets/dremio_pat
chmod 600 ~/.secrets/dremio_pat
```

### 3. Auto-Load Token

```bash
echo 'export DREMIO_PAT=$(cat ~/.secrets/dremio_pat 2>/dev/null)' >> ~/.bashrc
source ~/.bashrc
```

## Network Access

**Internal HTTP** (REST API)
```
http://lakehouse-1.jgi.lbl.gov:9047/api/v3
✅ Works with token
⚠️ LBNL network only
```

**Public HTTPS**
```
https://lakehouse.jgi.lbl.gov/api/v3
❌ Blocked by Cloudflare Access
```

## Using REST API

```python
import os
import requests

BASE_URL = "http://lakehouse-1.jgi.lbl.gov:9047/api/v3"
TOKEN = os.getenv("DREMIO_PAT")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Submit SQL
response = requests.post(
    f"{BASE_URL}/sql",
    headers=headers,
    json={"sql": "SHOW SCHEMAS"},
    verify=False
)
job_id = response.json()["id"]

# Get results
response = requests.get(
    f"{BASE_URL}/job/{job_id}/results",
    headers=headers,
    params={"limit": 100}
)
results = response.json()["rows"]
```

## Token Management

**Storage:** `~/.secrets/dremio_pat`
**Lifetime:** 30 hours
**Refresh:** Re-run `get_dremio_token.sh`

**Security:**
- Never commit tokens to git
- Use 600 permissions on token file
- Gitignore ~/.secrets/ directory

## Troubleshooting

**"No route to host"**
→ Port 9047 blocked. Run from LBNL network or use SSH tunnel.

**"HTTP 302"**
→ Cloudflare Access blocking. Use internal endpoint.

**"ModuleNotFoundError: requests"**
→ `pip install requests` or use pixi environment.
