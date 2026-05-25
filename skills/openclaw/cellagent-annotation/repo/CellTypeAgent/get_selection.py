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
import numpy as np
import pandas as pd
from tqdm import tqdm
from utils import standardize_cell_type
from eval import eval_cell_type_annotation_per_cell
from get_expression_score import load_expression_data
from get_prediction import get_CLname
from itertools import permutations

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

cl = pd.read_csv(os.path.join(SCRIPT_DIR, 'data/GPTCellType/src/compiled.csv'))
hier = pd.read_csv(os.path.join(SCRIPT_DIR, 'data/GPTCellType/src/relation.csv'), header=None)

expression_dir = os.path.join(SCRIPT_DIR, "data/CELLxGENE")
data_dir = os.path.join(SCRIPT_DIR, "data/GPTCellType/datasets")
saved_prediction_dir = os.path.join(SCRIPT_DIR, "analysis/o1-preview (for reproduce)")
data_file_names = ['BCL', 'coloncancer', 'lungcancer', 'literature', 'HCA', 'HCL', 'MCA', 'Azimuth', 'tabulasapiens']
no_tissue_data_names = ['HCL', 'MCA', 'BCL']

expression_file_names = {
    'tabulasapiens': [
        'TS_CELLxGENE_gene_expression_101124_0.csv',
        'TS_CELLxGENE_gene_expression_101124_1.csv',
        'TS_CELLxGENE_gene_expression_101124_2.csv',
        'TS_CELLxGENE_gene_expression_101124_3.csv',
    ],
    'Azimuth': [
        'Azimuth_CELLxGENE_gene_expression_101124_0.csv',
        'Azimuth_CELLxGENE_gene_expression_101124_1.csv',
        'Azimuth_CELLxGENE_gene_expression_101124_2.csv',
        'Azimuth_CELLxGENE_gene_expression_101124_3.csv',
        'Azimuth_CELLxGENE_gene_expression_101124_brain_0.csv',
        'Azimuth_CELLxGENE_gene_expression_101124_brain_1.csv',
        'Azimuth_CELLxGENE_gene_expression_101124_brain_2.csv',
        'Azimuth_CELLxGENE_gene_expression_101124_brain_3.csv'
    ],
    'literature': ['literature_CELLxGENE_gene_expression_101524.csv'],
    'MCA': ['MCA_CELLxGENE_gene_expression_101024.csv'],
    'HCA': ['HCA_CELLxGENE_gene_expression_100824.csv'],
    'HCL': ['HCL_CELLxGENE_gene_expression_101024.csv'],
    'BCL': ['BCL_CELLxGENE_gene_expression_102124.csv'],
    'lungcancer': ['lungcancer_CELLxGENE_gene_expression_101824.csv'],
    'coloncancer': ['coloncancer_CELLxGENE_gene_expression_101824.csv'],
}

data_to_expression_tissue_map = {
    'tabulasapiens': {
        'Bladder': 'bladder organ',
        'Blood': 'blood',
        'Bone Marrow': 'bone marrow',
        'Eye': 'eye',
        'Fat': 'adipose tissue',
        'Heart': 'heart',
        'Kidney': 'kidney',
        'Large Intestine': 'large intestine',
        'Liver': 'liver',
        'Lung': 'lung',
        'Lymph Node': 'lymph node',
        'Mammary': 'breast',
        'Muscle': 'musculature',
        'Pancreas': 'pancreas',
        'Prostate': 'prostate gland',
        'Salivary Gland': 'saliva',
        'Skin': 'skin of body',
        'Small Intestine': 'small intestine',
        'Spleen': 'spleen',
        'Thymus': 'breast',
        'Tongue': 'tongue',
        'Trachea': 'head',
        'Uterus': 'uterus',
        'Vasculature': 'vasculature'
    },
    'Azimuth': {
        'Adipose': 'adipose tissue',
        'Bone Marrow': 'bone marrow',
        'Fetal Development': 'embryo',
        'Heart': 'heart',
        'Kidney': 'kidney',
        'Liver': 'liver',
        'Lung': 'lung',
        'Motor Cortex': 'brain',
        'PBMC': 'blood',
        'Pancreas': 'pancreas',
        'Tonsil': 'lymph node'
    },
    'literature': {
        'Breast': 'breast',
        'Esophagus': 'esophagus',
        'Heart': 'heart',
        'Lung': 'lung',
        'Prostate': 'prostate gland',
        'Skeletal muscle': 'musculature',
        'Skin': 'skin of body'
    },
    'MCA': {
        'Adipose': 'adipose tissue',
        'Bone Marrow': 'bone marrow',
        'Fetal Development': 'embryo',
        'Heart': 'heart',
        'Kidney': 'kidney',
        'Liver': 'liver',
        'Lung': 'lung',
        'Motor Cortex': 'cortex',
        'PBMC': 'blood',
        'Pancreas': 'pancreas',
        'Tonsil': 'lymph node'
    },
    'HCA': {
        'Breast': 'breast',
        'Esophagus': 'esophagus',
        'Heart': 'heart',
        'Lung': 'lung',
        'Prostate': 'prostate gland',
        'Skeletal muscle': 'musculature',
        'Skin': 'skin of body'
    },
    'BCL': {
        'B cell lymphoma': 'bone marrow' # In cellxgene, only bone marrow includes disease B-cell non-Hodgkin lymphoma.
    },
    'lungcancer': {
        'lung cancer and brain metastasis': 'lung,brain',
    },
    'coloncancer': {
        'colon cancer': 'colon'
    },
}

