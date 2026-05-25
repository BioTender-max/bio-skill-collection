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
TrialGPT-Ranking main functions.
"""

import json
from nltk.tokenize import sent_tokenize
import time
import os

from openai import AzureOpenAI

client = AzureOpenAI(
	api_version="2023-09-01-preview",
	azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
	api_key=os.getenv("OPENAI_API_KEY"),
)

def convert_criteria_pred_to_string(
		prediction: dict,
		trial_info: dict,
) -> str:
	"""Given the TrialGPT prediction, output the linear string of the criteria."""
	output = ""

	for inc_exc in ["inclusion", "exclusion"]:

		# first get the idx2criterion dict
		idx2criterion = {}
		criteria = trial_info[inc_exc + "_criteria"].split("\n\n")
		
		idx = 0
		for criterion in criteria:
			criterion = criterion.strip()

			if "inclusion criteria" in criterion.lower() or "exclusion criteria" in criterion.lower():
				continue

			if len(criterion) < 5:
				continue
		
			idx2criterion[str(idx)] = criterion
			idx += 1

		for idx, info in enumerate(prediction[inc_exc].items()):
			criterion_idx, preds = info

			if criterion_idx not in idx2criterion:
				continue

			criterion = idx2criterion[criterion_idx]

			if len(preds) != 3:
				continue

			output += f"{inc_exc} criterion {idx}: {criterion}\n"
			output += f"\tPatient relevance: {preds[0]}\n"
			if len(preds[1]) > 0:
				output += f"\tEvident sentences: {preds[1]}\n"
			output += f"\tPatient eligibility: {preds[2]}\n"
	
	return output


def convert_pred_to_prompt(
		patient: str,
		pred: dict,
		trial_info: dict,
) -> str:
	"""Convert the prediction to a prompt string."""
	# get the trial string
	trial = f"Title: {trial_info['brief_title']}\n"
	trial += f"Target conditions: {', '.join(trial_info['diseases_list'])}\n"
	trial += f"Summary: {trial_info['brief_summary']}"

	# then get the prediction strings
	pred = convert_criteria_pred_to_string(pred, trial_info)

	# construct the prompt
	prompt = "You are a helpful assistant for clinical trial recruitment. You will be given a patient note, a clinical trial, and the patient eligibility predictions for each criterion.\n"
	prompt += "Your task is to output two scores, a relevance score (R) and an eligibility score (E), between the patient and the clinical trial.\n"
	prompt += "First explain the consideration for determining patient-trial relevance. Predict the relevance score R (0~100), which represents the overall relevance between the patient and the clinical trial. R=0 denotes the patient is totally irrelevant to the clinical trial, and R=100 denotes the patient is exactly relevant to the clinical trial.\n"
	prompt += "Then explain the consideration for determining patient-trial eligibility. Predict the eligibility score E (-R~R), which represents the patient's eligibility to the clinical trial. Note that -R <= E <= R (the absolute value of eligibility cannot be higher than the relevance), where E=-R denotes that the patient is ineligible (not included by any inclusion criteria, or excluded by all exclusion criteria), E=R denotes that the patient is eligible (included by all inclusion criteria, and not excluded by any exclusion criteria), E=0 denotes the patient is neutral (i.e., no relevant information for all inclusion and exclusion criteria).\n"
	prompt += 'Please output a JSON dict formatted as Dict{"relevance_explanation": Str, "relevance_score_R": Float, "eligibility_explanation": Str, "eligibility_score_E": Float}.'


	user_prompt = "Here is the patient note:\n"
	user_prompt += patient + "\n\n"
	user_prompt += "Here is the clinical trial description:\n"
	user_prompt += trial + "\n\n"
	user_prompt += "Here are the criterion-level eligibility prediction:\n"
	user_prompt += pred + "\n\n"
	user_prompt += "Plain JSON output:"

	return prompt, user_prompt


def trialgpt_aggregation(patient: str, trial_results: dict, trial_info: dict, model: str):
	system_prompt, user_prompt = convert_pred_to_prompt(
			patient,
			trial_results,
			trial_info
	)   

	messages = [
		{"role": "system", "content": system_prompt},
		{"role": "user", "content": user_prompt}
	]

	response = client.chat.completions.create(
		model=model,
		messages=messages,
		temperature=0,
	)
	result = response.choices[0].message.content.strip()
	result = result.strip("`").strip("json")
	result = json.loads(result)

	return result

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
