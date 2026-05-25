#!/bin/bash
#
# Explore GOLD database in JGI Lakehouse
# Run this from LBNL server where lakehouse-1.jgi.lbl.gov:9047 is accessible
#

set -euo pipefail

export DREMIO_PAT="${DREMIO_PAT:-$(cat ~/.secrets/dremio_pat 2>/dev/null)}"

if [ -z "$DREMIO_PAT" ]; then
  echo "ERROR: DREMIO_PAT not set"
  echo "Run: export DREMIO_PAT=$(cat ~/.secrets/dremio_pat)"
  exit 1
fi

DREMIO_HOST="${DREMIO_HOST:-lakehouse-1.jgi.lbl.gov}"
DREMIO_PORT="${DREMIO_PORT:-9047}"
BASE_URL="https://${DREMIO_HOST}:${DREMIO_PORT}/api/v3"

echo "════════════════════════════════════════════════════════════════"
echo "JGI GOLD Database Explorer"
echo "════════════════════════════════════════════════════════════════"
echo "Endpoint: $BASE_URL"
echo "Token: ${DREMIO_PAT:0:20}..."
echo ""

# Helper function to execute SQL
execute_sql() {
  local sql="$1"
  echo "  Query: ${sql:0:80}..." >&2

  # Submit job
  local job_response=$(curl -s --insecure -X POST "$BASE_URL/sql" \
    -H "Authorization: Bearer $DREMIO_PAT" \
    -H "Content-Type: application/json" \
    -d "{\"sql\": \"$sql\"}")

  local job_id=$(echo "$job_response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)

  if [ -z "$job_id" ]; then
    echo "ERROR: No job ID returned" >&2
    echo "$job_response" >&2
    return 1
  fi

  # Wait a moment for job to complete
  sleep 1

  # Get results
  curl -s --insecure -X GET "$BASE_URL/job/$job_id/results?limit=500" \
    -H "Authorization: Bearer $DREMIO_PAT" \
    -H "Content-Type: application/json"
}

# Step 1: List all schemas
echo "1. Listing all available schemas..."
echo "────────────────────────────────────────────────────────────────"
SCHEMAS=$(execute_sql "SHOW SCHEMAS")
echo "$SCHEMAS" | python3 << 'EOF'
import sys, json
data = json.load(sys.stdin)
rows = data.get("rows", [])
schemas = [r.get("SCHEMA_NAME") for r in rows]
print(f"Found {len(schemas)} schemas:")
for s in schemas:
    print(f"  - {s}")

# Check for GOLD
if "GOLD" in schemas:
    print("\n✓ GOLD schema found!")
else:
    print("\n✗ GOLD schema not found")
    gold_like = [s for s in schemas if 'gold' in s.lower()]
    if gold_like:
        print("  Schemas containing 'gold':")
        for s in gold_like:
            print(f"    - {s}")
EOF
echo ""

# Step 2: List GOLD tables
echo "2. Listing tables in GOLD schema..."
echo "────────────────────────────────────────────────────────────────"
TABLES=$(execute_sql "SHOW TABLES IN GOLD" 2>&1)

if echo "$TABLES" | grep -q "error\|ERROR"; then
  echo "  Trying alternative query..."
  TABLES=$(execute_sql "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.\"TABLES\" WHERE TABLE_SCHEMA = 'GOLD'" 2>&1)
fi

echo "$TABLES" | python3 << 'EOF'
import sys, json
try:
    data = json.load(sys.stdin)
    rows = data.get("rows", [])
    tables = [r.get("TABLE_NAME", r.get("table_name", "?")) for r in rows]
    print(f"Found {len(tables)} tables in GOLD:")
    for t in tables:
        print(f"  - {t}")

    # Store for next step
    with open("/tmp/gold_tables.txt", "w") as f:
        f.write("\n".join(tables))
except Exception as e:
    print(f"ERROR parsing tables: {e}")
    sys.exit(1)
EOF
echo ""

# Step 3: Describe each table
echo "3. Exploring GOLD tables (first 5)..."
echo "────────────────────────────────────────────────────────────────"

if [ -f /tmp/gold_tables.txt ]; then
  head -5 /tmp/gold_tables.txt | while read table; do
    [ -z "$table" ] && continue

    echo ""
    echo "Table: GOLD.$table"
    echo "  ──────────────────────────────────────────────────────────"

    # Get schema
    SCHEMA=$(execute_sql "DESCRIBE GOLD.$table" 2>&1)
    echo "$SCHEMA" | python3 << EOF
import sys, json
try:
    data = json.load(sys.stdin)
    rows = data.get("rows", [])
    print(f"  Columns: {len(rows)}")
    for col in rows[:15]:
        name = col.get("COLUMN_NAME", "?")
        dtype = col.get("DATA_TYPE", "?")
        print(f"    - {name}: {dtype}")
    if len(rows) > 15:
        print(f"    ... and {len(rows) - 15} more columns")
except Exception as e:
    print(f"  ERROR: {e}")
EOF

    # Get row count
    COUNT=$(execute_sql "SELECT COUNT(*) as cnt FROM GOLD.$table" 2>&1)
    echo "$COUNT" | python3 << 'EOF'
import sys, json
try:
    data = json.load(sys.stdin)
    rows = data.get("rows", [])
    if rows:
        count = rows[0].get("cnt", "?")
        print(f"  Row count: {count:,}" if isinstance(count, int) else f"  Row count: {count}")
except:
    print("  Row count: (unable to determine)")
EOF

    # Get sample
    SAMPLE=$(execute_sql "SELECT * FROM GOLD.$table LIMIT 2" 2>&1)
    echo "$SAMPLE" | python3 << 'EOF'
import sys, json
try:
    data = json.load(sys.stdin)
    rows = data.get("rows", [])
    print(f"  Sample data ({len(rows)} rows):")
    for i, row in enumerate(rows, 1):
        # Show first few fields
        items = list(row.items())[:5]
        print(f"    Row {i}:")
        for k, v in items:
            val_str = str(v)[:50]
            print(f"      {k}: {val_str}")
        if len(row) > 5:
            print(f"      ... and {len(row) - 5} more fields")
except:
    print("  Sample: (unable to retrieve)")
EOF

  done
else
  echo "  ERROR: No tables found"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "Exploration Complete!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "All GOLD tables:"
cat /tmp/gold_tables.txt 2>/dev/null || echo "(none found)"
echo ""