data_to_expression_cell_name_map = {
    'fat cell': 'adipocyte',
}

def assign_ranks(input_list):
    unique_sorted = sorted(set(input_list))
    rank_dict = {value: rank for rank, value in enumerate(unique_sorted)}
    return [rank_dict[element] for element in input_list]

def get_expression_rank(
    dataset_name,
    sample,
    cellxgene_gene_expression,
    term_to_compare="Expression, Scaled",
    tissue_flag=True,
    tissue_aggregation="averaged",
    max_markers=None,
    top_n=None,
    mixture_strategy="mean" # "mean" or "max" or "sum"
):

    cell_type_pred_CLname = eval(sample['cell_type_pred_CLname']) if isinstance(sample['cell_type_pred_CLname'], str) else sample['cell_type_pred_CLname']

    cell_type_pred_CLname = [
        [data_to_expression_cell_name_map.get(cell_type, cell_type) for cell_type in candidate]
        for candidate in cell_type_pred_CLname
    ]

    if tissue_flag:
        tissue = sample['tissue']
        mapped_tissue = data_to_expression_tissue_map[dataset_name][tissue]
        mapped_tissue_ls = mapped_tissue.split(',') if ',' in mapped_tissue else [mapped_tissue]
    else:
        mapped_tissue_ls = []

    marker_genes = sample['marker'].replace(', ', ',').split(',')
    if max_markers is not None:
        marker_genes = marker_genes[:min(max_markers, len(marker_genes))]

    if tissue_aggregation == "averaged":
        return _averaged_mode(cell_type_pred_CLname, marker_genes, cellxgene_gene_expression, term_to_compare, tissue_flag,
        mapped_tissue_ls, mixture_strategy)
    elif tissue_aggregation == "tissue_wise":
        return _tissue_wise_mode(cell_type_pred_CLname, marker_genes, cellxgene_gene_expression, term_to_compare, tissue_flag,
        mapped_tissue_ls, mixture_strategy)
    else:
        raise ValueError(f"Invalid tissue aggregation mode: {tissue_aggregation}")

def _averaged_mode(candidates, markers, expr_df, term, use_tissue, tissues, strategy):
    expression_list = []
    total_scores = []

    for candidate in candidates:
        candidate_expression = []
        comp_scores = []

        for ct in candidate:
            if ct == "unknown":
                candidate_expression.append([0] * len(markers))
                comp_scores.append(0)
                continue

            if use_tissue:
                sample_cellxgene = expr_df[
                    (expr_df['Cell Type'] == ct) &
                    (expr_df['Tissue'].isin(tissues))
                ]
            else:
                sample_cellxgene = expr_df[expr_df['Cell Type'] == ct]

            filtered_expression = sample_cellxgene[sample_cellxgene['Gene Symbol'].isin(markers)]
            scaled_expression_score = []

            for gene in markers:
                if gene in filtered_expression['Gene Symbol'].to_list():
                    exp_values = filtered_expression[filtered_expression['Gene Symbol'] == gene][term].values
                    gene_score = float(sum(exp_values) / len(exp_values))
                else:
                    gene_score = 0

                scaled_expression_score.append(gene_score)

            candidate_expression.append(scaled_expression_score)
            comp_scores.append(sum(scaled_expression_score))

        merged_expression = _merge_expression(candidate_expression, strategy)
        merged_score = _merge_scores(comp_scores, strategy)

        expression_list.append(merged_expression)
        total_scores.append(merged_score)

    final_rank = assign_ranks(total_scores)

    return final_rank, expression_list


