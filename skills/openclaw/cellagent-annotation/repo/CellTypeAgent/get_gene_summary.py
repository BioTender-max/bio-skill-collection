# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import requests
import xml.etree.ElementTree as ET
import time

def get_gene_id(gene_name, species="human"):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    esearch_url = f"{base_url}esearch.fcgi?db=gene&term={gene_name}[Gene Name]+AND+{species}[Organism]&retmode=xml"

    response = requests.get(esearch_url)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        id_element = root.find(".//Id")

        if id_element is not None:
            return id_element.text
        else:
            return None
    else:
        print(f"Error fetching gene ID for {gene_name}. Status code: {response.status_code}")
        return None

def get_gene_summary(gene_id):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    efetch_url = f"{base_url}efetch.fcgi?db=gene&id={gene_id}&retmode=xml"

    response = requests.get(efetch_url)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        summary = root.find(".//Entrezgene_summary")

        if summary is not None:
            return summary.text
        else:
            return "Summary not found"
    else:
        return f"Error: Unable to fetch data. Status code: {response.status_code}"

def get_summaries_for_genes(gene_list):
    result = "Here go the summaries of Genes from the NCBI Gene database for your reference:\n"
    for gene in gene_list:
        gene_id = get_gene_id(gene)
        if gene_id:
            summary = get_gene_summary(gene_id)
            result += f"- {gene}: {summary}\n"
        else:
            result += f"- {gene}: Gene ID not found\n"
        time.sleep(0.34)  # To respect NCBI's limit of 3 requests per second
    return result

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
