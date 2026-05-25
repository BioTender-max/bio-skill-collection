# Pixi Usage Guide

## Official Documentation
- URL: https://pixi.sh/latest/
- Version covered: v0.43.0+

## Installation

### Linux & macOS
```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

### Windows
```powershell
iwr -useb https://pixi.sh/install.ps1 | iex
```

### Alternative: Homebrew
```bash
brew install pixi
```

## Key Command-Line Flags

### Initialize New Workspace
```bash
pixi init [PATH]                    # Create new workspace (default: current dir)
pixi init --channel conda-forge     # Specify channel
pixi init --platform linux-64       # Set supported platforms
pixi init --import environment.yml  # Bootstrap from conda environment
pixi init --format pyproject        # Use pyproject.toml format
```

### Add Dependencies
```bash
pixi add python=3.9                 # Add specific version
pixi add python pytest numpy        # Add multiple packages
pixi add --pypi boto3               # Add PyPI package
pixi add python --platform linux-64 # Platform-specific dependency
pixi add python --build             # Add as build dependency
pixi add python --host              # Add as host dependency
pixi add --pypi --editable 'pkg @ file://path/to/pkg'  # Editable install
```

### Install Environment
```bash
pixi install                        # Install default environment
pixi install --environment prod     # Install specific environment
pixi install --all                  # Install all environments
pixi install --skip pandas          # Skip specific package (soft exclusion)
```

### Run Tasks
```bash
pixi run test                       # Run named task
pixi run --environment prod test    # Run in specific environment
pixi run --clean-env test           # Use minimal environment
pixi run --dry-run test             # Print command without running
pixi run --skip-deps test           # Skip task dependencies
```

### Other Key Commands
```bash
pixi task add test 'pytest -s'      # Define new task
pixi lock                           # Update lockfile without installing
pixi shell                          # Start interactive shell in environment
pixi list                           # List installed packages
pixi search numpy                   # Search for packages
pixi remove pandas                  # Remove dependency
pixi clean                          # Clean environment cache
```

## Common Usage for Bioinformatics Project Setup

### 1. Initialize Project
```bash
# Create new bioinformatics project
pixi init myproject --channel conda-forge --channel bioconda
cd myproject
```

### 2. Add Core Dependencies
```bash
# Add common bioinformatics tools
pixi add python=3.11 numpy pandas scipy
pixi add biopython pysam bcftools samtools
pixi add jupyter matplotlib seaborn
pixi add --pypi duckdb linkml pydantic
```

### 3. Define Environments
```bash
# Edit pixi.toml to add multiple environments
# [environments]
# default = {solve-group = "default"}
# analysis = {features = ["analysis"], solve-group = "analysis"}
# qc = {features = ["qc"], solve-group = "qc"}
```

### 4. Define Tasks
```bash
# Add common tasks
pixi task add setup 'python setup.py'
pixi task add test 'pytest tests/'
pixi task add qc 'python src/qc.py'
pixi task add analyze 'python src/analyze.py'
```

### 5. Lock and Install
```bash
# Generate lockfile and install
pixi install
```

### 6. Run Workflows
```bash
# Execute tasks
pixi run setup
pixi run qc
pixi run analyze
```

## Input/Output Formats

### Input
- **pixi.toml**: Workspace manifest (TOML format)
- **pyproject.toml**: Alternative Python project format
- **environment.yml**: Conda environment (for import)

### Output
- **pixi.lock**: Locked dependency specifications (JSON)
- **.pixi/**: Environment installation directory
- **pixi.toml**: Updated manifest with added dependencies

## Performance Tips

### 1. Use Solve Groups
Group environments that share dependencies to speed up solving:
```toml
[environments]
dev = {features = ["dev"], solve-group = "default"}
test = {features = ["test"], solve-group = "default"}
```

### 2. Lock Before Installing
For large projects, separate locking from installation:
```bash
pixi lock              # Solve dependencies once
pixi install --all     # Install all environments from lock
```

### 3. Cache Management
```bash
pixi clean             # Remove unused environments
pixi clean --cache     # Clear package cache
```

### 4. Platform-Specific Dependencies
Only install what you need for your platform:
```bash
pixi add bwa --platform linux-64
pixi add bwa --platform osx-arm64
```

### 5. Use Micromamba Solver
Pixi uses the fast rattler solver by default, much faster than conda.

### 6. Parallel Environment Installation
```bash
pixi install --all     # Installs environments in parallel where possible
```

## Bioinformatics-Specific Tips

### Channel Priority
Always include bioconda for bioinformatics packages:
```toml
[workspace]
channels = ["conda-forge", "bioconda"]
```

### Reproducible Environments
The pixi.lock file ensures exact reproducibility:
```bash
# Commit pixi.lock to git
git add pixi.toml pixi.lock
git commit -m "Add reproducible environment"
```

### Container Integration
Generate Dockerfile from pixi environment:
```bash
pixi global install pixi-pack
pixi pack --platform linux-64
```

### Task Dependencies
Chain bioinformatics workflow steps:
```toml
[tasks]
setup = "mkdir -p data results"
qc = {cmd = "fastqc data/*.fastq", depends-on = ["setup"]}
align = {cmd = "bwa mem", depends-on = ["qc"]}
call = {cmd = "bcftools call", depends-on = ["align"]}
```
