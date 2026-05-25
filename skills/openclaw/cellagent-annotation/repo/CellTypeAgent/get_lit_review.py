# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

# src: BioDiscoveryAgent
import os
import time
import random
import requests
import urllib.parse
from pymed import PubMed
from utils import standardize_cell_type
from LLM import complete_text
import concurrent.futures

def understand_file(lines, things_to_look_for, model):

    blocks = ["".join(lines[i:i+2000]) for i in range(0, len(lines), 2000)]

    descriptions  = []
    for idx, b in enumerate(blocks):
        start_line_number = 2000*idx+1
        end_line_number = 2000*idx+1 + len(b.split("\n"))
        prompt = f"""Given this (partial) file from line {start_line_number} to line {end_line_number}:

```
{b}
```

Here is a detailed description on what to look for and what should returned: {things_to_look_for}

The description should short and also reference crtical sentences in the script relevant to what is being looked for. Only describe what is objectively confirmed by the file content. Do not include guessed numbers. If you cannot find the answer to certain parts of the request, you should say "In this segment, I cannot find ...".
"""
        completion = complete_text(prompt, model = model, log_file=None)
        descriptions.append(completion)
    if len(descriptions) == 1:
        return descriptions[0]
    else:
        descriptions = "\n\n".join(["Segment {idx}: \n\n" + s for s in descriptions])
        prompt = f"""Given the relevant observations for each segments of a file, summarize to get a cohesive description of the entire file on what to look for and what should returned: {things_to_look_for}

{descriptions}
"""

        completion = complete_text(prompt, model = model, log_file=None)

        return completion

