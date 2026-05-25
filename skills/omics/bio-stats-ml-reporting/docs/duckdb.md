# DuckDB Usage Guide

**Official Documentation:** https://duckdb.org/docs/stable/

**Version:** 1.4.3

## Installation

```bash
# Via pip
pip install duckdb

# Via conda
conda install -c conda-forge duckdb

# CLI installation (download from duckdb.org/docs/stable/installation/)
```

## Key Command-Line Flags

```bash
duckdb [OPTIONS] [FILENAME]
```

**Common Options:**
- `-csv` - Set output mode to CSV format
- `-json` - Set output mode to JSON format
- `-readonly` - Open database in read-only mode
- `-init <file>` - Specify custom initialization file (default: ~/.duckdbrc)
- `-c <command>` - Execute SQL command and exit

## Common Usage Examples

### Launch Interactive Shell

```bash
# In-memory database
duckdb

# Persistent database
duckdb results.duckdb

# Read-only mode
duckdb -readonly results.duckdb
```

### Execute SQL from Command Line

```bash
# Single query
duckdb :memory: "SELECT 42 AS answer"

# From file
duckdb < analysis.sql

# Pipe data
cat data.csv | duckdb -c "SELECT * FROM read_csv('/dev/stdin')"
```

### Working with Parquet Files

```sql
-- Read single file
SELECT * FROM 'results/output.parquet';

-- Multiple files with glob pattern
SELECT * FROM 'results/*.parquet';

-- With filename tracking
SELECT *, filename FROM read_parquet('results/*.parquet');

-- Remote files
SELECT * FROM read_parquet('https://example.com/data.parquet');

-- Write with compression
COPY (SELECT * FROM results)
TO 'output.parquet'
(FORMAT parquet, COMPRESSION zstd);
```

### Working with TSV/CSV Files

```sql
-- Auto-detect format
SELECT * FROM 'metadata.tsv';

-- Explicit read
SELECT * FROM read_csv('metadata.tsv', delim='\t', header=true);

-- Write TSV
COPY (SELECT * FROM results)
TO 'output.tsv'
(FORMAT csv, DELIMITER '\t', HEADER true);
```

### Join and Aggregate Operations

```sql
-- Join Parquet outputs with metadata
SELECT
    r.*,
    m.sample_group,
    m.condition
FROM 'results/*.parquet' r
JOIN read_csv('metadata.tsv', delim='\t') m
    ON r.sample_id = m.sample_id;

-- Aggregate statistics
SELECT
    sample_group,
    COUNT(*) as n_samples,
    AVG(metric_value) as mean_value,
    STDDEV(metric_value) as sd_value
FROM joined_results
GROUP BY sample_group;
```

## Input/Output Formats

**Supported Input:**
- Parquet (native, recommended for large datasets)
- CSV/TSV (with auto-detection)
- JSON (line-delimited or standard)
- Excel (via extension)
- Arrow IPC

**Supported Output:**
- All input formats
- Multiple output modes: csv, json, markdown, latex, insert statements

## Performance Tips

**1. Use Parquet for Large Datasets**
- Native columnar format with automatic projection/filter pushdown
- Compress with zstd for good balance of speed and size
- Configure row group size (default: 122,880 rows)

**2. Optimize Queries**
- DuckDB automatically parallelizes queries
- Use projection pushdown (SELECT only needed columns)
- Apply filters early in query pipeline

**3. Memory Management**
- DuckDB can handle datasets larger than RAM
- Adjust memory limit: `SET memory_limit='8GB';`
- Use persistent database files for large intermediate results

**4. Batch Operations**
- Use `COPY` instead of `INSERT` for bulk loading
- Leverage glob patterns to process multiple files efficiently

**5. Compression Options**
```sql
-- Best compression (slower)
COMPRESSION zstd

-- Fastest (moderate compression)
COMPRESSION lz4

-- Default (good balance)
COMPRESSION snappy
```

## Common Dot Commands

Execute inside interactive shell:

```sql
.open results.duckdb          -- Open/switch database
.mode csv                      -- Change output format
.output results.csv           -- Direct output to file
.read script.sql              -- Execute SQL from file
.schema table_name            -- Show table schema
.tables                       -- List all tables
.help                         -- Show all commands
```

## Typical Workflow for Bio Stats

```bash
# 1. Start DuckDB with database file
duckdb results/analysis.duckdb

# 2. Load and join results
CREATE TABLE merged_results AS
SELECT * FROM read_parquet('results/*.parquet');

CREATE TABLE metadata AS
SELECT * FROM read_csv('metadata.tsv', delim='\t');

CREATE TABLE features AS
SELECT
    m.*,
    r.expression_level,
    r.fold_change,
    r.p_value
FROM metadata m
JOIN merged_results r ON m.sample_id = r.sample_id;

# 3. Export feature table
COPY features TO 'results/features.parquet' (FORMAT parquet);

# 4. Generate summary statistics
COPY (
    SELECT
        condition,
        COUNT(*) as n,
        AVG(expression_level) as mean_expr,
        STDDEV(expression_level) as sd_expr
    FROM features
    GROUP BY condition
) TO 'results/summary_stats.tsv' (FORMAT csv, DELIMITER '\t');
```

## References

- Official Docs: https://duckdb.org/docs/stable/
- CLI Reference: https://duckdb.org/docs/stable/clients/cli/overview.html
- Parquet Guide: https://duckdb.org/docs/stable/data/parquet/overview.html
- Performance Guide: https://duckdb.org/docs/stable/guides/performance/overview.html
