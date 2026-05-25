# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import os
import re
import time
import inflect
import pandas as pd
from LLM import complete_text

data_info = [
    { "name": 'Azimuth', "species": 'Human', "tissue": 'Mixed', "num_samples": {'Adipose':15, 'Bone Marrow':40, 'Fetal Development':62, 'Heart':21, 'Kidney':16, 'Liver':23, 'Lung':60, 'Motor Cortex':20, 'PBMC':30, 'Pancreas':12, 'Tonsil':24} },
    { "name": 'HCA', "species": 'Human', "tissue": 'Mixed', "num_samples": {'Breast':8, 'Esophagus':17, 'Heart':13, 'Lung':15, 'Prostate':16, 'Skeletal muscle':14, 'Skin':16} },
    { "name": 'MCA', "species": 'Mouse', "tissue": None, "num_samples": {'all': 64} },
    { "name": 'literature', "species": 'Human', "tissue": 'Mixed', "num_samples": {'Breast':12, 'Esophagus':12, 'Heart':11, 'Lung':14, 'Prostate':11, 'Skeletal muscle':13, 'Skin':17} },
    { "name": 'tabulasapiens', "species": 'Human', "tissue": 'Mixed', "num_samples": {'Bladder':15, 'Blood':26, 'Bone Marrow':17, 'Eye':29, 'Fat':13, 'Heart':6, 'Kidney':7, 'Large Intestine':20, 'Liver':13, 'Lung':37, 'Lymph Node':29, 'Mammary':14, 'Muscle':19, 'Pancreas':15, 'Prostate':21, 'Salivary Gland':23, 'Skin':25, 'Small Intestine':21, 'Spleen':24, 'Thymus':32, 'Tongue':12, 'Trachea':21, 'Uterus':14, 'Vasculature':14} },
    { "name": 'BCL', "species": 'Human', "tissue": 'B cell lymphoma', "num_samples": {'all': 9} },
    { "name": 'HCL', "species": 'human', "tissue": None, "num_samples": {'all': 61} },
    { "name": 'coloncancer', "species": 'Human', "tissue": 'colon cancer', "num_samples": {'all': 7} },
    { "name": 'lungcancer', "species": 'Human', "tissue": 'lung cancer and brain metastasis', "num_samples": {'all': 10} },
]

question_template = {
    "m": "I have a group of cells, the top 10 marker genes in the group are {marker_genes}. What is the cell type of this group of cells?",
    "s_t": "I have a group of cells from {species}, the tissue type is {tissue}, the top 10 marker genes in the group are {marker_genes}. What is the cell type of this group of cells?",
    "s": "I have a group of cells from {species}, the top 10 marker genes in the group are {marker_genes}. What is the cell type of this group of cells?",
    "t": "I have a group of cells, the tissue type is {tissue}, the top 10 marker genes in the group are {marker_genes}. What is the cell type of this group of cells?",
    "GPTCellType": "Identify cell types of {species} {tissue} using the following markers: {marker_genes}. Identify only one cell type.",
    "GPTCellType_m": "Identify cell types using the following markers: {marker_genes}. Identify only one cell type.",
    "get_top_n_cell_types": """Identify most likely top {top_candidate_count} cell types of {species_tissue} cells using the following markers separately for each row. Only provide the lists of top {top_candidate_count} cell type names row by row. The higher the probability, the further left it is ranked, separated by commas. The last {broad_cell_type_count} cell types in this list should be broad types. The number of lists should match the corresponding number of rows in the input. Do not include any other text or comments in the output.\n\n{row_wise_marker_genes}"""
}

def construct_markers_prompt(df_maker):
    markers_prompt = ''
    markers_ls = df_maker.to_list()
    for i, markers in enumerate(markers_ls):
        markers_prompt += str(i+1) + '. ' + markers + '\n'

    return markers_prompt

