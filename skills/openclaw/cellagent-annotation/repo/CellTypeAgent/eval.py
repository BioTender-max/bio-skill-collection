# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import pandas as pd
import numpy as np
from ols_py.client import Ols4Client
from utils import standardize_cell_type
from utils import flatten
import time

def CL_term_search(cell_type):
    # Find the unambiguous cell ontology (CL) term for the given natural language cell type via OLS4.
    client = Ols4Client()
    resp = client.select(cell_type, params={"ontology": "cl"})

    if resp.response.numFound == 0:
        terms = ["unknown"]
    else:
        terms = [doc.obo_id for doc in resp.response.docs]
        terms = [term for term in terms if term.startswith("CL:") or term.startswith("cl:")] # Drop those not in CL

    return terms[0]

def match_CLID(cell_type, cl):
    cell_type = standardize_cell_type(cell_type)

    if len(cl[cl['originalname'] == cell_type]) > 0:
        CLID = cl[cl['originalname'] == cell_type]['CLID'].values[0]
    elif len(cl[cl['Clname'] == cell_type]) > 0:
        CLID = cl[cl['Clname'] == cell_type]['CLID'].values[0]
    elif len(cl[cl['originalname'].str.contains(cell_type)]) > 0:
        CLID = cl[cl['originalname'].str.contains(cell_type)]['CLID'].values[0]
    else:
        CLID = None
        max_retry = 3
        while True and max_retry > 0:
            max_retry -= 1
            try:
                CLID = CL_term_search(cell_type)
                if len(CLID) > 0:
                    break
            except:
                print("Rate limit reached. Waiting for 1 seconds")
                time.sleep(1)
            if max_retry == 0 and CLID == None:
                CLID = "unknown"

    return CLID

def match_CL_info(CLID, cl, cell_type=None):
    CLname = cl.loc[cl['CLID'] == CLID, 'Clname'].values[0] if len(cl.loc[cl['CLID'] == CLID, 'Clname']) > 0 else "unknown"
    broadtype = cl.loc[cl['CLID'] == CLID, 'type'].values[0] if len(cl.loc[cl['CLID'] == CLID, 'type']) > 0 else "unknown"

    if cell_type is not None: # For those without CLID
        broadtype = cl.loc[cl['originalname'] == cell_type, 'type'].values[0] if len(cl.loc[cl['originalname'] == cell_type, 'type']) > 0 else broadtype

    return CLname, broadtype

def get_dataset_wise_CL_info(model, dataset_with_model_anno, cl):
    anno_col = model + "_annotation"
    CLID_col = model + "_CLID"
    CLname_col = model + "_CLname"
    broadtype_col = model + "_broadtype"

    for i, row in dataset_with_model_anno.iterrows():
        cell_type = row[anno_col]

        if pd.isna(cell_type):
            cell_type, CLID, CLname, broadtype = "unknown", "unknown", "unknown", "unknown"
        else:
            CLID = match_CLID(cell_type, cl)
            CLname, broadtype = match_CL_info(CLID, cl, cell_type)
            if cell_type in set(cl['type']):
                broadtype = cell_type
            elif cell_type == "cancer-associated fibroblast" or cell_type == "cancer-associated fibroblast (caf)":
                broadtype = "fibroblast"

        time.sleep(1)
        dataset_with_model_anno.at[i, CLID_col], dataset_with_model_anno.at[i, CLname_col], dataset_with_model_anno.at[i, broadtype_col] = CLID, CLname, broadtype

    return dataset_with_model_anno

def compute_partscore(model, dataset_with_model_CL, hier):
    hier = pd.concat([hier, hier.iloc[:, [1, 0]].rename(columns={1: 0, 0: 1})])

    hv = {}
    for key, value in zip(hier[1], hier[0]):
        if key not in hv:
            hv[key] = [value]
        else:
            hv[key].append(value)

    broadtype_col = model + "_broadtype"
    agreement_col = model + "_agreement"

    for i, row in dataset_with_model_CL.iterrows():
        t1 = set(row['manual_broadtype'].split(','))
        t2 = set(row[broadtype_col].split(','))
        t1 = t1.union(set(flatten([hv.get(x) for x in t1])))
        t2 = t2.union(set(flatten([hv.get(x) for x in t2])))

        intersection = t1.intersection(t2)
        intersection = intersection - {"unknown", None}
        dataset_with_model_CL.at[i, agreement_col] = 0.5 if (len(intersection)>0) else 0

    return dataset_with_model_CL

