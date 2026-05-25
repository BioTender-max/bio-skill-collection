# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

from dotenv import load_dotenv
from langchain_core.tools import tool
from serpapi import GoogleSearch    
import os
from squidpy_rag import squidpy_rag_agent
from textwrap import dedent
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import InjectedState
from typing import Annotated, Dict
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from datetime import datetime
import streamlit as st
import functools
import logging
import multiprocessing
import json
import re
import sys
from io import StringIO
from typing import Dict, Optional
from pydantic import BaseModel, Field
logger = logging.getLogger(__name__)
load_dotenv()

# Google Scholar Tool
class GoogleScholarAPI:
    def __init__(self, serp_api_key: str = None, top_k_results: int = 40, hl: str = "en", lr: str = "lang_en"):
        self.serp_api_key = serp_api_key or os.environ.get("SERP_API_KEY")
        self.top_k_results = top_k_results
        self.hl = hl
        self.lr = lr

    def run(self, query: str) -> str:
        if not self.serp_api_key:
            return "API key missing for Google Scholar search."
        params = {
            "engine": "google_scholar",
            "q": query,
            "api_key": self.serp_api_key,
            "hl": self.hl,
            "lr": self.lr,
            "num": min(self.top_k_results, 40),
        }
        search = GoogleSearch(params)
        results = search.get_dict().get("organic_results", [])
        if not results:
            return "No good Google Scholar Result was found."
        return "\n\n".join([
            f"Title: {result.get('title', '')}\n"
            f"Authors: {', '.join([a.get('name') for a in result.get('publication_info', {}).get('authors', [])])}\n"
            f"Summary: {result.get('snippet', '')}\n"
            f"Link: {result.get('link', '')}"
            for result in results
        ])

google_scholar = GoogleScholarAPI()


@tool
def google_scholar_search(query: str) -> str:
    """Searches Google Scholar for the provided query."""
    return google_scholar.run(query)


@tool
def visualize_cell_cell_interaction_tool() -> str:
    """
    Visualizes cell-cell interaction patterns from spatial transcriptomics data.
    
    This tool analyzes and visualizes how different cell types interact with each other
    in spatial proximity using neighborhood enrichment analysis. It:
    
    1. Loads preprocessed pancreas spatial transcriptomics data
    2. For each sample in the dataset:
        - Computes spatial neighbors between cells
        - Performs neighborhood enrichment analysis based on cell types
        - Creates a heatmap visualization showing interaction patterns
        
    The visualization shows:
    - Red colors indicate cell types that are more likely to be neighbors
    - Blue colors indicate cell types that tend to avoid each other
    - Color intensity represents the strength of attraction/avoidance
    
    No input parameters are required - the tool uses a default preprocessed dataset.
    
    Note: This code should be executed using the python_repl_tool.
    """
    code = f"""
    import squidpy as sq
    import anndata as ad
    import scanpy as sc
    import seaborn as sns
    data_path = './data/pancreas_processed_full.h5ad'
    adata = ad.read_h5ad(data_path)
    # Neighborhood enrichment analysis
    id = adata.obs['slice_name'].unique()
    result_cell_type_csv = 
    # set the NaN value to 0
    for sample_i in id:
        data_i = adata[adata.obs['slice_name']==sample_i]
        sq.gr.spatial_neighbors(data_i, coord_type="generic", spatial_key="spatial", delaunay=True)
        sq.gr.nhood_enrichment(data_i, cluster_key="cell_type")
        data_i.uns['cell_type_nhood_enrichment']['zscore'] = np.nan_to_num(data_i.uns['cell_type_nhood_enrichment']['zscore'])
        result_cell_type_csv[sample_i] = pd.DataFrame(data_i.uns['cell_type_nhood_enrichment']['zscore'], columns=data_i.obs['cell_type'].cat.categories, index=data_i.obs['cell_type'].cat.categories)

    week_4 = ['Week_4_slice_1', 'Week_4_slice_2']
    week_16 = ['Week_16_slice_1', 'Week_16_slice_2', 'Week_16_slice_3']
    week_20 = ['Week_20_slice_1', 'Week_20_slice_2', 'Week_20_slice_3', 'Week_20_slice_4']

    week_4_result = 
    for sample_i in week_4:
        week_4_result[sample_i] = result_cell_type_csv[sample_i]
    week_16_result = 
    for sample_i in week_16:
        week_16_result[sample_i] = result_cell_type_csv[sample_i]
    week_20_result = 
    for sample_i in week_20:
        week_20_result[sample_i] = result_cell_type_csv[sample_i]


    week_4_average = (week_4_result['(4, 1)'] + week_4_result['(4, 29)'])/2
    week_16_average = (week_16_result['(16, 185)'] + week_16_result['(16, 215)'] + week_16_result['(16, 242)'])/3
    week_20_average = (week_20_result['(20, 1)'] + week_20_result['(20, 46)'] + week_20_result['(20, 70)'] + week_20_result['(20, 160)'])/4

    enrichment_dict = 
        'week_4': week_4_average,
        'week_16': week_16_average,
        'week_20': week_20_average
    

    input_list = ['human_alpha',
                'human_beta', 
                'human_delta',
                'human_enterochromaffin',
                'human_exocrine',
                'human_mesenchymal',
                'mouse_nephron',
                'mouse_ureteric_epithelium', 
                'mouse_vascular']
    
    for sample_i in enrichment_dict.keys():
        a = enrichment_dict[sample_i].reindex(index=input_list, columns=input_list)
        ax = sns.heatmap(a, vmax=30, vmin=-30, cmap='RdBu_r', annot=True, fmt=".1f")		
        ax.set_title('cell_type neighborhood enrichment of {{}}'.format(sample_i))
        plt.show()

    # Please use python_repl_tool to execute the above code directly. IMPORTANT: PLEASE DON'T CHANGE THE CODE.
    <<<REPEAT: PLEASE DON'T CHANGE THE CODE. AND YOU SHOULD USE THE `python_repl_tool` TO EXECUTE THE CODE. However, you can fix the bug>>>
    """
    return dedent(code)


