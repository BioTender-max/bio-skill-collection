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

# TrialGPT: Matching Patients to Clinical Trials with Large Language Models

## Introduction
Clinical trials are often hindered by the challenge of patient recruitment. In this work, we introduce TrialGPT, a novel end-to-end framework for zero-shot patient-to-trial matching with large language models (LLMs). TrialGPT consists of three key components: it first performs filtering of irrelevant clinical trials at scale (TrialGPT-Retrieval), then predicts the patient eligibility on a criterion-by-criterion basis (TrialGPT-Matching); and finally aggregates criterion-level predictions into trial-level scores for ranking the clinical trials (TrialGPT-Ranking). We evaluate TrialGPT on three publicly available cohorts of 183 synthetic patients with over 75,000 trial eligibility annotations. TrialGPT-Retrieval can efficiently recall over 90% of relevant clinical trials using only less than 6% of the initial clinical trial collection. Over 1,000 patient-criterion pairs were manually annotated by three physicians to evaluate TrialGPT-Matching, which achieves a criterion-level accuracy of 87.3% with faithful explanations, close to the expert performance (88.7%–90.0%). For TrialGPT-Ranking, the aggregated trial-level scores are highly correlated with human eligibility judgments, and they outperform the best-competing models by 28.8% to 53.5% in ranking and excluding clinical trials. Furthermore, our user study reveals that TrialGPT can significantly reduce the screening time by 42.6% in a real-life clinical trial matching task. Taken together, these results have demonstrated promising opportunities for clinical trial matching with LLMs via the TrialGPT framework.

