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
Running the TrialGPT matching for three cohorts (sigir, TREC 2021, TREC 2022).
"""

import json
from nltk.tokenize import sent_tokenize
import os
import sys

from TrialGPT import trialgpt_matching 

if __name__ == "__main__":
	corpus = sys.argv[1]
	model = sys.argv[2] 
	
	dataset = json.load(open(f"dataset/{corpus}/retrieved_trials.json"))

	output_path = f"results/matching_results_{corpus}_{model}.json" 

	# Dict{Str(patient_id): Dict{Str(label): Dict{Str(trial_id): Str(output)}}}
	if os.path.exists(output_path):
		output = json.load(open(output_path))
	else:
		output = {}

	for instance in dataset:
		# Dict{'patient': Str(patient), '0': Str(NCTID), ...}
		patient_id = instance["patient_id"]
		patient = instance["patient"]
		sents = sent_tokenize(patient)
		sents.append("The patient will provide informed consent, and will comply with the trial protocol without any practical issues.")
		sents = [f"{idx}. {sent}" for idx, sent in enumerate(sents)]
		patient = "\n".join(sents)

		# initialize the patient id in the output 
		if patient_id not in output:
			output[patient_id] = {"0": {}, "1": {}, "2": {}}
		
		for label in ["2", "1", "0"]:
			if label not in instance: continue

			for trial in instance[label]: 
				trial_id = trial["NCTID"]

				# already calculated and cached
				if trial_id in output[patient_id][label]:
					continue
				
				# in case anything goes wrong (e.g., API calling errors)
				try:
					results = trialgpt_matching(trial, patient, model)
					output[patient_id][label][trial_id] = results

					with open(output_path, "w") as f:
						json.dump(output, f, indent=4)

				except Exception as e:
					print(e)
					continue

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