@tool
def visualize_spatial_cell_type_map() -> str:
    """
    Visualizes spatial distribution of cell types across different slices.
    
    This tool creates spatial scatter plots showing the location and identity
    of different cell types in the tissue space. It:
    
    1. Loads preprocessed pancreas spatial transcriptomics data
    2. For each slice (Week_4_slice_1, Week_4_slice_2, Week_16_slice_1, etc.):
        - Creates a spatial plot where each point represents a cell
        - Colors points based on cell type identity
        - Displays the spatial organization of different cell populations
        
    The visualization shows:
    - Each dot represents a single cell
    - Colors indicate different cell types
    - Spatial coordinates preserve the original tissue structure
    - Separate plots for each slice for detailed spatial comparison
    
    No input parameters are required - the tool uses a default preprocessed dataset.
    
    Note: This code should be executed using the python_repl_tool.
    """

    code = f"""
        import scanpy as sc
        import squidpy as sq
        import anndata as ad
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import os
        # Load data
        data_path = './data/pancreas_processed_full.h5ad'
        adata = ad.read_h5ad(data_path)
        # Define color dictionary for cell types
        cell_type_color_dict = 
            'human_enterochromaffin': '#fdbf6e',
            'human_alpha': '#34a048',
            'human_beta': '#f69999', 
            'human_delta': '#e21f26',
            'human_exocrine': '#2078b4',
            'human_mesenchymal': '#b4d88a',
            'mouse_vascular': '#f57f20',
            'mouse_nephron': '#6b3e98',
            'mouse_ureteric_epithelium': '#fbf49c'
        
        # Get slice names
        slice_names = sorted(adata.obs['slice_name'].unique().tolist())
        # Plot spatial distribution for each slice
        for slice_id in slice_names:
            adata_slice = adata[adata.obs['slice_name'] == slice_id].copy()
            fig, ax = plt.subplots(figsize=(10, 8))
            # Get unique cell types in this slice
            cell_types_in_slice = adata_slice.obs['cell_type'].unique()
            # Plot each cell type with its color
            for cell_type in cell_types_in_slice:
                cells = adata_slice[adata_slice.obs['cell_type'] == cell_type]
                ax.scatter(
                    cells.obsm['spatial'][:, 0],
                    cells.obsm['spatial'][:, 1],
                    c=cell_type_color_dict[cell_type],
                    label=cell_type,
                    s=20,
                    alpha=0.8
                )
            ax.set_title(f'Spatial Cell Type Distribution - {{slice_id}}')
            ax.set_xlabel('Spatial X')
            ax.set_ylabel('Spatial Y')
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.show()
    # Please use python_repl_tool to execute this code directly. IMPORTANT: PLEASE DON'T CHANGE THE CODE.
    <<<REPEAT: PLEASE DON'T CHANGE THE CODE. AND YOU SHOULD USE THE `python_repl_tool` TO EXECUTE THE CODE. But you can fix the bugs>>>
    """
    return dedent(code)


