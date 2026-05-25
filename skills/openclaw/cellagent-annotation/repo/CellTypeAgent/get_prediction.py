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
import time
import pandas as pd
from utils import data_info
from LLM import complete_text
from utils import standardize_cell_type
from eval import match_CLID, match_CL_info

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

cl = pd.read_csv(os.path.join(SCRIPT_DIR, 'data/GPTCellType/src/compiled.csv'))
hier = pd.read_csv(os.path.join(SCRIPT_DIR, 'data/GPTCellType/src/relation.csv'), header=None)

def create_predicition_prompt(dataset_name, number_of_candidates=3, data_dir='Data/GPTCellType/datasets', data_info=data_info, index_to_predict=None, poor_performance_model=False, max_markers=None, prompt_suffix="", species=None):
    data_dir = os.path.join(SCRIPT_DIR, data_dir)
    data = pd.read_csv(os.path.join(data_dir, f'{dataset_name}.csv'))

    print("--------------------------------")
    print(data_dir)
    print("--------------------------------")

    species = next(item for item in data_info if item["name"] == dataset_name)["species"] if species is None else species
    if index_to_predict is not None:
        data = data.iloc[index_to_predict]

    has_tissues = not data['tissue'].isna().all()
    tissue_prompt = ' and separated by tissue types' if has_tissues else ''

    poor_performance_model_prompt = f"Do remember that each row must contain exactly {number_of_candidates} cell types." if poor_performance_model else ""

    base_prompt = f"""
Identify most likely top {number_of_candidates} cell types of {species} cells using the following markers separately for each row. Only provide the lists of top {number_of_candidates} cell type names row by row. The higher the probability, the further left it is ranked, separated by commas. The number of lists should match the corresponding number of rows in the input. Answer for each row should start with the index number followed by a ': ' and then the predicted cell type names. {poor_performance_model_prompt}
{prompt_suffix}

Here are the marker gene lists, organized row by row{tissue_prompt}:
"""
    if has_tissues:
        for tissue in data['tissue'].unique():
            marker_lists = []
            tissue_data = data[data['tissue'] == tissue]
            base_prompt += f"\n{tissue}:\n"
            for _, row in tissue_data.iterrows():
                markers_num = len(row['marker'].split(','))
                markers = row['marker'].split(',')[:min(max_markers, markers_num)] if max_markers else row['marker'].split(',')
                marker_list = ','.join(markers)
                marker_lists.append(f"{int(row.name)}: {marker_list}")

            marker_lists.append("")
            base_prompt += "\n".join(marker_lists)
    else:
        marker_lists = []
        for _, row in data.iterrows():
            markers_num = len(row['marker'].split(','))
            markers = row['marker'].split(',')[:min(max_markers, markers_num)] if max_markers else row['marker'].split(',')
            marker_list = ','.join(markers)
            marker_lists.append(f"{int(row.name)}: {marker_list}")
        base_prompt += "\n".join(marker_lists)

    print(base_prompt)
    return base_prompt

def parse_prediction(prediction, data, end_idx, open_reasoning=False):
    if open_reasoning:
        print(prediction.split('</think>')[0])
        prediction = prediction.split('</think>')[-1].lstrip('\n')

    lines = [line.strip() for line in prediction.split('\n') if line.strip()]
    missing_indices = []

    for line in lines:
        try:
            index_str, cell_types = line.split(':', -1)
            index = int(index_str.strip())
            data.at[index, 'cell_type_pred'] = cell_types.strip()
        except:
            continue

    missing_indices = [index for index in data.index[:end_idx] if data.loc[index, 'cell_type_pred'] is None]

    return data, missing_indices

def mask_duplicate_cells(cells):
    seen = set()
    result = []
    for cell_group in cells:
        group_key = tuple(cell_group) if isinstance(cell_group, list) else cell_group

        if group_key in seen:
            result.append(['unknown'])
        else:
            seen.add(group_key)
            result.append(cell_group)

    return result