def _tissue_wise_mode(candidates, markers, expr_df, term, use_tissue, tissues, mixture_strategy):

    processed_candidates = [
        list(candidate) if isinstance(candidate, (tuple, list)) else [candidate]
        for candidate in candidates
    ]

    all_components = [ct for candidate in processed_candidates for ct in candidate]

    if use_tissue:
        data = expr_df[expr_df['Tissue'].isin(tissues)]
    else:
        data = expr_df.copy()

    filtered_data = data[data['Gene Symbol'].isin(markers)]

    tissue_groups = filtered_data.groupby('Tissue')
    tissue_cell_dict = {
        tissue: set(group['Cell Type'].unique())
        for tissue, group in tissue_groups
    }

    cell_set = set(all_components)
    full_match_tissues = [
        tissue for tissue, cells in tissue_cell_dict.items()
        if cell_set.issubset(cells)
    ]

    component_scores = {ct: 0 for ct in all_components}

    def calculate_score(tissue_data, cell_type):
        return tissue_data[tissue_data['Cell Type'] == cell_type][term].sum()

    if full_match_tissues:
        for tissue in full_match_tissues:
            tissue_data = tissue_groups.get_group(tissue)
            for ct in all_components:
                component_scores[ct] += calculate_score(tissue_data, ct)

    else:
        cell_pairs = [(c1, c2) for i, c1 in enumerate(all_components) for c2 in all_components[i+1:]]

        for ct1, ct2 in cell_pairs:
            pair_tissues = [
                tissue for tissue, cells in tissue_cell_dict.items()
                if ct1 in cells and ct2 in cells
            ]
            if not pair_tissues:
                continue

            score1, score2 = 0, 0
            for tissue in pair_tissues:
                tissue_data = tissue_groups.get_group(tissue)
                score1 += calculate_score(tissue_data, ct1)
                score2 += calculate_score(tissue_data, ct2)

            if score1 == score2:
                if score1 != 0:
                    component_scores[ct1] += 0.5
                    component_scores[ct2] += 0.5
            else:
                winner = ct1 if score1 > score2 else ct2
                component_scores[winner] += 1

    candidate_scores = []
    for candidate in processed_candidates:
        scores = [component_scores[ct] for ct in candidate]

        if mixture_strategy == "mean":
            merged_score = np.mean(scores)
        elif mixture_strategy == "max":
            merged_score = np.max(scores)
        elif mixture_strategy == "sum":
            merged_score = np.sum(scores)
        else:
            raise ValueError(f"Invalid mixture strategy: {mixture_strategy}")

        candidate_scores.append(merged_score)

    sorted_scores = sorted(enumerate(candidate_scores), key=lambda x: x[1], reverse=True)
    rank_dict = {}
    for rank, (idx, score) in enumerate(sorted_scores):
        rank_dict[idx] = rank
    final_rank = [rank_dict[i] for i in range(len(candidate_scores))]

    expression_list = [[score] for score in candidate_scores]

    return final_rank, expression_list


def _merge_expression(expression_lists, strategy):
    if len(expression_lists) == 1:
        return expression_lists[0]

    merged = []
    for gene_scores in zip(*expression_lists):
        if strategy == "mean":
            merged.append(np.mean(gene_scores))
        elif strategy == "max":
            merged.append(np.max(gene_scores))
        elif strategy == "sum":
            merged.append(np.sum(gene_scores))
    return merged

def _merge_scores(scores, strategy):
    if len(scores) == 1:
        return scores[0]
    return {
        "mean": np.mean,
        "max": np.max,
        "sum": np.sum
    }[strategy](scores)