@tool
def visualize_cell_type_composition() -> str:
    """
    Visualizes cell type composition changes across different time points.
    
    This tool creates both stacked bar plots and heatmaps to show how cell type
    proportions change over time. It:
    
    1. Loads preprocessed pancreas spatial transcriptomics data
    2. Calculates cell type proportions for each sample
    3. Creates two complementary visualizations:
        - Stacked bar plot showing relative proportions
        - Heatmap showing exact percentage values
        
    The visualizations show:
    - Relative abundance of each cell type per sample
    - Changes in cell type composition across time points
    - Exact percentage values for each cell type
    
    No input parameters are required - the tool uses a default preprocessed dataset.
    
    Note: This code should be executed using the python_repl_tool.
    """
    code = f"""
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    import squidpy as sq
    import anndata as ad
    import scanpy as sc
    # Load the data
    data_path = './data/pancreas_processed_full.h5ad'
    adata = ad.read_h5ad(data_path)
    # Calculate cell type composition for each sample
    composition_df = pd.crosstab(
    adata.obs['sample_name'], 
    adata.obs['cell_type'], 
    normalize='index'  # This gives proportions instead of raw counts
    ) * 100  # Convert to percentages

    plt.figure(figsize=(12, 6))
    composition_df.plot(kind='bar', stacked=True)
    plt.title('Cell Type Composition Across Samples')
    plt.xlabel('Sample')
    plt.ylabel('Percentage of Cells')
    plt.legend(title='Cell Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()


    print("Cell type composition (%):")
    print(composition_df.round(2))
    plt.figure(figsize=(10, 6))
    sns.heatmap(composition_df, annot=True, fmt='.1f', cmap='YlOrRd')
    plt.title('Human Cell Type Composition Heatmap')
    plt.ylabel('Sample')
    plt.xlabel('Cell Type')
    plt.tight_layout()
    plt.show()
    
    # Please use python_repl_tool to execute this code directly. IMPORTANT: PLEASE DON'T CHANGE THE CODE.
    <<<REPEAT: PLEASE DON'T CHANGE THE CODE. AND YOU SHOULD USE THE `python_repl_tool` TO EXECUTE THE CODE.>>>
    <<<DO NOT CHANGE ANY OF THE CODE FROM THE OUTPUT OF THE `visualize_cell_type_composition`>>>
    """
    return dedent(code)


@tool
def visualize_umap() -> str:
    """
    Visualizes UMAP plots for cell types across different time points.
    
    This tool creates UMAP visualizations code showing the distribution of cell types
    in reduced dimensional space. It:
    
    1. Loads preprocessed pancreas spatial transcriptomics data
    2. For each sample (Week 4, Week 16, Week 20):
        - Creates a UMAP plot where each point represents a cell
        - Colors points based on cell type identity
        - Shows cell type clustering patterns
        
    The visualization shows:
    - Each dot represents a single cell
    - Colors indicate different cell types
    - Clustering patterns reveal relationships between cell types
    - Separate plots for each time point for temporal comparison
    
    No input parameters are required - the tool uses a default preprocessed dataset.
    
    Note: This code should be executed using the python_repl_tool.
    """
    code = f"""
    import squidpy as sq
    import anndata as ad
    import scanpy as sc

    # Load the data
    data_path = './data/pancreas_processed_full.h5ad'
    adata = ad.read_h5ad(data_path)

    cell_type_color_dict =  
        'human_enterochromaffin': '#fdbf6e',
        'human_alpha': '#34a048',
        'human_beta': '#f69999',
        'human_delta': '#e21f26',
        'human_exocrine': '#2078b4',
        'human_mesenchymal': '#b4d88a',
        'mouse_vascular': '#f57f20',
        'mouse_nephron': '#6b3e98',
        'mouse_ureteric_epithelium': '#fbf49c'
    
    # Plot the UMAP for the whole smaple     
    sc.pl.umap(
        adata,
        color='cell_type',  # Replace with your cell type annotation key
        title=f'umap for all samples',
        legend_loc='on data',
        legend_fontsize="small",
        legend_fontoutline=2, 
        palette=cell_type_color_dict
    )
    # Iterate over each sample in the AnnData object
    for sample_id in ['Week_4', 'Week_16', 'Week_20']:
        # Subset the AnnData object for the current sample
        adata_sample = adata[adata.obs['sample_name'] == sample_id]
        # Plot umap for the specific sample
        sc.pl.umap(
            adata_sample,
            color='cell_type',  # Replace with your cell type annotation key
            title=f'umap for sample {{sample_id}}',
            legend_loc='on data',
            legend_fontsize="small",
            legend_fontoutline=2, 
            palette=cell_type_color_dict
        )
    # Please use python_repl_tool to execute this code directly. IMPORTANT: PLEASE DON'T CHANGE THE CODE.
    <<<REPEAT: PLEASE DON'T CHANGE THE CODE. AND YOU SHOULD USE THE `python_repl_tool` TO EXECUTE THE CODE. But you can fix the bugs>>>
    """
    return dedent(code)