![image](https://github.com/user-attachments/assets/66b01b03-1871-4ccc-be05-10e17e077370)

## Configuration

To run TrialGPT, one needs to first set up the OpenAI API either directly through OpenAI or through Microsoft Azure. Here we use Microsoft Azure because it is compliant with Health Insurance Portability and Accountability Act (HIPAA). Please set the enviroment variables accordingly:

```bash
export OPENAI_ENDPOINT=YOUR_AZURE_OPENAI_ENDPOINT_URL
export OPENAI_API_KEY=YOUR_AZURE_OPENAI_API_KEY
```

The code has been tested with Python 3.9.13 using CentOS Linux release 7.9.2009 (Core). Please install the required Python packages by:

```bash
pip install -r requirements.txt
```

## Datasets

We used the clinical trial information on https://clinicaltrials.gov/. Please download our parsed dataset by:

```bash
wget -O dataset/trial_info.json https://ftp.ncbi.nlm.nih.gov/pub/lu/TrialGPT/trial_info.json
```

Three publicly available datasets are used in the study (please properly cite these datasets if you use them; see details about citations in the bottom):
- The SIGIR 2016 corpus, available at: https://data.csiro.au/collection/csiro:17152
- The TREC Clinical Trials 2021 corpus, available at: https://www.trec-cds.org/2021.html
- The TREC Clinical Trials 2022 corpus, available at: https://www.trec-cds.org/2022.html

The SIGIR dataset is already in `/dataset/`, please download the corpora of TREC CT 2021 and 2022 by:

```bash
wget -O dataset/trec_2021/corpus.jsonl https://ftp.ncbi.nlm.nih.gov/pub/lu/TrialGPT/trec_2021_corpus.jsonl
wget -O dataset/trec_2022/corpus.jsonl https://ftp.ncbi.nlm.nih.gov/pub/lu/TrialGPT/trec_2022_corpus.jsonl
```

## TrialGPT-Retrieval

Given a patient summary and an initial collection of clinical trials, the first step is TrialGPT-Retrieval, which generates a list of keywords for the patient and utilizes a hybrid-fusion retrieval mechanism to get relevant trials (component a in the figure). 

Specifically, one can run the code below for keyword generation. The generated keywords will be saved in the `./results/` directory.

```bash
# syntax: python trialgpt_retrieval/keyword_generation.py ${corpus} ${model}  
# ${corpus} can be sigir, trec_2021, and trec_2022
# ${model} can be any model indices in OpenAI or AzureOpenAI API
# examples below
python trialgpt_retrieval/keyword_generation.py sigir gpt-4-turbo
python trialgpt_retrieval/keyword_generation.py trec_2021 gpt-4-turbo
python trialgpt_retrieval/keyword_generation.py trec_2022 gpt-4-turbo
```

After generating the keywords, one can run the code below for retrieving relevant clinical trials. The retrieved trials will be saved in the `./results/` directory. The code below will use our cached results of keyword generation that are located in `./dataset/{corpus}/id2queries.json`.

```bash
# syntax: python trialgpt_retrieval/hybrid_fusion_retrieval.py ${corpus} ${q_type} ${k} ${bm25_weight} ${medcpt_weight} 
# ${corpus} can be sigir, trec_2021, and trec_2022
# ${q_type} can be raw, gpt-35-turbo (our cached results), and gpt-4-turbo (our cached results), Clinician_A (for sigir only), Clinician_B (for sigir only), Clinician_C (for sigir only), and Clinician_D (for sigir only)
# ${k} is the constant in the reciprocal rank fusion, and we recommend using 20
# ${bm25_weight} is the weight for the BM25 retriever, it should be set as 1 unless in ablation experiments
# ${medcpt_weight} is the weight for the MedCPT retriever, it should be set as 1 unless in ablation experiments
# examples below
python trialgpt_retrieval/hybrid_fusion_retrieval.py sigir gpt-4-turbo 20 1 1
python trialgpt_retrieval/hybrid_fusion_retrieval.py trec_2021 gpt-4-turbo 20 1 1
python trialgpt_retrieval/hybrid_fusion_retrieval.py trec_2022 gpt-4-turbo 20 1 1
```

## TrialGPT-Matching

After retrieving the candidate clinical trials with TrialGPT-Retrieval, the next step is to use TrialGPT-Matching to perform fine-grained criterion-by-criterion analyses on each patient-trial pair (component b in the figure). We have also made the retrieved trials by GPT-4-based TrialGPT-Retrieval available at `./dataset/{corpus}/retrieved_trials.json`. One can run the following commands to use TrialGPT-Matching, and the results will be saved in `./results/`:

```bash
# syntax: python trialgpt_matching/run_matching.py ${corpus} ${model}
# ${corpus} can be sigir, trec_2021, and trec_2022
# ${model} can be any model indices in OpenAI or AzureOpenAI API
# examples below
python trialgpt_matching/run_matching.py sigir gpt-4-turbo
python trialgpt_matching/run_matching.py trec_2021 gpt-4-turbo
python trialgpt_matching/run_matching.py trec_2022 gpt-4-turbo
```

## TrialGPT-Ranking

The final step is to use TrialGPT-Ranking to aggregate the criterion-level predictions into trial-level scores for ranking (component c in the figure). To get the LLM-aggregation scores for TrialGPT-Ranking, one can run the following commands. The results will be saved in `./results/`:

```bash
# syntax: python trialgpt_ranking/run_aggregation.py ${corpus} ${model} ${matching_results_path}
# ${corpus} can be sigir, trec_2021, and trec_2022
# ${model} can be any model indices in OpenAI or AzureOpenAI API
# ${matching_results_path} is the path to the TrialGPT matching results 
# example below (please make sure to have the TrialGPT-Matching results for the SIGIR corpus with the gpt-4-turbo model before running this)
python trialgpt_ranking/run_aggregation.py sigir gpt-4-turbo results/matching_results_sigir_gpt-4-turbo.json
```

Once the matching results and the aggregation results are complete, one can run the following code to get the final ranking of clinical trials for each patient:

```bash
# syntax: python trialgpt_ranking/rank_results.py ${matching_results_path} ${aggregation_results_path}
# ${matching_results_path} is the path to the TrialGPT matching results 
# ${aggregation_results_path} is the path to the aggregation results generated above
# example below (please make sure to have the TrialGPT-Matching results and the aggregation results for the SIGIR corpus with the gpt-4-turbo model before running this)
python trialgpt_ranking/rank_results.py results/matching_results_sigir_gpt-4-turbo.json results/aggregation_results_sigir_gpt-4-turbo.json
```

Example output:

```bash
Patient ID: sigir-20141
Clinical trial ranking:
NCT00185120 2.8999999995
NCT02144636 2.8999999995
NCT02608255 2.84999999975
NCT01724996 2.7999999998
...
```

## Acknowledgments

This work was supported by the Intramural Research Programs of the National Institutes of Health, National Library of Medicine.

## Disclaimer

This tool shows the results of research conducted in the Computational Biology Branch, NCBI/NLM. The information produced on this website is not intended for direct diagnostic use or medical decision-making without review and oversight by a clinical professional. Individuals should not change their health behavior solely on the basis of information produced on this website. NIH does not independently verify the validity or utility of the information produced by this tool. If you have questions about the information produced on this website, please see a health care professional. More information about NCBI's disclaimer policy is available.

## Citation

If you find this repo helpful, please cite TrialGPT by:
```bibtex
@article{jin2024matching,
  title={Matching patients to clinical trials with large language models},
  author={Jin, Qiao and Wang, Zifeng and Floudas, Charalampos S and Chen, Fangyuan and Gong, Changlin and Bracken-Clarke, Dara and Xue, Elisabetta and Yang, Yifan and Sun, Jimeng and Lu, Zhiyong},
  journal={Nature Communications},
  volume={15},
  number={1},
  pages={9074},
  year={2024},
  publisher={Nature Publishing Group UK London}
}
```

If you use the SIGIR cohort, please cite the original dataset papers by:
```bibtex
@inproceedings{koopman2016test,
  title={A test collection for matching patients to clinical trials},
  author={Koopman, Bevan and Zuccon, Guido},
  booktitle={Proceedings of the 39th International ACM SIGIR conference on Research and Development in Information Retrieval},
  pages={669--672},
  year={2016}
}
@inproceedings{roberts2015overview,
  title={Overview of the TREC 2015 Clinical Decision Support Track},
  author={Roberts, Kirk and Simpson, Matthew S and Voorhees, Ellen M and Hersh, William R},
  booktitle={Proceedings of the Twenty-Fourth Text REtrieval Conference (TREC 2015)},
  year={2015}
}
@inproceedings{simpson2014overview,
  title={Overview of the TREC 2014 Clinical Decision Support Track},
  author={Simpson, Matthew S and Voorhees, Ellen M and Hersh, William R},
  booktitle={Proceedings of the Twenty-Third Text REtrieval Conference (TREC 2014)},
  year={2014}
}
```

If you use the TREC cohorts, please cite the original dataset papers by:
```bibtex
@inproceedings{roberts2021overview,
  title={Overview of the TREC 2021 clinical trials track},
  author={Roberts, Kirk and Demner-Fushman, Dina and Voorhees, Ellen M and Bedrick, Steven and Hersh, Willian R},
  booktitle={Proceedings of the Thirtieth Text REtrieval Conference (TREC 2021)},
  year={2021}
}
@inproceedings{roberts2022overview,
  title={Overview of the TREC 2022 clinical trials track},
  author={Roberts, Kirk and Demner-Fushman, Dina and Voorhees, Ellen M and Bedrick, Steven and Hersh, Willian R},
  booktitle={Proceedings of the Thirty-first Text REtrieval Conference (TREC 2022)},
  year={2022}
}
```


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->