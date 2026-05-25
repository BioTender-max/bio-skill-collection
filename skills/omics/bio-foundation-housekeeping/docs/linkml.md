# LinkML Usage Guide

## Official Documentation
- URL: https://linkml.io/linkml/
- Version covered: v1.9.6+

## Installation

### Python Package
```bash
pip install linkml
```

### With Docker
```bash
docker pull linkml/linkml
```

## Key Command-Line Flags

### Generate Command Structure
```bash
linkml generate <format> [OPTIONS] YAMLFILE
```

### Generate Pydantic Models
```bash
linkml generate pydantic schema.yaml > models.py
linkml generate pydantic --black schema.yaml > models.py      # Format with black
linkml generate pydantic --extra-fields allow schema.yaml     # Allow extra fields
linkml generate pydantic --no-metadata schema.yaml            # Exclude metadata
linkml generate pydantic --mergeimports schema.yaml           # Merge imports
```

#### Pydantic Generator Options
- `--meta [full|except_children|auto|None]`: Control metadata inclusion (default: auto)
- `--black`: Format output with black formatter
- `--extra-fields [allow|ignore|forbid]`: Extra field handling in BaseModel
- `--array-representations [list|numpydantic]`: Array representation format
- `--template-dir PATH`: Custom jinja2 templates directory
- `--metadata/--no-metadata`: Include/exclude metadata
- `--mergeimports/--no-mergeimports`: Merge imports into single file

### Generate Other Formats
```bash
linkml generate json-schema schema.yaml      # JSON Schema
linkml generate python schema.yaml           # Python dataclasses
linkml generate typescript schema.yaml       # TypeScript interfaces
linkml generate java schema.yaml             # Java classes
linkml generate rust schema.yaml             # Rust types
linkml generate sqltables schema.yaml        # SQL DDL
linkml generate owl schema.yaml              # OWL ontology
linkml generate graphql schema.yaml          # GraphQL schema
linkml generate markdown schema.yaml         # Documentation
```

### Validation
```bash
linkml validate --schema schema.yaml data.json    # Validate data
linkml validate --schema schema.yaml data.yaml
linkml validate --schema schema.yaml data.tsv
```

### Schema Linting
```bash
linkml lint schema.yaml                      # Check schema quality
linkml lint --fix schema.yaml                # Auto-fix issues
```

### Data Conversion
```bash
linkml convert --schema schema.yaml --output data.json data.yaml
linkml convert --schema schema.yaml --output data.yaml data.json
linkml convert --schema schema.yaml --target-class Sample data.yaml
```

## Common Usage for Bioinformatics Metadata Schemas

### 1. Define Sample Metadata Schema
```yaml
# sample_schema.yaml
id: https://example.org/sample-schema
name: sample-schema
description: Sample metadata for bioinformatics projects

prefixes:
  sample: https://example.org/sample/
  biolink: https://w3id.org/biolink/vocab/

classes:
  Sample:
    description: A biological sample
    attributes:
      id:
        identifier: true
        range: string
      sample_name:
        required: true
        range: string
      organism:
        required: true
        range: string
      tissue_type:
        range: string
      collection_date:
        range: date
      sequencing_platform:
        range: SequencingPlatformEnum
      read_length:
        range: integer
      coverage:
        range: float

  Run:
    description: A sequencing run
    attributes:
      id:
        identifier: true
        range: string
      sample_id:
        required: true
        range: Sample
      run_date:
        range: date
      instrument:
        range: string
      fastq_files:
        multivalued: true
        range: string

enums:
  SequencingPlatformEnum:
    permissible_values:
      ILLUMINA:
      PACBIO:
      NANOPORE:
      ELEMENT:
```

### 2. Generate Pydantic Models
```bash
# Generate formatted Pydantic models
linkml generate pydantic --black sample_schema.yaml > sample_models.py
```

### 3. Validate Sample Data
```bash
# Create sample data file (samples.yaml)
linkml validate --schema sample_schema.yaml samples.yaml
```

### 4. Convert Between Formats
```bash
# Convert YAML to JSON
linkml convert --schema sample_schema.yaml --output samples.json samples.yaml

# Convert TSV to JSON
linkml convert --schema sample_schema.yaml --output samples.json samples.tsv
```

### 5. Generate Documentation
```bash
# Generate markdown docs
linkml generate markdown sample_schema.yaml > schema_docs.md

# Generate full documentation site
linkml generate doc sample_schema.yaml --directory ./docs/
```

## Input/Output Formats

### Input
- **Schema Format**: YAML (primary)
- **Data Formats**: JSON, YAML, TSV, CSV, RDF
- **Import Formats**: JSON Schema, OWL, SQL DDL

### Output
- **Code Generation**: Python, Pydantic, TypeScript, Java, Rust, Go
- **Schema Formats**: JSON Schema, SQL DDL, OWL, SHACL, ShEx, GraphQL
- **Documentation**: Markdown, HTML
- **Visualization**: Mermaid ER diagrams, PlantUML, GraphViz

## Performance Tips

### 1. Use Mergeimports for Single-File Output
```bash
# Faster loading with single file
linkml generate pydantic --mergeimports schema.yaml > models.py
```

### 2. Minimize Metadata for Production
```bash
# Smaller models without metadata
linkml generate pydantic --no-metadata schema.yaml > models.py
```

### 3. Cache Schema Validation
```python
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.schema_as_dict import schema_as_dict

# Cache schema for repeated validation
schema_view = SchemaView("schema.yaml")
# Reuse schema_view for multiple validations
```

### 4. Use Strict Mode for Performance
```bash
# Pydantic strict mode (faster validation)
linkml generate pydantic --extra-fields forbid schema.yaml
```

### 5. Batch Validation
For large datasets, validate in batches rather than loading all at once.

### 6. Pre-compile Schemas
Generate code once and reuse rather than parsing YAML repeatedly:
```bash
# Generate once
linkml generate pydantic schema.yaml > models.py

# Use generated models in Python (faster)
from models import Sample
sample = Sample(id="S001", sample_name="Control_1", organism="Homo sapiens")
```

## Bioinformatics-Specific Tips

### Use Standard Prefixes
```yaml
prefixes:
  obo: http://purl.obolibrary.org/obo/
  edam: http://edamontology.org/
  sio: http://semanticscience.org/resource/
  biolink: https://w3id.org/biolink/vocab/
```

### Common Bioinformatics Ranges
```yaml
classes:
  Sequence:
    attributes:
      sequence:
        range: string
        pattern: "^[ACGT]+$"
      length:
        range: integer
        minimum_value: 1
      gc_content:
        range: float
        minimum_value: 0.0
        maximum_value: 1.0
```

### Link to Ontologies
```yaml
classes:
  Sample:
    attributes:
      organism:
        range: string
        exact_mappings:
          - NCBITaxon:9606  # Human
```

### Multi-valued Attributes for Files
```yaml
classes:
  Sample:
    attributes:
      fastq_files:
        multivalued: true
        range: string
      bam_files:
        multivalued: true
        range: string
```

### Use Slots for Reusable Attributes
```yaml
slots:
  sample_id:
    description: Unique sample identifier
    range: string
    required: true

  date:
    description: Date in ISO format
    range: date

classes:
  Sample:
    slot_usage:
      sample_id:
      collection_date:
        is_a: date
```