def compute_fullscore(model, dataset_with_model_CL):
    CLname_col = model + "_CLname"
    broadtype_col = model + "_broadtype"
    agreement_col = model + "_agreement"
    annotation_col = model + "_annotation"

    for i, row in dataset_with_model_CL.iterrows():
        if pd.isna(row['manual_CLname']) or pd.isna(row[CLname_col]):
            s2 = pd.Series([row['manual_annotation']])[0] == pd.Series([row[annotation_col]])[0]
            s3 = row['manual_broadtype'] == 'malignant cell' and row[broadtype_col] == 'malignant cell'
            dataset_with_model_CL.at[i, agreement_col] = 1 if (s2 or s3) else dataset_with_model_CL.at[i, agreement_col]
        else:
            t1 = set(row['manual_CLname'].split(','))
            t2 = set(row[CLname_col].split(','))
            s1 = len(t1.intersection(t2)) / len(t1.union(t2)) == 1 if len(t1.union(t2)-{"unknown", None}) > 0 else False
            s2 = pd.Series([row['manual_annotation']])[0] == pd.Series([row[annotation_col]])[0]
            s3 = row['manual_broadtype'] == 'malignant cell' and row[broadtype_col] == 'malignant cell'
            dataset_with_model_CL.at[i, agreement_col] = 1 if (s1 or s2 or s3) else dataset_with_model_CL.at[i, agreement_col]

    return dataset_with_model_CL

def eval_cell_type_annotation(model, dataset_with_model_anno, cl, hier):
    dataset_with_model_CL = get_dataset_wise_CL_info(model, dataset_with_model_anno, cl)
    dataset_with_model_CL = compute_partscore(model, dataset_with_model_CL, hier)
    dataset_with_model_CL = compute_fullscore(model, dataset_with_model_CL)

    return dataset_with_model_CL

def eval_cell_type_annotation_per_cell(pred_cell_type, true_cell_type, cl, hier):
    """This function is a cell-level version of eval_cell_type_annotation(). It evaluates the accuracy of a single cell type prediction by comparing it to the true cell type.
    """

    def standardize_and_match_CLID(cell_type):
        cell_type = standardize_cell_type(cell_type)
        return match_CLID(cell_type, cl)

    def get_broadtype(CLID):
        return cl.loc[cl['CLID'] == CLID, 'type'].values[0] if len(cl.loc[cl['CLID'] == CLID, 'type']) > 0 else "unknown"

    def compute_partscore(pred_broadtype, true_broadtype):
        hier_dict = dict(zip(hier[1], hier[0]))
        hier_dict.update(dict(zip(hier[0], hier[1])))

        t1 = set(true_broadtype.split(','))
        t2 = set(pred_broadtype.split(','))

        t1 = t1.union(set(flatten([hier_dict.get(x, []) for x in t1])))
        t2 = t2.union(set(flatten([hier_dict.get(x, []) for x in t2])))

        intersection = t1.intersection(t2) - {"unknown", None}
        return 0.5 if len(intersection) > 0 else 0

    def compute_fullscore(pred_cell_type, true_cell_type, pred_broadtype, true_broadtype):
        pred_CLID = standardize_and_match_CLID(pred_cell_type)
        pred_CLID = pred_CLID if pd.notna(pred_CLID) else "unknown"
        true_CLID = true_cell_type['manual_CLID'] if pd.notna(true_cell_type['manual_CLID']) else "unknown"

        if true_CLID == "unknown" or pred_CLID == "unknown":
            return 1 if pred_cell_type == true_cell_type['manual_annotation'] or (true_broadtype == 'malignant cell' and pred_broadtype == 'malignant cell') else 0
        else:
            t1 = set(true_CLID.split(','))
            t2 = set(pred_CLID.split(','))
            s1 = len(t1.intersection(t2)) / len(t1.union(t2)) == 1 if len(t1.union(t2) - {"unknown", None}) > 0 else False
            s2 = pred_cell_type == true_cell_type['manual_annotation']
            s3 = true_broadtype == 'malignant cell' and pred_broadtype == 'malignant cell'

            return 1 if (s1 or s2 or s3) else 0

    true_broadtype = true_cell_type['manual_broadtype'] if true_cell_type['manual_broadtype'] is not pd.NA else "unknown"

    pred_CLID = standardize_and_match_CLID(pred_cell_type)
    pred_broadtype = get_broadtype(pred_CLID)

    part_score = compute_partscore(pred_broadtype, true_broadtype)
    full_score = compute_fullscore(pred_cell_type, true_cell_type, pred_broadtype, true_broadtype)

    return max(part_score, full_score)

if __name__ == "__main__":
    cl = pd.read_csv('data/GPTCellType/src/compiled.csv')
    hier = pd.read_csv('data/GPTCellType/src/relation.csv', header=None)

    dataset_path = "logs/cell_type_annotation/tabulasapiens/gpt-4o-mini-2024-07-18/20240908-033903/results/reverse_tabulasapiens_results.csv"
    dataset_with_model_anno = pd.read_csv(dataset_path)
    model = 'reverse_' + 'gpt-4o-mini-2024-07-18'
    dataset_with_agreement = eval_cell_type_annotation(model, dataset_with_model_anno, cl, hier)
    dataset_with_agreement.to_csv(dataset_path, index=False)
    print(dataset_path)
    print(dataset_with_agreement[model + '_agreement'].mean())

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