def understand_LitSense_results(results, args, task_info, log_file=None):
    if args.task == "cell-type-annotation":
        if args.reasoning_mode == "selection":
            prompt = f"""
Here are scientific paper segments identified by their PMCIDs:
```
{results}
```

**Task**: Extract and summarize evidence supporting the relationship between the predicted cell type "{task_info['cell_type']}" and the marker genes "{task_info['marker_genes']}".

#### Instructions:
1. **Identify Relevant Evidence**: Find descriptions that discuss the expression or role of any of the marker genes (in "{task_info['marker_genes']}") in relation to the predicted cell type "{task_info['cell_type']}".
2. **Extract Key Points**: For each marker gene (in "{task_info['marker_genes']}"):
    - Extract concise evidence directly connecting it to the predicted cell type "{task_info['cell_type']}".
    - Include only direct evidence from the literature. Do not speculate or infer connections.
    - If evidence refers to a different cell type, omit it entirely.
    - Be brief, accurate, and stick strictly to the information provided in the literature.
    - If a gene is not mentioned in relation to the predicted cell type in the literature, do not include it as evidence.
    - Avoid any indirect speculation or forced connections.
3. **Cite Sources**: Provide PMCIDs for each piece of evidence. The evidence should be directly connecting the marker gene to the predicted cell type.
4. **Certainty Level**: Determine the certainty level based on the number of matched marker genes. Use the following criteria:
        - High: 7 or more matched genes
        - Medium: 4 to 6 matched genes
        - Low: 1 to 3 matched genes
        - No evidence: 0 matched genes
    Do not fabricate or estimate information; use only the evidence found in the literature.

#### Output Format:
- Predicted Cell Type: {task_info['cell_type']}
- Provided Marker Genes: {task_info['marker_genes']}
- Evidence Summary:
    - Evidence for Gene xxx: [Description of evidence, including the source content in quotation marks and then show your understanding of the evidence.] (Citation: PMCID X)
    - Evidence for Gene xxx: [Description of evidence, including the source content in quotation marks and then show your understanding of the evidence.] (Citation: PMCID Y, PMCID Z, ...)
    - ...
- Matched Marker Genes: [Based on the evidence, list the marker genes in "{task_info['marker_genes']}" that are showing strong correlation with the predicted cell type "{task_info['cell_type']}"]
- Number of Matched Marker Genes: [Return the number of matched marker genes in "**Matched Marker Genes**".]
- Certainty Level: [Return the certainty level as: High (Number of Matched Marker Genes >= 8) or Medium (Number of Matched Marker Genes >= 6 but < 8) or Low (Number of Matched Marker Genes >= 1 but < 6) or No-evidence (Number of Matched Marker Genes = 0)]
"""
        elif args.reasoning_mode == "reverse":
            prompt = f"""Here are a group of scientific paper segments identified by their pmcid:
```
{results}
```

Your task is to extract and summarize specific evidence supporting the relationship between the cell type "{task_info['cell_type']}" and the marker genes: "{task_info['marker_genes']}".

Instructions:
1. **Identify Relevant Evidence**: Look for descriptions in the paper segments that discuss the expression or role of any of the marker genes ("{task_info['marker_genes']}") in relation to the cell type "{task_info['cell_type']}".
2. **Extract Key Points**: For each marker gene in "{task_info['marker_genes']}", extract sentences or paragraphs that provide direct evidence, such as experimental results, data analysis, or expert opinions connecting the marker gene to the cell type "{task_info['cell_type']}" in the paper segments. If the evidence is about another cell type, please say so, do not forcefully link the unrelevant evidence to the predicted cell type. Be short and concise. If there's not enough information that can support the relationship between the marker gene and the cell type, please say so. If there's no evidence for a marker gene and the cell type relationship, it's okay to say so. Do not make up any information.
3. **Cite the Source**: Provide the source information like the pmcid for each extracted piece of evidence.
4. **Summarize the Findings**: Write a concise summary that integrates the evidence to explain how the marker genes support or confirm the identification of the cell type "{task_info['cell_type']}".

Output Format:
- **Predicted Cell Type**: {task_info['cell_type']}
- **Provided Marker Genes**: {task_info['marker_genes']}
- **Evidence Summary**:
    - *Evidence for Gene 1*: [Description of evidence, including the source content in quotation marks and then show your understanding of the evidence]. (Citation: pmcid 1, pmcid 2, ...)
    - *Evidence for Gene 2*: [Description of evidence, including the source content in quotation marks and then show your understanding of the evidence]. (Citation: pmcid ...)
    - ...
- **Integrated Summary**: [A comprehensive paragraph summarizing the evidence supporting the relationship between the cell type and the marker genes. Critically evaluate the strength and sufficiency of the evidence. If the evidence is insufficient or inconclusive, clearly state that it does not adequately support the prediction. Conclude by quantifying the number of marker genes that demonstrate strong positive correlation with the predicted cell type based solely on the literature review findings. Do not include speculative information or unsupported claims.]
"""
        elif args.reasoning_mode == "straightforward": # do not know cell type, search for papers based on marker genes to find cell type
            prompt = f"""Here are a group of scientific paper segments identified by their pmcid:
```
{results}
```

Your task is to extract and summarize relevant information from the paper segments that may help to identify the cell type with the marker genes: "{task_info['marker_genes']}".

Instructions:
1. **Identify Relevant Evidence**: Look for descriptions in the paper segments that discuss the expression or role of any of the marker genes ("{task_info['marker_genes']}") in relation to any cell type".
2. **Extract Key Points**: For each marker gene in "{task_info['marker_genes']}", extract sentences or paragraphs that provide direct evidence, such as experimental results, data analysis, or expert opinions connecting the marker gene to any cell type. If the information does not mention any cell type, please say so. Be short and concise. Do not make up any information.
3. **Cite the Source**: Provide the source information like the pmcid for each extracted piece of evidence.
4. **Summarize the Findings**: Write a concise summary that integrates the evidence to explain how the marker genes support or confirm the identification of any cell type.

Output Format:
- **Provided Marker Genes**: {task_info['marker_genes']}
- **Evidence Summary**:
    - *Evidence for Gene 1*: [Description of evidence, including the source content in quotation marks and then show your understanding of the evidence]. (Citation: pmcid 1, pmcid 2, ...)
    - *Evidence for Gene 2*: [Description of evidence, including the source content in quotation marks and then show your understanding of the evidence]. (Citation: pmcid ...)
    - ...
- **Potential Cell Type**: [Conclude the cell types that the above evidence supports]
    - *Potential Cell Type 1*: [The cell type that the evidence supports]. (Citation: pmcid 1, pmcid 2, ...)
        - [Summarize the matched marker genes in {task_info['marker_genes']} that support the cell type]
        - Number of matched marker genes: [Number of matched marker genes]
        - [Briefly explain why you think this cell type is supported by the evidence, cite the pmcid of the papers you used in the key evidence]
    - *Potential Cell Type 2*: [The cell type that the evidence supports]. (Citation: pmcid ...)
        - [Summarize the matched marker genes in {task_info['marker_genes']} that support the cell type]
        - Number of matched marker genes: [Number of matched marker genes]
        - [Briefly explain why you think this cell type is supported by the evidence, cite the pmcid of the papers you used in the key evidence]
    - ...
- **Integrated Summary**: [A comprehensive paragraph summarizing the evidence supporting the relationship between any cell type and marker genes. Critically evaluate the strength and sufficiency of the evidence. If the evidence is insufficient or inconclusive, clearly state that it does not adequately support the prediction. Conclude by quantifying the number of marker genes that demonstrate strong positive correlation with the typical cell type based solely on the literature review findings. Do not include speculative information or unsupported claims.]
"""

    completion = complete_text(prompt, model = args.model, log_file=log_file)
    return completion