def generate_cell_type_candidate_prompts(prompt_template, num_candidates=5, num_broad_types=2, data_info=data_info, data_path='data/GPTCellType/datasets'):
    prompts = {}
    for dataset in data_info:
        name = dataset["name"]
        species = dataset["species"]

        df = pd.read_csv(f"{data_path}/{name}.csv")
        tissues = df['tissue'].unique()
        prompts[name] = {}

        if dataset['tissue'] != "Mixed":
            species_tissue = f"{species} {tissues[0]}" if dataset['tissue'] else species
            markers = construct_markers_prompt(df["marker"])
            prompt = prompt_template.format(
                top_candidate_count=num_candidates,
                broad_cell_type_count=num_broad_types,
                species_tissue=species_tissue,
                row_wise_marker_genes=markers
            )
            prompts[name]['all'] = prompt
        else:
            for tissue in tissues:
                tissue_markers = df[df['tissue'] == tissue]['marker']
                species_tissue = f"{species} {tissue}"
                markers = construct_markers_prompt(tissue_markers)
                prompt = prompt_template.format(
                    top_candidate_count=num_candidates,
                    broad_cell_type_count=num_broad_types,
                    species_tissue=species_tissue,
                    row_wise_marker_genes=markers
                )
                prompts[name][tissue] = prompt

    return prompts

def standardize_candidates(response):
    result_ls = response.split('\n')
    result_ls = [re.sub(r'^\d+\.\s*', '', item.strip()) for item in result_ls]
    candidates_ls = []
    for item in result_ls:
        candidates = item.split(',')
        candidates = [standardize_cell_type(c.strip()) for c in candidates]
        candidates_ls.append(candidates)
    return candidates_ls

def get_cell_type_candidates(dataset_name, prompts, model='o1-preview', temperature=1, max_attempts=3, data_info=data_info, log_dir='logs/cell_type_candidates_prediction'):
    dataset_info = next(item for item in data_info if item["name"] == dataset_name)
    tissue = dataset_info['tissue']
    num_samples = dataset_info['num_samples']
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    log_dir = os.path.join(log_dir, dataset_name, model, timestamp)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    def try_get_candidates(prompt, num):
        for _ in range(max_attempts):
            completion = complete_text(prompt, model=model, temperature=temperature, log_file=os.path.join(log_dir, f"{dataset_name}_{tissue}.log"))
            completion = '1. '+completion.split('1. ', 1)[-1] if '1. ' in completion else completion # remove unncessary text in the beginning
            candidates = standardize_candidates(completion)
            if len(candidates) == num:
                return candidates
        return None

    if dataset_info['tissue'] != 'Mixed':
        candidates = try_get_candidates(prompts[dataset_name]['all'], num_samples['all'])
    else:
        candidates = []
        for t, num in num_samples.items():
            tissue_candidates = try_get_candidates(prompts[dataset_name][t], num)
            if tissue_candidates:
                candidates.extend(tissue_candidates)
            else:
                break
        if len(candidates) != sum(num_samples.values()):
            candidates = None

    if candidates is None:
        raise Exception(f"Failed to get the right number of candidates for {dataset_name}")
    return candidates

def split_dataset(all, data_path='data/GPTCellType/datasets'):
    data_list = all['dataset'].unique()
    for data in data_list:
        dataset_df = all[all['dataset'] == data]
        if dataset_df['tissue'].nunique() > 1:
            dataset_df.sort_values('tissue', inplace=True)
        dataset_df.to_csv(f"{data_path}/{data}.csv", index=False)

