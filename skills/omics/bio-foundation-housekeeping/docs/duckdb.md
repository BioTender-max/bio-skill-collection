# DuckDB Usage Guide

## Official Documentation
- URL: https://duckdb.org/docs/
- Version covered: v1.4.3+

## Installation

### Python
```bash
pip install duckdb
```

### Command Line (Universal)
```bash
curl https://install.duckdb.org | sh
```

### Homebrew (macOS)
```bash
brew install duckdb
```

### Docker
```bash
docker run --rm -it -v "$(pwd):/workspace" -w /workspace duckdb/duckdb
```

### Other Languages
```bash
# R
install.packages("duckdb")

# Node.js
npm install @duckdb/node-api

# Rust
cargo add duckdb --features bundled

# Go
go get github.com/duckdb/duckdb-go/v2
```

## Key Commands for Data Cataloging

### Create Database
```python
import duckdb

# In-memory database
conn = duckdb.connect()

# Persistent database
conn = duckdb.connect('catalog.duckdb')
```

### CLI Database Creation
```bash
# Create and open database
duckdb catalog.duckdb

# In-memory
duckdb :memory:
```

### Register Parquet Tables

#### From Python
```python
import duckdb

conn = duckdb.connect('catalog.duckdb')

# Register single Parquet file as table
conn.execute("CREATE TABLE samples AS SELECT * FROM 'data/samples.parquet'")

# Register with view (no copy, query directly)
conn.execute("CREATE VIEW samples AS SELECT * FROM 'data/samples.parquet'")

# Register multiple files as single table
conn.execute("""
    CREATE TABLE all_samples AS
    SELECT * FROM 'data/*.parquet'
""")

# Register with glob pattern
conn.execute("CREATE TABLE runs AS SELECT * FROM 'data/runs/*.parquet'")

# Query directly without registration
results = conn.execute("SELECT * FROM 'data/samples.parquet'").fetchall()
```

#### From CLI
```sql
-- In DuckDB CLI
CREATE TABLE samples AS SELECT * FROM 'data/samples.parquet';

-- Create view
CREATE VIEW samples AS SELECT * FROM 'data/samples.parquet';

-- Multiple files
CREATE TABLE all_samples AS SELECT * FROM read_parquet(['file1.parquet', 'file2.parquet']);

-- Glob pattern
CREATE TABLE runs AS SELECT * FROM 'data/runs/*.parquet';
```

### Query Parquet Files Directly
```sql
-- Query without creating table
SELECT * FROM 'data/samples.parquet' WHERE organism = 'Homo sapiens';

-- Join multiple Parquet files
SELECT s.*, r.run_id
FROM 'data/samples.parquet' s
JOIN 'data/runs.parquet' r ON s.sample_id = r.sample_id;

-- Automatic filename column (since v1.3.0)
SELECT filename, sample_id FROM 'data/*.parquet';
```

### Write Parquet Files
```sql
-- Export query results
COPY (SELECT * FROM samples WHERE coverage > 30)
TO 'results/high_coverage.parquet' (FORMAT parquet);

-- With compression
COPY samples TO 'output.parquet'
(FORMAT parquet, COMPRESSION zstd, ROW_GROUP_SIZE 100000);

-- Export entire database
EXPORT DATABASE 'backup_dir' (FORMAT parquet);
```

### Python API for Parquet
```python
import duckdb

conn = duckdb.connect('catalog.duckdb')

# Read Parquet to DataFrame
df = conn.execute("SELECT * FROM 'data/samples.parquet'").df()

# Write DataFrame to Parquet
conn.execute("COPY (SELECT * FROM samples) TO 'output.parquet' (FORMAT parquet)")

# Register DataFrame as table
conn.register('samples_df', samples_df)
conn.execute("CREATE TABLE samples AS SELECT * FROM samples_df")
```

## Common Usage for Bioinformatics Data Cataloging

### 1. Create Data Catalog Database
```python
import duckdb
from pathlib import Path

# Create catalog
conn = duckdb.connect('data/catalog.duckdb')

# Define schema
conn.execute("""
    CREATE TABLE IF NOT EXISTS samples (
        sample_id VARCHAR PRIMARY KEY,
        sample_name VARCHAR NOT NULL,
        organism VARCHAR NOT NULL,
        tissue VARCHAR,
        collection_date DATE,
        platform VARCHAR,
        read_length INTEGER,
        coverage DOUBLE,
        fastq_r1 VARCHAR,
        fastq_r2 VARCHAR
    )
""")

conn.execute("""
    CREATE TABLE IF NOT EXISTS sequencing_runs (
        run_id VARCHAR PRIMARY KEY,
        sample_id VARCHAR REFERENCES samples(sample_id),
        run_date DATE,
        instrument VARCHAR,
        flowcell VARCHAR,
        lanes INTEGER
    )
""")
```

### 2. Register Parquet Files
```python
# Register sample metadata
conn.execute("CREATE TABLE samples AS SELECT * FROM 'data/samples.parquet'")

# Register QC metrics
conn.execute("CREATE VIEW qc_metrics AS SELECT * FROM 'data/qc/*.parquet'")

# Register variant calls (partitioned by chromosome)
conn.execute("""
    CREATE TABLE variants AS
    SELECT *, filename
    FROM 'data/variants/chr*.parquet'
""")
```