def what_to_query(current_prompt, model, log_file_path, args, answer=None, query_used=None, extra_prompt=""):
    query_used_prompt = ""
    if query_used:
        query_used_prompt = """
# Attention:
- The following queries separated by comma have been used previously. Please avoid repeating them: """
        query_used_prompt += ", ".join(f"{q}" for q in query_used)

    base_prompt = f"""
You are an expert at literature review. Given the current state of the research problem and previous research:
"{current_prompt}"

Your task is to generate a concise, highly focused query to find relevant papers that would best advance the research problem.

"""

    guidelines = """
# Guidelines:
- Create a single-line query without Boolean operators (AND, OR, NOT)
- Use quotation marks sparingly and only for single, critical terms
- Limit to a maximum of two quoted terms per query
- Do not enclose the entire query in quotation marks
- Prioritize key concepts, cell types, genes, species, and tissue types directly related to the research problem

"""
    if args.reasoning_mode == "straightforward" and args.task == "cell-type-annotation":
        base_prompt += guidelines + f"""
# Hint for first query:
- Combine all marker genes, species (if provided), and tissue type (if provided) without quotation marks
- Example: LYZ C1QA C1QB AIF1 TYROBP FCER1G CD68 C1QC APOC1 LST1 human pbmc cell type
- Avoid quotation marks for individual terms in the first query to maximize search flexibility
- Subsequent queries can explore different combinations of these elements
"""
    elif args.reasoning_mode in "reverse" and args.task == "cell-type-annotation":
        base_prompt += guidelines + f"""
Meanwhile, you have predicted the answer to the research problem: "{answer}"

Your task is to generate a query that provides evidence supporting your predicted answer. Include the predicted answer, marker genes, species, and tissue type in the query if provided.

# Hint:
- Use double quotes only for the most important keyword, typically the predicted cell type name
- Avoid quotation marks for other terms
- Use at most one quotation mark group in the query
- Example: "xx cell" Camp Ngp S100a9 S100a8 Chil3 Ltf Wfdc21 Lcn2 Fcnb Pglyrp1 species tissue
"""
    elif args.reasoning_mode in "selection" and args.task == "cell-type-annotation":
        base_prompt += f"""
You have predicted the answer to the research problem: "{answer}"

Your task is to generate a query that provides evidence supporting your predicted answer. Include the predicted answer, marker genes, species, and tissue type in the query if provided.

# Hint:
- Use double quotes only for the most important keyword, i.e., the predicted cell type name
- Avoid quotation marks for other terms
- Use at most one quotation mark group in the query
- Example: "xx cell" Camp Ngp S100a9 S100a8 Chil3 Ltf Wfdc21 Lcn2 Fcnb Pglyrp1 species tissue
"""
    prompt = base_prompt + query_used_prompt + extra_prompt
    query = complete_text(prompt=prompt, model=model, log_file=log_file_path)
    return query.strip()

def query_LitSense(query, max_results, rerank=True):
    base_url = "https://www.ncbi.nlm.nih.gov/research/litsense-api/api/"

    query = query.strip(' .')

    params = {
        'query': query,
        'rerank': 'true' if rerank else 'false'
    }
    full_url = f"{base_url}?{urllib.parse.urlencode(params)}"
    response = requests.get(full_url)
    reviews = []

    if response.status_code == 200:
        reviews = response.json()
        if len(reviews) >= max_results:
            reviews = reviews[:max_results]
            num_papers_to_get = 0
        else:
            num_papers_to_get = max_results - len(reviews)
    else:
        num_papers_to_get = max_results
        print("Error: ", response.status_code)

    return reviews, num_papers_to_get, response.status_code

def thread_query_LitSense(args):
    return query_LitSense(*args)

def execute_queries(queries):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(thread_query_LitSense, args) for args in queries]
        all_reviews = []
        for future in concurrent.futures.as_completed(futures):
            reviews, _, _ = future.result()
            all_reviews.extend(reviews)
        return all_reviews

