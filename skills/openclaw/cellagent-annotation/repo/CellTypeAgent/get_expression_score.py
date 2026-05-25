# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import re
import time
import inflect
import numpy as np
import pandas as pd
from tqdm import tqdm
from ols_py.client import Ols4Client
from utils import standardize_cell_type, data_info
from eval import match_CLID, match_CL_info

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

def load_expression_data(file_list, file_dir):
    expression_data = pd.DataFrame()
    for file in file_list:
        data = pd.read_csv(f"{file_dir}/{file}", comment='#', skipinitialspace=True)
        expression_data = pd.concat([expression_data, data], axis=0)

    return expression_data

def get_expression(dataset_name, sample, cellxgene_gene_expression, term_to_compare="Expression, Scaled", tissue_flag=True):
    if tissue_flag:
        tissue = sample['tissue']
        mapped_tissue = data_to_expression_tissue_map[dataset_name][tissue]
        if len(mapped_tissue.split(',')) > 1:
            mapped_tissue_ls = mapped_tissue.split(',')
        else:
            mapped_tissue_ls = [mapped_tissue]

    marker_genes = sample['marker'].replace(' ', '').split(',')
    cell_type_pred_CLname = sample['cell_type_pred_CLname']
    if cell_type_pred_CLname[0] in data_to_expression_cell_name_map:
        cell_type_pred_CLname[0] = data_to_expression_cell_name_map[cell_type_pred_CLname[0]]

    expression_list = []
    for cell_type in cell_type_pred_CLname:
        if cell_type != "unknown":
            if tissue_flag:
                sample_cellxgene = cellxgene_gene_expression[(cellxgene_gene_expression['Cell Type'] == cell_type) & (cellxgene_gene_expression['Tissue'].isin(mapped_tissue_ls))]
            else:
                sample_cellxgene = cellxgene_gene_expression[(cellxgene_gene_expression['Cell Type'] == cell_type)]
            filtered_expression = sample_cellxgene[sample_cellxgene['Gene Symbol'].isin(marker_genes)]

            scaled_expression_score = []
            for gene in marker_genes:
                if gene in filtered_expression['Gene Symbol'].to_list():
                    scaled_expression_score.append(float(sum(filtered_expression[filtered_expression['Gene Symbol'] == gene][term_to_compare].values)/len(filtered_expression[filtered_expression['Gene Symbol'] == gene])))
                else:
                    scaled_expression_score.append(0)
            expression_list.append(scaled_expression_score)
        else:
            expression_list.append([0] * len(marker_genes))
    return expression_list

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
