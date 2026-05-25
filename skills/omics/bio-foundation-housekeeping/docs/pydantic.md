# Pydantic Usage Guide

## Official Documentation
- URL: https://docs.pydantic.dev/latest/
- Version covered: v2.12.5+

## Installation

### Basic Installation
```bash
pip install pydantic
```

### With Email Validation
```bash
pip install 'pydantic[email]'
```

### With All Extensions
```bash
pip install 'pydantic[email,dotenv]'
```

## Key Features and Usage

### Basic Model Definition
```python
from pydantic import BaseModel, Field, PositiveInt
from typing import Optional
from datetime import date

class Sample(BaseModel):
    id: str
    sample_name: str
    organism: str
    tissue_type: Optional[str] = None
    collection_date: Optional[date] = None
    read_depth: PositiveInt

    class Config:
        str_strip_whitespace = True
        validate_assignment = True
```

### Validation Modes
```python
from pydantic import BaseModel, ConfigDict

# Strict mode (no type coercion)
class StrictSample(BaseModel):
    model_config = ConfigDict(strict=True)
    id: int
    name: str

# Lax mode (with type coercion, default)
class LaxSample(BaseModel):
    id: int  # "123" will be converted to 123
    name: str
```

### Field Constraints
```python
from pydantic import Field, field_validator

class QualityMetrics(BaseModel):
    sample_id: str = Field(..., min_length=1, max_length=50)
    q30_score: float = Field(..., ge=0.0, le=1.0)
    read_count: int = Field(..., gt=0)
    gc_content: float = Field(..., ge=0.0, le=1.0)

    @field_validator('gc_content')
    @classmethod
    def check_gc_range(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('GC content must be between 0 and 1')
        return v
```

### Custom Validators
```python
from pydantic import BaseModel, field_validator, model_validator

class Sequence(BaseModel):
    id: str
    sequence: str
    sequence_type: str

    @field_validator('sequence')
    @classmethod
    def validate_dna(cls, v, info):
        if info.data.get('sequence_type') == 'DNA':
            if not set(v.upper()).issubset({'A', 'C', 'G', 'T', 'N'}):
                raise ValueError('Invalid DNA sequence')
        return v.upper()

    @model_validator(mode='after')
    def check_sequence_length(self):
        if len(self.sequence) == 0:
            raise ValueError('Sequence cannot be empty')
        return self
```

### Nested Models
```python
from typing import List

class FastqFile(BaseModel):
    path: str
    read_number: int
    size_bytes: int

class SequencingRun(BaseModel):
    run_id: str
    sample: Sample
    fastq_files: List[FastqFile]
    platform: str

    def total_size(self) -> int:
        return sum(f.size_bytes for f in self.fastq_files)
```

### JSON Schema Generation
```python
schema = Sample.model_json_schema()
print(schema)
```

### Serialization/Deserialization
```python
# From dict
sample = Sample(**data_dict)

# From JSON
sample = Sample.model_validate_json(json_string)

# To dict
sample_dict = sample.model_dump()

# To JSON
json_str = sample.model_dump_json()

# Exclude fields
sample_dict = sample.model_dump(exclude={'internal_id'})

# Include only specific fields
sample_dict = sample.model_dump(include={'id', 'name'})
```

## Common Usage for Bioinformatics

### 1. Sample Metadata Validation
```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from enum import Enum

class Platform(str, Enum):
    ILLUMINA = "ILLUMINA"
    PACBIO = "PACBIO"
    NANOPORE = "NANOPORE"

class Sample(BaseModel):
    sample_id: str = Field(..., pattern=r'^[A-Z0-9_-]+$')
    sample_name: str
    organism: str = Field(..., min_length=1)
    tissue: Optional[str] = None
    collection_date: date
    platform: Platform
    read_length: int = Field(..., gt=0)
    coverage: float = Field(..., gt=0.0)
    fastq_r1: str
    fastq_r2: Optional[str] = None

# Usage
sample = Sample(
    sample_id="S001",
    sample_name="Control_1",
    organism="Homo sapiens",
    collection_date="2024-01-15",
    platform="ILLUMINA",
    read_length=150,
    coverage=30.5,
    fastq_r1="/data/S001_R1.fastq.gz",
    fastq_r2="/data/S001_R2.fastq.gz"
)
```

### 2. VCF Record Validation
```python
class VCFRecord(BaseModel):
    chrom: str
    pos: int = Field(..., gt=0)
    id: Optional[str] = None
    ref: str = Field(..., pattern=r'^[ACGTN]+$')
    alt: List[str]
    qual: Optional[float] = Field(None, ge=0)
    filter: str
    info: dict

    @field_validator('alt')
    @classmethod
    def validate_alt_alleles(cls, v):
        for allele in v:
            if not set(allele.upper()).issubset({'A', 'C', 'G', 'T', 'N'}):
                raise ValueError(f'Invalid alt allele: {allele}')
        return v
```