### 3. Query Across Files
```python
# Find high-coverage samples
high_cov = conn.execute("""
    SELECT sample_id, sample_name, coverage
    FROM samples
    WHERE coverage > 30
    ORDER BY coverage DESC
""").df()

# Join samples with QC metrics
results = conn.execute("""
    SELECT s.sample_id, s.sample_name, q.mean_quality, q.duplicate_rate
    FROM samples s
    JOIN qc_metrics q ON s.sample_id = q.sample_id
    WHERE q.mean_quality > 30
""").df()

# Aggregate statistics
stats = conn.execute("""
    SELECT organism, COUNT(*) as n_samples, AVG(coverage) as mean_coverage
    FROM samples
    GROUP BY organism
""").df()
```

### 4. Update Catalog
```python
# Add new samples
conn.execute("""
    INSERT INTO samples
    SELECT * FROM 'data/new_samples.parquet'
""")

# Update existing records
conn.execute("""
    UPDATE samples
    SET coverage = 35.2
    WHERE sample_id = 'S001'
""")
```

### 5. Export Subsets
```python
# Export filtered data
conn.execute("""
    COPY (SELECT * FROM samples WHERE organism = 'Homo sapiens')
    TO 'data/human_samples.parquet' (FORMAT parquet)
""")

# Export aggregated results
conn.execute("""
    COPY (
        SELECT sample_id, COUNT(*) as variant_count
        FROM variants
        GROUP BY sample_id
    )
    TO 'results/variant_counts.parquet' (FORMAT parquet)
""")
```

## Input/Output Formats

### Input Formats
- **Parquet** (native, optimized)
- **CSV/TSV**
- **JSON** (including NDJSON)
- **Excel** (with extensions)
- **Apache Arrow**
- **Pandas DataFrames**

### Output Formats
- **Parquet**
- **CSV/TSV**
- **JSON**
- **Arrow**
- **DataFrames** (Pandas, Polars)

### Read CSV Example
```sql
CREATE TABLE samples AS
SELECT * FROM read_csv('data/samples.csv', AUTO_DETECT=TRUE);
```

### Read JSON Example
```sql
CREATE TABLE metadata AS
SELECT * FROM read_json('data/metadata.json');
```

## Performance Tips

### 1. Use Parquet for Large Datasets
Parquet is columnar and compressed, much faster than CSV:
```python
# Good: Parquet
conn.execute("SELECT * FROM 'data.parquet' WHERE coverage > 30")

# Slower: CSV
conn.execute("SELECT * FROM read_csv('data.csv') WHERE coverage > 30")
```

### 2. Projection Pushdown
Query only needed columns:
```sql
-- Fast: Only reads 2 columns
SELECT sample_id, coverage FROM 'samples.parquet';

-- Slower: Reads all columns
SELECT * FROM 'samples.parquet';
```

### 3. Filter Pushdown
DuckDB automatically pushes filters to Parquet:
```sql
-- Automatically uses Parquet zonemaps
SELECT * FROM 'samples.parquet' WHERE coverage > 30;
```

### 4. Use Views for Large Files
Don't copy data unnecessarily:
```sql
-- Good: No data copy
CREATE VIEW samples AS SELECT * FROM 'data/samples.parquet';

-- Slower: Copies all data
CREATE TABLE samples AS SELECT * FROM 'data/samples.parquet';
```

### 5. Parallel Processing
DuckDB automatically parallelizes queries:
```python
# Set thread count (default: all available)
conn.execute("SET threads TO 8")
```

### 6. Partition Large Datasets
```python
# Write partitioned Parquet
conn.execute("""
    COPY (SELECT * FROM variants)
    TO 'data/variants' (FORMAT parquet, PARTITION_BY (chrom))
""")

# Query specific partitions (faster)
conn.execute("SELECT * FROM 'data/variants/chrom=chr1/*.parquet'")
```

### 7. Optimize Row Group Size
```sql
-- Larger row groups for analytical queries
COPY samples TO 'output.parquet'
(FORMAT parquet, ROW_GROUP_SIZE 1000000);
```

### 8. Use Compression
```sql
-- Zstd compression (good balance of speed and size)
COPY samples TO 'output.parquet'
(FORMAT parquet, COMPRESSION zstd);
```

## Bioinformatics-Specific Tips

### Catalog Genomic Data
```python
# Register BAM index information
conn.execute("""
    CREATE TABLE alignments AS
    SELECT * FROM 'data/alignment_stats.parquet'
""")

# Register VCF statistics
conn.execute("""
    CREATE TABLE variant_stats AS
    SELECT * FROM 'data/vcf_stats/*.parquet'
""")
```

### Query Variant Data
```sql
-- Find high-quality variants
SELECT chrom, pos, ref, alt, qual
FROM 'variants/*.parquet'
WHERE qual > 30 AND filter = 'PASS';

-- Aggregate by chromosome
SELECT chrom, COUNT(*) as variant_count
FROM 'variants/*.parquet'
GROUP BY chrom
ORDER BY chrom;
```

### Track Analysis Provenance
```python
conn.execute("""
    CREATE TABLE analysis_runs (
        run_id VARCHAR PRIMARY KEY,
        sample_id VARCHAR,
        pipeline VARCHAR,
        version VARCHAR,
        run_date TIMESTAMP,
        parameters JSON,
        output_files JSON
    )
""")
```

### Integrate with Workflows
```python
# Read sample sheet
samples = conn.execute("SELECT * FROM 'samplesheet.parquet'").df()

# Process each sample
for sample in samples.itertuples():
    # Run analysis
    # ...
    # Store results
    conn.execute("""
        INSERT INTO results VALUES (?, ?, ?, ?)
    """, [sample.sample_id, coverage, quality, output_path])
```

### Export for R or Other Tools
```python
# Export to format readable by other tools
conn.execute("""
    COPY (SELECT * FROM samples)
    TO 'samples.csv' (HEADER, DELIMITER ',')
""")
```
