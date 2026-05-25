# How to Explore GOLD Database

## Current Limitation

Your workstation (`jgi-ont.tailfd4067.ts.net`) **cannot access** the Dremio API directly due to network restrictions:
- Port 9047 is blocked/firewalled
- Public HTTPS endpoint has Cloudflare Access protection

## Solution: Run from LBNL Server

You need to run the exploration script from the **same LBNL server** where you generated the token.

### Step 1: Copy Files to LBNL Server

```bash
# From your workstation, copy the exploration script
scp scripts/explore_gold_database.sh <lbnl-server>:~/
scp ~/.secrets/dremio_pat <lbnl-server>:~/.secrets/
```

### Step 2: SSH to LBNL Server

```bash
ssh <lbnl-server>
```

### Step 3: Run the Exploration Script

```bash
# Set the token
export DREMIO_PAT=$(cat ~/.secrets/dremio_pat)

# Run the exploration
bash ~/explore_gold_database.sh > gold_exploration_results.txt 2>&1

# View results
cat gold_exploration_results.txt
```

## What the Script Does

The script will:

1. **List all available schemas** in the lakehouse
2. **Find the GOLD database** (or similar)
3. **List all tables** in GOLD
4. **For each table**, show:
   - Column names and data types
   - Row count
   - Sample data (first 2 rows)

## Alternative: Manual Exploration

If you prefer to explore manually, here are the SQL commands:

```bash
# Set token
export DREMIO_PAT=$(cat ~/.secrets/dremio_pat)
BASE_URL="http://lakehouse-1.jgi.lbl.gov:9047/api/v3"

# Helper function
run_query() {
  local sql="$1"
  local job=$(curl -s --insecure -X POST "$BASE_URL/sql" \
    -H "Authorization: Bearer $DREMIO_PAT" \
    -H "Content-Type: application/json" \
    -d "{\"sql\": \"$sql\"}")

  local job_id=$(echo "$job" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")

  sleep 1

  curl -s --insecure "$BASE_URL/job/$job_id/results?limit=100" \
    -H "Authorization: Bearer $DREMIO_PAT" | python3 -m json.tool
}

# List all schemas
run_query "SHOW SCHEMAS"

# List GOLD tables
run_query "SHOW TABLES IN GOLD"

# Describe a specific table
run_query "DESCRIBE GOLD.PROJECT"

# Sample data from a table
run_query "SELECT * FROM GOLD.PROJECT LIMIT 5"
```

## Expected Output

You should see something like:

```
════════════════════════════════════════════════════════════════
JGI GOLD Database Explorer
════════════════════════════════════════════════════════════════

1. Listing all available schemas...
────────────────────────────────────────────────────────────────
Found 15 schemas:
  - GOLD
  - Phytozome
  - Mycocosm
  - JDP
  - IMG
  ...

✓ GOLD schema found!

2. Listing tables in GOLD schema...
────────────────────────────────────────────────────────────────
Found 12 tables in GOLD:
  - PROJECT
  - BIOSAMPLE
  - ORGANISM
  - SEQUENCING_PROJECT
  - ANALYSIS_PROJECT
  ...

3. Exploring GOLD tables...
────────────────────────────────────────────────────────────────

Table: GOLD.PROJECT
  ──────────────────────────────────────────────────────────
  Columns: 25
    - PROJECT_ID: VARCHAR
    - PROJECT_NAME: VARCHAR
    - ORGANISM_NAME: VARCHAR
    - ECOSYSTEM: VARCHAR
    - HABITAT: VARCHAR
    ...
  Row count: 125,431
  Sample data (2 rows):
    Row 1:
      PROJECT_ID: Gp0123456
      PROJECT_NAME: Marine metagenome sequencing
      ORGANISM_NAME: Marine microbial communities
      ...
```

## Common GOLD Tables

Based on typical GOLD structure, you might find:

- **PROJECT** - Research projects
- **BIOSAMPLE** - Biological samples
- **ORGANISM** - Organism information
- **SEQUENCING_PROJECT** - Sequencing efforts
- **ANALYSIS_PROJECT** - Analysis workflows
- **STUDY** - Study metadata

## Saving Results

To save the results for later analysis:

```bash
# Run and save
bash ~/explore_gold_database.sh > ~/gold_data_catalog.txt 2>&1

# Copy back to your workstation
# From your workstation:
scp <lbnl-server>:~/gold_data_catalog.txt ~/

# Then analyze locally
cat ~/gold_data_catalog.txt
```

## Troubleshooting

**Error: "No route to host"**
→ You're not on the LBNL network. Make sure you're SSH'd into the correct server.

**Error: "Unauthorized" or "401"**
→ Token might be expired (30 hour lifetime). Regenerate using the admin's script.

**Error: "GOLD schema not found"**
→ The schema might have a different name. Check the schema list for variations like "Gold", "gold", etc.

**No output**
→ Check that curl and python3 are available on the LBNL server

## Next Steps

After exploring the GOLD database:

1. **Identify tables of interest** for your analysis
2. **Document the schema** for the tables you need
3. **Create queries** to extract specific data
4. **Consider setting up** an SSH tunnel or scheduled exports if you need regular access

---

**Script Location**: `scripts/explore_gold_database.sh`
**Token**: Stored in `~/.secrets/dremio_pat` (30 hour lifetime)
