# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

__author__ = "qiao"

"""
Using GPT to aggregate the scores by itself.
"""

from beir.datasets.data_loader import GenericDataLoader
import json
from nltk.tokenize import sent_tokenize
import os
import sys
import time

from TrialGPT import trialgpt_aggregation

if __name__ == "__main__":
	corpus = sys.argv[1] 
	model = sys.argv[2]

	# the path of the matching results
	matching_results_path = sys.argv[3]
	results = json.load(open(matching_results_path))

	# loading the trial2info dict
	trial2info = json.load(open("dataset/trial_info.json"))
	
	# loading the patient info
	_, queries, _ = GenericDataLoader(data_folder=f"dataset/{corpus}/").load(split="test")
	
	# output file path
	output_path = f"results/aggregation_results_{corpus}_{model}.json"

	if os.path.exists(output_path):
		output = json.load(open(output_path))
	else:
		output = {}

	# patient-level
	for patient_id, info in results.items():
		# get the patient note
		patient = queries[patient_id]
		sents = sent_tokenize(patient)
		sents.append("The patient will provide informed consent, and will comply with the trial protocol without any practical issues.")
		sents = [f"{idx}. {sent}" for idx, sent in enumerate(sents)]
		patient = "\n".join(sents)

		if patient_id not in output:
			output[patient_id] = {}
		
		# label-level, 3 label / patient
		for label, trials in info.items():
				
			# trial-level
			for trial_id, trial_results in trials.items():
				# already cached results
				if trial_id in output[patient_id]:
					continue

				if type(trial_results) is not dict:
					output[patient_id][trial_id] = "matching result error"

					with open(output_path, "w") as f:
						json.dump(output, f, indent=4)

					continue

				# specific trial information
				trial_info = trial2info[trial_id]	

				try:
					result = trialgpt_aggregation(patient, trial_results, trial_info, model)
					output[patient_id][trial_id] = result 

					with open(output_path, "w") as f:
						json.dump(output, f, indent=4)

				except:
					continue

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
