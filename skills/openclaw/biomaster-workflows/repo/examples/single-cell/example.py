# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

from agents.Biomaster import Biomaster
from langchain_core.messages import HumanMessage
import json
# Example of using the agent
if __name__ == "__main__":

    config = {"configurable": {"thread_id": "abc124"}}
    api_key = ''
    base_url = ''
    # you can choose other base url
    manager = Biomaster(api_key, base_url,excutor=True,id='001')
    
    # example data you can find the google drive link in the README.md,which is in the WGS/WES example data folder.
    # you can also download the data from the link below
    # cd data
    # git clone https://github.com/STAR-Fusion/STAR-Fusion-Tutorial.git
    # mv STAR-Fusion-Tutorial/*
    datalist=[ './data/rnaseq_1.fastq.gz: RNA-Seq read 1 data (left read)',
            './data/rnaseq_2.fastq.gz: RNA-Seq read 2 data (right read)',
            './data/minigenome.fa: small genome sequence consisting of ~750 genes.',]
    goal='please do WGS/WES data analysis Somatic SNV+indel calling.'
    manager.execute_PLAN(goal,datalist)
    print("**********************************************************")

    PLAN_results_dict = manager.execute_TASK(datalist)
    print(PLAN_results_dict)



__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
