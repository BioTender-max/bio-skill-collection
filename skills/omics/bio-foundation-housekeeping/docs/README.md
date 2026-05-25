# Tool Documentation

Documentation created: 2026-02-01

This directory contains practical usage guides for the core tools used in bio-foundation-housekeeping.

## Tools Covered

### [Pixi](pixi.md)
**Version**: v0.43.0+
**Purpose**: Developer workflow and environment management for multi-platform, language-agnostic workspaces
**Key Use**: Creating reproducible conda/mamba environments with lockfiles

**Quick Start**:
```bash
pixi init myproject --channel conda-forge --channel bioconda
cd myproject
pixi add python=3.11 biopython pysam
pixi install
```

### [LinkML](linkml.md)
**Version**: v1.9.6+
**Purpose**: Flexible modeling language for authoring schemas in YAML
**Key Use**: Defining metadata schemas and generating Pydantic models

**Quick Start**:
```bash
pip install linkml
linkml generate pydantic --black schema.yaml > models.py
linkml validate --schema schema.yaml data.yaml
```

### [Pydantic](pydantic.md)
**Version**: v2.12.5+
**Purpose**: Data validation using Python type hints
**Key Use**: Runtime validation of sample metadata and configuration

**Quick Start**:
```python
from pydantic import BaseModel, Field

class Sample(BaseModel):
    sample_id: str
    organism: str
    coverage: float = Field(gt=0)

sample = Sample(sample_id="S001", organism="Human", coverage=30.5)
```

### [DuckDB](duckdb.md)
**Version**: v1.4.3+
**Purpose**: In-process SQL OLAP database
**Key Use**: Creating data catalogs and querying Parquet files

**Quick Start**:
```python
import duckdb
conn = duckdb.connect('catalog.duckdb')
conn.execute("CREATE TABLE samples AS SELECT * FROM 'samples.parquet'")
results = conn.execute("SELECT * FROM samples WHERE coverage > 30").df()
```

## Documentation Structure

Each tool guide includes:
- Official documentation URL
- Installation commands
- Key command-line flags and options
- Common usage examples for project setup
- Input/output formats
- Performance tips
- Bioinformatics-specific usage patterns

## Usage in bio-foundation-housekeeping

These tools work together in the skill workflow:

1. **Pixi**: Sets up reproducible environment with all dependencies
2. **LinkML**: Defines metadata schemas for samples, runs, etc.
3. **Pydantic**: Validates data at runtime using generated models
4. **DuckDB**: Catalogs data files for efficient querying

## Official Documentation Links

- Pixi: https://pixi.sh/latest/
- LinkML: https://linkml.io/linkml/
- Pydantic: https://docs.pydantic.dev/latest/
- DuckDB: https://duckdb.org/docs/

## Notes

- All guides focus on practical bioinformatics use cases
- Examples emphasize reproducibility and data validation
- Performance tips are tailored for typical genomics workflows
- Documentation will be updated as tool versions evolve