def calculate_agreement_scores(
    data,
    cellxgene_gene_expression_dict,
    tissue_flag=True,
    max_markers=None,
    top_n=3,
    cl=cl,
    hier=hier,
    mixture_strategy="mean"
):
    agreement_score = data['agreement_score']
    results = {'agreement_score': [], 'final_candidate': [], 'final_candidate_seq': []}

    if tissue_flag:
        for i in tqdm(range(len(data))):
            candidate_scores = [float(x) for x in agreement_score[i].strip('[]').replace(' ', '').split(',')]
            dataset_name = data.iloc[i]['dataset']
            cellxgene_gene_expression = cellxgene_gene_expression_dict[dataset_name]

            ranks = [
                get_expression_rank(
                    dataset_name, data.iloc[i], cellxgene_gene_expression,
                    "Expression, Scaled", True, "averaged", max_markers,
                    mixture_strategy=mixture_strategy
                )[0],

                get_expression_rank(
                    dataset_name, data.iloc[i], cellxgene_gene_expression,
                    "Expressed in Cells", True, "averaged", max_markers,
                    mixture_strategy=mixture_strategy
                )[0],

                get_expression_rank(
                    dataset_name, data.iloc[i], cellxgene_gene_expression,
                    "Expression, Scaled", False, "averaged", max_markers,
                    mixture_strategy=mixture_strategy
                )[0]
            ]

            base_ranks = np.arange(top_n-1, -1, -1) * 3 / top_n
            combo_scores = np.sum(ranks, axis=0) + base_ranks
            results['agreement_score'].append(candidate_scores[np.argmax(combo_scores)])
            results['final_candidate'].append(data.iloc[i]['cell_type_pred'][np.argmax(combo_scores)])
            results['final_candidate_seq'].append(np.argmax(combo_scores))
    else:
        for i in tqdm(range(len(data))):
            candidate_scores = [float(x) for x in agreement_score[i].strip('[]').replace(' ', '').split(',')]
            dataset_name = data.iloc[i]['dataset']
            cellxgene_gene_expression = cellxgene_gene_expression_dict[dataset_name]

            ranks = [
                get_expression_rank(
                    dataset_name, data.iloc[i], cellxgene_gene_expression,
                    "Expression, Scaled", False, "averaged", max_markers,
                    mixture_strategy=mixture_strategy
                )[0],
                get_expression_rank(
                    dataset_name, data.iloc[i], cellxgene_gene_expression,
                    "Expressed in Cells", False, "averaged", max_markers,
                    mixture_strategy=mixture_strategy
                )[0],
                get_expression_rank(
                    dataset_name, data.iloc[i], cellxgene_gene_expression,
                    "Expression, Scaled", False, "tissue_wise", max_markers,
                    mixture_strategy=mixture_strategy
                )[0]
            ]

            base_ranks = np.arange(top_n-1, -1, -1) * 3 / top_n

            combo_scores = np.sum(ranks, axis=0) + base_ranks
            results['agreement_score'].append(candidate_scores[np.argmax(combo_scores)])
            results['final_candidate'].append(data.iloc[i]['cell_type_pred'][np.argmax(combo_scores)])
            results['final_candidate_seq'].append(np.argmax(combo_scores))

    return results

def clname_padding(clname_df, top_n=3, col_name='cell_type_pred'):
    mask = clname_df[col_name].apply(len) < top_n

    clname_df.loc[mask, col_name] = clname_df.loc[mask, col_name].apply(
        lambda x: x + [['unknown']] * (top_n - len(x))
    )

    clname_df.loc[mask, col_name] = clname_df.loc[mask, col_name].apply(
        lambda x: x[:top_n]
    )
    return clname_df