def construct_cell_type_annotation_questions(data_info, data_path='data/GPTCellType/datasets', GPTCellType_flag=False):
    for info in data_info:
        name = info["name"]
        species = info["species"]
        tissue = info["tissue"]

        dataset_path = f"{data_path}/{name}.csv"
        dataset_df = pd.read_csv(dataset_path)

        if species is None and tissue is None:
            dataset_df["cell_type_annotation_question"] = dataset_df.apply(lambda row: question_template["m"].format(marker_genes=row["marker"]), axis=1)
        elif species is None:
            dataset_df["cell_type_annotation_question"] = dataset_df.apply(lambda row: question_template["t"].format(tissue=row["tissue"], marker_genes=row["marker"]), axis=1)
        elif tissue is None:
            dataset_df["cell_type_annotation_question"] = dataset_df.apply(lambda row: question_template["s"].format(species=species, marker_genes=row["marker"]), axis=1)
        else:
            dataset_df["cell_type_annotation_question"] = dataset_df.apply(lambda row: question_template["s_t"].format(species=species, tissue=row["tissue"], marker_genes=row["marker"]), axis=1)

        if GPTCellType_flag:
            if species is None and tissue is None:
                dataset_df["cell_type_annotation_question"] = dataset_df.apply(lambda row: question_template["GPTCellType_m"].format(marker_genes=row["marker"]), axis=1)
            else:
                dataset_df["cell_type_annotation_question"] = dataset_df.apply(lambda row: question_template["GPTCellType"].format(species='' if species is None else species, tissue=row["tissue"] if row["tissue"] is not None else '', marker_genes=row["marker"]), axis=1)

        dataset_df.to_csv(f"{data_path}/{name}.csv", index=False)


def standardize_cell_type(cell_type):
    cell_type = cell_type.strip(' ')
    cell_type = re.sub(r'^\d+[\.\ -\-\:]\s*', '', cell_type)
    cell_type = cell_type.strip('.:- ')
    p = inflect.engine()
    singular_cell_type = p.singular_noun(cell_type) # convert to singular form
    if singular_cell_type:
        return singular_cell_type.lower()
    elif not singular_cell_type:
        return cell_type.lower().replace('cells', 'cell')


def structured_outputs(model): # TODO
    '''While the [gpt-4o-mini, gpt-4o-2024-08-06, and later] models natively support structured outputs, others like [gpt-3.5-turbo, Claude, ...] do not. This function can be used to convert structured outputs to a format that can be used by the model.'''
    pass

def extract_marker_genes_from_open_problem(open_problem, model):
    # extract marker genes from the open problem

    prompt = (
        f"Extract the marker genes group from the following open problem:\n\n"
        f"{open_problem}\n\n"
        f"Instructions:\n"
        f"1. Return only the marker genes group.\n"
        f"2. Separate each gene by a comma.\n"
        f"3. Do not include a period at the end.\n"
        f"4. Do not include any other text or comments.\n"
        f"5. If no marker genes are found, return 'No marker genes found.'"
    )
    completion = complete_text(prompt, log_file=None, model=model, temperature=0)

    return completion

def flatten(lst):
    return [item for sublist in lst for item in (sublist if isinstance(sublist, list) else [sublist])]

def combine_result(dataset_csv: str, result_txt: str, result_col_name_prefix: str) -> pd.DataFrame:
    dataset = pd.read_csv(dataset_csv)
    annotations = pd.read_csv(result_txt, sep='\t', header=None)
    dataset[f'{result_col_name_prefix}_annotation'] = annotations[0]

    return dataset

if __name__ == "__main__":
    all = pd.read_csv("data/GPTCellType/src/all.csv")
    split_dataset(all)
    construct_cell_type_annotation_questions(data_info, GPTCellType_flag=False)
    # print(extract_marker_genes_from_open_problem("I have a group of cells, the top 10 marker genes in the group are CD4, CD8, CD19, CD3, CD14, CD15, CD80, CD86, CD163, CD200. What is the cell type of this group of cells?", "gpt-4o-mini"))

    # model = 'o1-preview'
    # top_n = 3
    # max_marker_genes = "None"
    # dataset_name_list = ['Azimuth', 'HCA', 'literature', 'tabulasapiens', 'BCL', 'HCL', 'coloncancer', 'lungcancer', 'MCA']
    # for dataset_name in dataset_name_list:
    #     data = combine_result(f'data/GPTCellType/datasets/{dataset_name}.csv', f'analysis/o1-preview (for reproduce)/{dataset_name}/top_{top_n}_max_{max_marker_genes}.txt', f'{model}_top_{}')
    #     data.to_csv(f'data/GPTCellType/datasets/top_3/{dataset_name}.csv', index=False)

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
