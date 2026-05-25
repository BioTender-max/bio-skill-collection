<!--
# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

-->

# CellTypeAgent

## Introduction

Cell type annotation is a critical yet laborious step in single-cell RNA sequencing analysis. We present a trustworthy large language model (LLM)-agent, CellTypeAgent, which integrates LLMs with verification from relevant databases. CellTypeAgent achieves higher accuracy than existing methods while mitigating hallucinations. We evaluated CellTypeAgent across nine real datasets involving 303 cell types from 36 tissues. This combined approach holds promise for more efficient and reliable cell type annotation.


## Requirements

1. Clone the repository
```bash
git clone https://github.com/jianghao-zhang/CellTypeAgent.git
cd CellTypeAgent
```

2. Create a conda environment and install the dependencies
```bash
conda create -n CellTypeAgent python=3.10
conda activate CellTypeAgent
pip install -r requirements.txt
```

3. Set your OpenAI/Anthropic/DeepSeek API keys configuration in the 'CellTypeAgent/APIs' folder

4. Prepare the data
- The datasets used in the paper are stored in the 'CellTypeAgent/data' folder.
- Please download the gene expression data used in this paper from [Google Drive](https://drive.google.com/drive/folders/1mC6r5Nu1JimBWSOanOdGDT2QolYdhF_S?usp=sharing) and place it in the 'CellTypeAgent/data/CELLxGENE' directory.
- Please check the [README.md](CellTypeAgent/data/README.md) in the 'CellTypeAgent/data' folder for more information.


## Example Usage

- Run an experiment on all datasets:

```bash
python CellTypeAgent/get_prediction.py
python CellTypeAgent/get_selection.py
```

## Adapting the Framework to Custom Datasets

To utilize CellTypeAgent with your own datasets, follow these steps:

1. Format your data according to the structure in `CellTypeAgent/data/GPTCellType/datasets`
2. Download the corresponding gene expression data from the [CZ CellxGene - Gene Expression Atlas](https://cellxgene.cziscience.com/gene-expression), for more details, please refer to the [README.md](CellTypeAgent/data/README.md) in the 'CellTypeAgent/data' folder
3. Modify the dataset settings in `get_prediction.py` and `get_selection.py`
4. Configure model parameters as needed (e.g., `model`, `top_n`, `max_markers`)
5. Run the pipeline as described in the Example Usage section



<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->