def get_hit_rate(pred, ground_truth, cl, hier, as_string=False):
    pred_name_list = pred.columns.tolist()
    hit_rate_df = pd.DataFrame(index=pred.index, columns=pred_name_list)
    n_sample_per_mixture_pair = len(ground_truth)

    def calculate_single_cell_scores(pred_cell, ground_truth_cells):
        return [
            eval_cell_type_annotation_per_cell(pred_cell, gt_cell, cl, hier)
            for gt_cell in ground_truth_cells
        ]

    def get_best_permutation_score(scores_list, n_items):
        best_score = 0
        for perm in permutations(range(n_items), min(len(scores_list), n_items)):
            current_scores = [scores_list[pred_idx] for pred_idx in range(len(perm))]
            best_score = max(best_score, np.mean(current_scores))
        return best_score

    def evaluate_cell_mixture(pred_cell, ground_truth_cells):
        if len(pred_cell) == 1:
            scores = calculate_single_cell_scores(pred_cell[0], ground_truth_cells)
            return np.mean(scores)

        mixture_scores = [
            calculate_single_cell_scores(single_cell, ground_truth_cells)
            for single_cell in pred_cell
        ]

        best_mixture_score = 0
        for perm in permutations(range(len(ground_truth_cells)), min(len(pred_cell), len(ground_truth_cells))):
            current_scores = [mixture_scores[pred_idx][gt_idx]
                            for pred_idx, gt_idx in enumerate(perm)]
            best_mixture_score = max(best_mixture_score, np.mean(current_scores))

        return best_mixture_score

    for pred_name in pred_name_list:
        pred_ls = pred[pred_name].apply(lambda x: eval(x) if isinstance(x, str) else x).tolist()

        for i in tqdm(range(len(pred_ls)), desc=f'Processing {pred_name}'):
            ground_truth_cells = [
                ground_truth[j].iloc[i].to_dict()
                for j in range(n_sample_per_mixture_pair)
            ]

            pred_cells = pred_ls[i]

            score_matrix = [
                evaluate_cell_mixture(pred_cell, ground_truth_cells)
                for pred_cell in pred_cells
            ]

            best_score = (score_matrix[0] if len(pred_cells) == 1 else get_best_permutation_score(score_matrix, len(ground_truth_cells)))

            hit_rate_df.at[i, pred_name] = (
                str(score_matrix) if as_string else (best_score, 0)
            )

    return hit_rate_df

def show_hit_rate(hit_rate_df, show_index=True):
    for col in hit_rate_df.columns:
        print("-"*77)
        print(f"{col} hit rate: {hit_rate_df[col].apply(lambda x: x[0]).mean()}")
        if show_index:
            print(f"{col} index: {hit_rate_df[col].apply(lambda x: x[1]).mean()}")
        print("-"*77)

def process_dataset(path_df_with_pred, expression_dir=expression_dir, top_n=3, cl=cl, hier=hier,
                    tissue_flag=True, max_markers=None, n_sample_per_mixture_pair=1):

    data = pd.read_csv(path_df_with_pred)
    contained_datasets = data['dataset'].unique()

    expression_data_dict = {}
    for dataset in contained_datasets:
        tmp_expression_data = load_expression_data(expression_file_names[dataset], expression_dir)
        tmp_expression_data['Expressed in Cells'] = tmp_expression_data['Number of Cells Expressing Genes'] / tmp_expression_data['Cell Count']
        tmp_expression_data['Expressed in Cells'] = tmp_expression_data['Expressed in Cells'].fillna(0)
        tmp_expression_data['Expression, Scaled'] = tmp_expression_data['Expression, Scaled'].fillna(0)
        expression_data_dict[dataset] = tmp_expression_data

    data = clname_padding(data, top_n=top_n, col_name='cell_type_pred')
    data = clname_padding(data, top_n=top_n, col_name='cell_type_pred_CLname')

    saved_prediction = data[['cell_type_pred']].copy()
    saved_prediction["cell_type_pred"] = saved_prediction["cell_type_pred"].apply(
        lambda x: eval(x) if isinstance(x, str) and '[[' in x else ([ [x] ] if isinstance(x, str) else x)
    )

    saved_prediction["cell_type_pred_1st"] = saved_prediction["cell_type_pred"].apply(lambda x: [x[0]])

    ground_truth = {}
    if n_sample_per_mixture_pair > 1:
        for i in range(n_sample_per_mixture_pair):
            ground_truth[i] = data[[f"manual_annotation_{i}", f"manual_CLname_{i}", f"manual_CLID_{i}", f"manual_broadtype_{i}"]].copy().rename(
                columns={
                    f"manual_annotation_{i}": "manual_annotation",
                    f"manual_CLname_{i}": "manual_CLname",
                    f"manual_CLID_{i}": "manual_CLID",
                    f"manual_broadtype_{i}": "manual_broadtype"
                }
            )
    else:
        ground_truth[0] = data[["manual_annotation", "manual_CLname", "manual_CLID", "manual_broadtype"]]

    hit_rate_df = get_hit_rate(saved_prediction, ground_truth, cl, hier, as_string=False)
    hit_rate_df_str = get_hit_rate(saved_prediction, ground_truth, cl, hier, as_string=True)
    show_hit_rate(hit_rate_df)
    agreement_score = hit_rate_df_str["cell_type_pred"]
    data['agreement_score'] = agreement_score

    data["cell_type_pred"] = data["cell_type_pred"].apply(
        lambda x: eval(x) if isinstance(x, str) and '[[' in x else ([ [x] ] if isinstance(x, str) else x)
    )
    data["cell_type_pred_CLname"] = data["cell_type_pred_CLname"].apply(
        lambda x: eval(x) if isinstance(x, str) and '[[' in x else ([ [x] ] if isinstance(x, str) else x)
    )
    agreement_score_dict = calculate_agreement_scores(
        data, expression_data_dict, tissue_flag=tissue_flag, max_markers=max_markers, top_n=top_n
    )
    data['final_score'] = agreement_score_dict['agreement_score']

    ours = sum(agreement_score_dict['agreement_score']) / len(data)
    direct_top_1 = [float(x.strip('[]').replace(' ', '').split(',')[0]) for x in agreement_score]
    direct_top_1_mean = sum(direct_top_1) / len(data)

    if len(contained_datasets) == 1:
        results_string = f"{dataset_name} | ours: {ours}"
    else:
        mixed_annotation_sep_avg_score = []
        for i in range(len(data)):
            sep_avg_score = 0
            for j in range(n_sample_per_mixture_pair):
                sep_avg_score += eval(data[f'final_score_{j}'][i]) if isinstance(data[f'final_score_{j}'][i], str) else data[f'final_score_{j}'][i]
            mixed_annotation_sep_avg_score.append(sep_avg_score / n_sample_per_mixture_pair)
        final_avg_sep_score = sum(mixed_annotation_sep_avg_score) / len(data)
        data['final_score_sep_avg'] = mixed_annotation_sep_avg_score
        results_string = f"{contained_datasets} | ours: {ours} ; average of separated annotation scores: {final_avg_sep_score}"
    if n_sample_per_mixture_pair <= 1:
        results_string += f", direct_top_1: {direct_top_1_mean}"
    print(results_string)

    data['best_candidate_index'] = data['agreement_score'].apply(lambda x: np.argmax(eval(x)))
    data['final_annotation'] = data.apply(lambda row: row['cell_type_pred'][row['best_candidate_index']], axis=1)
    data['final_CLname'] = data.apply(lambda row: row['cell_type_pred_CLname'][row['best_candidate_index']], axis=1)

    return data, agreement_score_dict, ours, direct_top_1_mean