### 3. Pipeline Configuration
```python
class AlignmentConfig(BaseModel):
    threads: int = Field(default=8, ge=1, le=64)
    memory_gb: int = Field(default=16, ge=1)
    reference_genome: str
    output_dir: str

class VariantCallingConfig(BaseModel):
    min_depth: int = Field(default=10, ge=1)
    min_quality: float = Field(default=20.0, ge=0)
    caller: str = Field(default="bcftools")

class PipelineConfig(BaseModel):
    alignment: AlignmentConfig
    variant_calling: VariantCallingConfig
    input_samples: List[Sample]
```

### 4. Quality Control Metrics
```python
class QCMetrics(BaseModel):
    sample_id: str
    total_reads: int = Field(..., gt=0)
    mapped_reads: int = Field(..., ge=0)
    duplicate_rate: float = Field(..., ge=0.0, le=1.0)
    mean_coverage: float = Field(..., ge=0.0)
    pct_bases_20x: float = Field(..., ge=0.0, le=1.0)

    @model_validator(mode='after')
    def validate_mapping(self):
        if self.mapped_reads > self.total_reads:
            raise ValueError('Mapped reads cannot exceed total reads')
        return self

    @property
    def mapping_rate(self) -> float:
        return self.mapped_reads / self.total_reads if self.total_reads > 0 else 0.0
```

## Input/Output Formats

### Input
- Python dictionaries
- JSON strings or files
- Environment variables (with pydantic-settings)
- YAML (with PyYAML)

### Output
- Python dictionaries
- JSON strings
- JSON Schema
- TypedDict (for type hints)

## Performance Tips

### 1. Use Strict Mode for Known Data
```python
class StrictSample(BaseModel):
    model_config = ConfigDict(strict=True)
    id: int
    name: str
# Faster validation, no type coercion
```

### 2. Disable Extra Fields
```python
class Sample(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str
    name: str
# Reject unknown fields (faster than allowing them)
```

### 3. Lazy Validation
```python
# Validate only when needed
sample = Sample.model_construct(**data)  # Skip validation
sample.model_validate(sample)  # Validate later
```

### 4. Reuse Validators
```python
# Define validator once
def validate_sequence(v: str) -> str:
    if not set(v.upper()).issubset({'A', 'C', 'G', 'T', 'N'}):
        raise ValueError('Invalid DNA sequence')
    return v.upper()

class Sequence1(BaseModel):
    seq: str
    _validate_seq = field_validator('seq')(validate_sequence)

class Sequence2(BaseModel):
    seq: str
    _validate_seq = field_validator('seq')(validate_sequence)
```

### 5. Use Rust Core
Pydantic v2+ uses Rust internally for validation (fast by default).
No additional configuration needed.

### 6. Batch Validation
```python
# Validate multiple samples
samples = [Sample.model_validate(data) for data in batch_data]
```

### 7. Defer Validation
```python
from pydantic import TypeAdapter

# Create type adapter once
SampleList = TypeAdapter(List[Sample])

# Reuse for multiple validations
samples = SampleList.validate_python(data_list)
```

## Bioinformatics-Specific Tips

### Sequence Validation
```python
DNA_PATTERN = r'^[ACGTN]+$'
PROTEIN_PATTERN = r'^[ACDEFGHIKLMNPQRSTVWY]+$'

class DNASequence(BaseModel):
    seq: str = Field(..., pattern=DNA_PATTERN)

class ProteinSequence(BaseModel):
    seq: str = Field(..., pattern=PROTEIN_PATTERN)
```

### File Path Validation
```python
from pathlib import Path
from pydantic import field_validator

class AnalysisInput(BaseModel):
    fastq_file: str

    @field_validator('fastq_file')
    @classmethod
    def check_file_exists(cls, v):
        if not Path(v).exists():
            raise ValueError(f'File not found: {v}')
        return v
```

### Coordinate Validation
```python
class GenomicRange(BaseModel):
    chrom: str
    start: int = Field(..., ge=0)
    end: int = Field(..., gt=0)

    @model_validator(mode='after')
    def check_range(self):
        if self.start >= self.end:
            raise ValueError('Start must be less than end')
        return self
```

### Handle Missing Data
```python
from typing import Optional

class Sample(BaseModel):
    id: str
    coverage: Optional[float] = None  # Allow missing values
    quality: float = Field(default=0.0)  # Provide defaults
```