@tool
def report_tool(state: Annotated[Dict, InjectedState], query: str) -> str:
    """Generates a comprehensive scientific report based on the conversation history.
    
    This tool takes the entire conversation history and generates a well-structured scientific report
    in academic paper format, covering the analysis performed and insights gathered from the spatial
    transcriptomics data. The report includes sections like Abstract, Introduction, Methods, Results,
    Discussion, Conclusion, and References.
    
    The tool saves the report as a PDF file.
    
    Args:
        state: The current conversation state containing message history
        query: Additional context or specific requirements for the report (optional)
        
    Returns:
        str: Confirmation message with the path to the saved PDF file
    """

    # Extract the chat history from the injected state
    chat_history = state["messages"]



    report_prompt = """
    # Scientific Analysis Report

    <objective>
    Generate a comprehensive scientific report (minimum 1000 words) based on the conversation history above. The report should be specific and avoid general statements. All analysis should be based on data presented in the conversation.
    </objective>

    <report_structure>
    ## 1. Objective
    - Clear statement of the research goals
    - Overview of what the report aims to address

    ## 2. Study Overview
    - Background on the research topic
    - Purpose of the study
    - Key research questions being investigated

    ## 3. Methods Summary
    - Description of analysis techniques employed
    - Outline of data processing approaches used

    ## 4. Key Findings
    - Detailed results from each visualization/analysis in the conversation
    - Specific observations with quantitative data where available
    - Identification of significant patterns or trends

    ## 5. Biological Implications
    - Interpretation of the biological significance of findings
    - Integration with existing literature (include inline citations)
    - Discussion of broader impacts and relevance

    ## 6. Conclusion
    - Summary of major discoveries
    - Future research directions
    - Potential applications

    ## 7. References
    - Relevant citations from literature searches
    - Format: Title only (NO author names or years or URL)
    </report_structure>

    <important_instructions>
    1. OUTPUT ONLY THE REPORT CONTENT, NO OTHER TEXT
    2. Use specific data-driven insights rather than general statements
    3. Maintain scientific tone throughout
    4. Include inline citations where appropriate
    5. Do not assume conclusions not supported by the data
    6. Be consistent with the user's input language. you are a multi-lingual assistant.
    FORMAT: THE REPORT SHOULD BE IN MARKDOWN FORMAT.
    </important_instructions>
    """
    
    # Generate the report
    ins = chat_history[:-1] + [HumanMessage(content=report_prompt, name="report_tool")]
    st.write(ins)
    llm = ChatAnthropic(model="claude-3-7-sonnet-20250219",max_tokens=8000)
    report = llm.invoke(ins)
    try:
        # Save as markdown file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs('output_report', exist_ok=True)
        md_filename = f'./output_report/spatial_transcriptomics_report_{timestamp}.md'
        
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write(report.content)
        return f"Report has been saved as markdown file: {md_filename}"
        
    except Exception as e:
        return f"Error saving markdown file: {str(e)}"

@functools.lru_cache(maxsize=None)
def warn_once() -> None:
    """Warn once about the dangers of PythonREPL."""
    logger.warning("Python REPL can execute arbitrary code. Use with caution.")


class PythonREPL(BaseModel):
    """Simulates a standalone Python REPL."""

    globals: Optional[Dict] = Field(default_factory=dict, alias="_globals")  # type: ignore[arg-type]
    locals: Optional[Dict] = None  # type: ignore[arg-type]

    @staticmethod
    def sanitize_input(query: str) -> str:
        """Sanitize input to the python REPL.

        Remove whitespace, backtick & python
        (if llm mistakes python console as terminal)

        Args:
            query: The query to sanitize

        Returns:
            str: The sanitized query
        """
        query = re.sub(r"^(\s|`)*(?i:python)?\s*", "", query)
        query = re.sub(r"(\s|`)*$", "", query)
        return query

    @classmethod
    def worker(
        cls,
        command: str,
        globals: Optional[Dict],
        locals: Optional[Dict],
        queue: multiprocessing.Queue,
    ) -> None:
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            cleaned_command = cls.sanitize_input(command)
            exec(cleaned_command, globals, locals)
            sys.stdout = old_stdout
            queue.put(mystdout.getvalue())
        except Exception as e:
            sys.stdout = old_stdout
            queue.put(repr(e))

    def run(self, command: str, timeout: Optional[int] = None) -> str:
        """Run command with own globals/locals and returns anything printed.
        Timeout after the specified number of seconds."""

        # Warn against dangers of PythonREPL
        warn_once()

        queue: multiprocessing.Queue = multiprocessing.Queue()

        # Only use multiprocessing if we are enforcing a timeout
        if timeout is not None:
            # create a Process
            p = multiprocessing.Process(
                target=self.worker, args=(command, self.globals, self.locals, queue)
            )

            # start it
            p.start()

            # wait for the process to finish or kill it after timeout seconds
            p.join(timeout)

            if p.is_alive():
                p.terminate()
                return "Execution timed out"
        else:
            self.worker(command, self.globals, self.locals, queue)
        # get the result from the worker function
        return queue.get()


__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