if __name__ == "__main__":
    top_n = 3
    max_markers = None
    results = {}
    all_data = []
    n_sample_per_mixture_pair = 1
    model = 'o1-preview'

    data_file_names = ['coloncancer', 'BCL', 'lungcancer', 'literature', 'HCA', 'HCL', 'MCA', 'Azimuth', 'tabulasapiens']

    for dataset_name in data_file_names:
        print(f"Processing dataset: {dataset_name}")
        tissue_flag = True if dataset_name not in no_tissue_data_names else False
        path_df_with_pred = os.path.join(f"data/GPTCellType/datasets/{model}/top_{top_n}", f"{dataset_name}.csv")
        data, agreement_score_dict, ours, direct_top_1_mean = process_dataset(path_df_with_pred, tissue_flag=tissue_flag, max_markers=max_markers, top_n=top_n, n_sample_per_mixture_pair=n_sample_per_mixture_pair)
        results[dataset_name] = {
            'data': data,
            'agreement_score_dict': agreement_score_dict,
            'ours': ours,
            'direct_top_1_mean': direct_top_1_mean
        }
        data['dataset'] = dataset_name
        all_data.append(data)
        if os.path.exists(os.path.join(saved_prediction_dir, dataset_name)):
            data.to_csv(os.path.join(saved_prediction_dir, dataset_name, f"top_{top_n}_max_{max_markers}.csv"), index=False)
        else:
            os.makedirs(os.path.join(saved_prediction_dir, dataset_name))
            data.to_csv(os.path.join(saved_prediction_dir, dataset_name, f"top_{top_n}_max_{max_markers}.csv"), index=False)
        print(f"Completed processing {dataset_name}\n")

    dir_to_merged_data = os.path.join(saved_prediction_dir, "All", "Results")
    if not os.path.exists(dir_to_merged_data):
        os.makedirs(dir_to_merged_data)
    merged_df = pd.concat(all_data, ignore_index=True)
    merged_df.to_csv(os.path.join(saved_prediction_dir, "All", "Results", f"merged_top_{top_n}_max_{max_markers}.csv"), index=False)

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
