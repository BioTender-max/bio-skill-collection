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

# MAGE
## Generation of novel paired heavy-light chain antibodies using large language models
Monoclonal Antibody GEnerator (MAGE) - a fine-tuned LLM for generating paired heavy-light antibody variable sequences with predicted binding specificity to antigen prompt.

This repository contains Python scripts to accompany Wasdin et al., including antibody generation and follow-up analyses presented in the manuscript. All analyses were initially ran in Linux Red Hat 8.4, but have also been tested in Ubuntu 22.04. For training, 4 V100s were used and for antibody generation, an Nvidia A6000 was used. The model weights are hosted on HuggingFace at https://huggingface.co/perrywasdin/MAGE_V1.

The following libraries are needed, we recommened installing these within a Conda environment with Python 3.11. Note that other versions are likely compatible, but we used the following. 
* Numpy 1.26
* Pandas 2.1.1
* Scikit-learn 1.3.0
* Matplotlib 3.8.1
* Seaborn 0.13.1
* Jupterlab 3.6.3

Model training and generation require the following libraries:
* PyTorch 2.1.0 with pytorch-cuda 11.8
* Transformers 4.32.1

The Progen2 repository must cloned from:
https://github.com/enijkamp/progen2

Once downloaded, move to the 'progen' directory here in order to import within the training/generation scripts.

Follow-up Analyses used these additional libraries:
* python-Levenshtein 0.25.0
* pandarallel 1.6.4 (to speed up Pandas functions)
* Abnumber 0.3.2

## Overview of directories
_Data cleaning_: notebooks for cleaning data, including a variety of different sources.

_Output_analysis_: notebooks for recreating figures in manuscript
- Include selection scripts for RBD, RSV-A, and H5/TX/24

_Antibody_generation_: script for generating antibody sequences against RBD. This yields a CSV file with raw sequences which can be analyzed using the notebooks in the previous directory.

_Fine_tuning_: script and example subset dataset (n=1000) for fine-tuning Progen2.


## Tutorial for antibody generation
- Antibody sequences can be generated using the generate_antibodies.py Python script
- An antigen prompt should be provided as an amino acid sequence with any signal peptides or transmembrane regions removed, example:
    SARS-CoV-2 index strain RBD: RVQPTESIVRFPNITNLCPFGEVFNATRFASVYAWNRKRISNCVADYSVLYNSASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSKVGGNYNYLYRLFRKSNLKPFERDISTEIYQAGSTPCNGVEGFNCYFPLQSYGFQPTNGVGYQPYRVVVLSFELLHAPATVCGPKKSTNLVKNKCVNF
    - This is provided as a string named antigen_prompt within the python script
- When running the script from the terminal, specify n number of sequences to generate, and an output csv name:
    - Example: python generate_antibodies.py --n=1 --output=MAGE_antibodies.csv
- This was tested on an Nvidia A6000 and took ~15 seconds to generate one antibody sequence against RBD.
- To annotate and analyze output sequences without installing the follow-up analyses libraries listed above, generated sequences can be uploaded to the IMGT Domain Gap Align webserver: https://www.imgt.org/3Dstructure-DB/cgi/DomainGapAlign.cgi
  


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->