def get_CLname(data_with_prediction, cl=cl):
    def process_cell_type(cell_type):
        if len(cell_type) > 1:
            CLname_mixture = []
            for sub_type in cell_type:
                CLID = match_CLID(sub_type.strip(), cl)
                CLname, _ = match_CL_info(CLID, cl, sub_type.strip())
                CLname_mixture.append(CLname)
            return CLname_mixture
        elif len(cell_type) == 1:
            CLID = match_CLID(cell_type[0].strip(), cl)
            CLname, _ = match_CL_info(CLID, cl, cell_type[0].strip())
            return [CLname]

    data_with_prediction['cell_type_pred_CLname'] = None
    for i in range(len(data_with_prediction)):
        pred = eval(data_with_prediction.loc[i, 'cell_type_pred']) if isinstance(
            data_with_prediction.loc[i, 'cell_type_pred'], str
        ) else data_with_prediction.loc[i, 'cell_type_pred']

        CLname_ls = []
        for cell_type in pred:
            CLname = process_cell_type(cell_type)
            CLname_ls.append(CLname)

        data_with_prediction.at[i, 'cell_type_pred_CLname'] = mask_duplicate_cells(CLname_ls)

    return data_with_prediction

def filter_predictions(predictions):
    predictions = predictions.copy()
    for index, prediction in enumerate(predictions['cell_type_pred']):
        preds = prediction.replace(', ', ',').split(',')
        for i, p in enumerate(preds):
            if 'mixture' in p:
                mixture = [standardize_cell_type(cell_type) for cell_type in p.replace('mixture of ', '').replace('a ', '').split(' and ')]
                preds[i] = mixture
            else:
                preds[i] = [standardize_cell_type(p)]
        predictions.at[index, 'cell_type_pred'] = str(preds)
    return predictions

def get_prediction(model, dataset_name, number_of_candidates=3, data_dir='Data/GPTCellType/datasets', cl=cl, log_dir='logs/selection_mode', poor_performance_model=False, max_markers=None, prompt_suffix="", species=None):
    date = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    log_dir = os.path.join(SCRIPT_DIR, log_dir, dataset_name, 'prediction', model, date)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    data_dir = os.path.join(SCRIPT_DIR, data_dir)
    data = pd.read_csv(os.path.join(data_dir, f'{dataset_name}.csv'))
    num_samples = len(data)
    segment_size = 50
    data['cell_type_pred'] = None
    if model == 'deepseek-r1':
        open_reasoning = True
    else:
        open_reasoning = False

    missing_indices = []
    for i in range(0, num_samples, segment_size):
        end_idx = min(i + segment_size, num_samples)
        index_to_predict = list(set(list(data.index[i:end_idx]) + missing_indices))
        prediction_prompt = create_predicition_prompt(dataset_name, number_of_candidates, index_to_predict=index_to_predict, poor_performance_model=poor_performance_model, max_markers=max_markers, prompt_suffix=prompt_suffix, species=species, data_dir=data_dir)
        prediction = complete_text(prediction_prompt, log_file=os.path.join(log_dir, f'{i}-{end_idx}.log'), model=model)
        data, missing_indices = parse_prediction(prediction, data, end_idx=end_idx, open_reasoning=open_reasoning)

    if len(missing_indices) != 0:
        prediction_prompt = create_predicition_prompt(dataset_name, number_of_candidates, index_to_predict=missing_indices, poor_performance_model=poor_performance_model, prompt_suffix=prompt_suffix, species=species, data_dir=data_dir)
        prediction = complete_text(prediction_prompt, log_file=os.path.join(log_dir, f'missing_indices.log'), model=model)
        data, missing_indices = parse_prediction(prediction, data, end_idx=end_idx, open_reasoning=open_reasoning)

    data = filter_predictions(data)
    data['cell_type_pred_CLname'] = None
    data = get_CLname(data, cl)
    data.to_csv(os.path.join(log_dir, f'{dataset_name}.csv'), index=False)

    return data, os.path.join(log_dir, f'{dataset_name}.csv')

if __name__ == "__main__":
    datasets = ['coloncancer', 'BCL', 'lungcancer', 'literature', 'HCA', 'HCL', 'MCA', 'Azimuth', 'tabulasapiens']
    for dataset_name in datasets:
        model, dataset_name, top_n, max_markers = 'o1-preview', dataset_name, 3, None
        log_dir = f'data/GPTCellType/datasets/{model}/top_{top_n}'
        path_to_saved_prediction = f"analysis/{model}/{dataset_name}"
        if not os.path.exists(path_to_saved_prediction):
            os.makedirs(path_to_saved_prediction)
        data, log_path = get_prediction(model, dataset_name, poor_performance_model=False, max_markers=max_markers, number_of_candidates=top_n)
        data['cell_type_pred'].to_csv(os.path.join(path_to_saved_prediction, f'top_{top_n}_max_{max_markers}.txt'), index=False, header=False)
        print(f"{dataset_name}:\n", data['cell_type_pred'], '\n')

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