def generate_pair_queries(cell_type_candidate, marker_genes, max_literature_count=5):
    queries =[]
    for gene in marker_genes:
        queries.append((f'"{cell_type_candidate}" {gene}', max_literature_count))
    return queries

def format_lit_record(all_reviews):
    return "\n".join([
        f"pmcid: {paper.get('pmcid', '')}\n"
        f"section: {paper.get('section', '')}\n"
        f"content: {paper.get('text', '')}\n"
        f"{'-' * 70}"
        for paper in all_reviews if paper.get('pmcid') not in [None, 'None', '']
    ])

def get_LitSense_review(prompt, args, log_file_path, task_info=None):

    if args.task == "cell-type-annotation" and args.reasoning_mode == "selection":
        candidate = task_info["answer"]
        task_info["cell_type"] = standardize_cell_type(candidate)
        marker_genes = [gene.strip() for gene in task_info["marker_genes"].split(',')]
        queries = generate_pair_queries(candidate, marker_genes)
        all_reviews = execute_queries(queries)
        lit_record = format_lit_record(all_reviews)

        time.sleep(2)

        return str(understand_LitSense_results(lit_record, args, task_info, log_file_path))

    lit_review = ""
    papers, query_used = [], []
    count_query, max_queries = 0, 15
    num_papers_to_get = args.max_literature_count

    markers = ' '.join(m.strip() for m in task_info['marker_genes'].split(','))
    cell_type = standardize_cell_type(task_info.get('answer', '')) or ''
    species = task_info.get('species', '')
    tissue = task_info.get('tissue', '')

    if args.fast_lit_search:
        fast_queries = [
            f'"{cell_type}" {markers}',
            f'"{cell_type}" {markers} {species} {tissue}',
            f'"{cell_type}" {markers} {species}',
            f'"{cell_type}" {markers} {tissue}',
            f'{cell_type} {markers} {species} {tissue}',
        ]

        for fast_query in fast_queries:
            p, num_papers_to_get, status_code = query_LitSense(fast_query, num_papers_to_get)
            papers.extend(p)
            query_used.append(fast_query)
            count_query += 1
            if num_papers_to_get == 0 or count_query >= max_queries:
                break

    while num_papers_to_get > 0 and count_query < max_queries:
        query = what_to_query(prompt, args.model, log_file_path, args=args, answer=task_info['answer'], query_used=query_used)
        query_used.append(query)

        count_404 = 0
        extra_prompt = ""

        for _ in range(3):
            try:
                p, num_papers_to_get, status_code = query_LitSense(query, num_papers_to_get)
                papers.extend(p)
                count_query += 1

                if num_papers_to_get <= 0 or count_query >= max_queries:
                    break

                if status_code == 404:
                    count_404 += 1
                    if count_404 >= 7:
                        break

                    extra_instructions = {
                        2: "\n\n# Additional Instruction 1: Ignore the previous 'Hint'. Do not use any quotation marks in the query, including for cell type names. Avoid special characters.",
                        3: "\n\n# Additional Instruction 2: Exclude periods from the query. Omit marker genes containing periods.",
                        4: "\n\n# Additional Instruction 3: Simplify the query by including only 3-4 key terms or marker genes."
                    }

                    if count_404 in extra_instructions:
                        extra_prompt += extra_instructions[count_404]
                        query_used = None if count_404 == 3 else query_used

                    query = what_to_query(prompt, args.model, log_file_path, args=args, answer=task_info['answer'], query_used=query_used, extra_prompt=extra_prompt)

                    if count_404 < 3 and query not in query_used:
                        query_used.append(query)

                time.sleep(5)
            except:
                print("Rate limit reached. Waiting for 5 seconds")
                time.sleep(5)

        if papers or count_query >= max_queries:
            break

    if not papers:
        print("Cannot find any related papers.")
        return "No relevant papers found."

    lit_record = "\n".join([
        f"pmcid: {paper.get('pmcid', '')}\n"
        f"section: {paper.get('section', '')}\n"
        f"content: {paper.get('text', '')}\n"
        f"{'-' * 100}"
        for paper in papers
    ])

    if args.task == "cell-type-annotation" and args.reasoning_mode in ("reverse", "selection"):
        task_info["cell_type"] = standardize_cell_type(task_info["answer"])

    lit_review = understand_LitSense_results(lit_record, args, task_info)
    lit_record += f"\n\n{lit_review}\n\n"

    with open(log_file_path, "a", 1) as f:
        f.write(lit_record)

    return str(lit_review)

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
