# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

""" This file contains the code for calling all LLM APIs. Ref: https://github.com/snap-stanford/BioDiscoveryAgent/blob/master/LLM.py"""
import sys
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

try:
    import anthropic
    # Please setup your Anthropic API key
    anthropic_client = anthropic.Client(api_key=open("CellTypeAgent/APIs/claude_api_key.txt").read().strip())
except Exception as e:
    print(e)
    print("Could not load anthropic API key APIs/claude_api_key.txt.")

try:
    import openai
    from openai import OpenAI
    import yaml
    # Please setup your OpenAI API key
    try:
        client = OpenAI(
            api_key = open("CellTypeAgent/APIs/openai_api_key (myself).txt").read().strip(),
            timeout=60*10, # o1-preview need a long time to respond
        )
    except FileNotFoundError:
        print("Error: OpenAI API key file not found at CellTypeAgent/APIs/openai_key.txt")
        print("Please create the file and add your OpenAI API key")
        sys.exit(1)
except Exception as e:
    print(e)
    print("Could not initialize OpenAI client.")

try:
    import openai
    import yaml
    # Please setup your DeepSeek API key
    key = yaml.safe_load(open("CellTypeAgent/APIs/deepseek_api_key.yaml").read())
    client = OpenAI(
        base_url = key["base_url"],
        api_key = key["api_key"]
    )
except Exception as e:
    print(e)
    print("Could not load deepseek API key in APIs/deepseek_api_key.yaml.")


class TooLongPromptError(Exception):
    """Exception raised for errors in the prompt length."""
    def __init__(self, message="The prompt is too long."):
        self.message = message
        super().__init__(self.message)

class LLMError(Exception):
    """Exception raised for errors related to the LLM."""
    def __init__(self, message="An error occurred with the LLM."):
        self.message = message
        super().__init__(self.message)


def log_to_file(log_file, prompt, completion, model):
    """ Log the prompt and completion to a file."""
    with open(log_file, "a") as f:
        f.write("\n===================prompt=====================\n")
        f.write(f"{anthropic.HUMAN_PROMPT} {prompt} {anthropic.AI_PROMPT}")
        num_prompt_tokens = len(enc.encode(f"{anthropic.HUMAN_PROMPT} {prompt} {anthropic.AI_PROMPT}"))
        f.write(f"\n==================={model} response =====================\n")
        f.write(completion)
        num_sample_tokens = len(enc.encode(completion))
        f.write("\n===================tokens=====================\n")
        f.write(f"Number of prompt tokens: {num_prompt_tokens}\n")
        f.write(f"Number of sampled tokens: {num_sample_tokens}\n")
        f.write("\n\n")


def complete_text_claude(prompt, stop_sequences=[anthropic.HUMAN_PROMPT], model="claude-3.5-sonnet", max_tokens_to_sample = 2000, temperature=0.5, log_file=None, **kwargs):
    """ Call the Claude API to complete a prompt."""

    try:
        message = anthropic_client.messages.create(
            model=model,
            max_tokens=max_tokens_to_sample,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
            stop_sequences=stop_sequences,
            **kwargs
        )
    except anthropic.APIStatusError as e:
        print(e)
        sys.exit()
        raise TooLongPromptError()
    except Exception as e:
        raise LLMError(str(e))

    completion = message.content[0].text
    if log_file is not None:
        log_to_file(log_file, prompt, completion, model)
    return completion

def complete_text_openai(prompt, model="gpt-4o-mini-2024-07-18", temperature=0.5, log_file=None, **kwargs):

    if model.startswith("o1"):
        temperature = 1.0 # o1 models only support temperature 1.0

    """ Call the OpenAI API to complete a prompt."""
    raw_request = {
        "model": model,
        "temperature": temperature,
        # "max_tokens": max_tokens_to_sample,
        **kwargs
    }

    if model.startswith("gpt-3.5") or model.startswith("gpt-4") or model.startswith("o1") or model.startswith("o3"):
        messages = [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(**{"messages": messages,**raw_request})
        completion = response.choices[0].message.content
    else:
        response = client.chat.completions.create(model, **{"prompt": prompt,**raw_request})
        completion = response.choices[0].text
    if log_file is not None:
        log_to_file(log_file, prompt, completion, model)
    return completion

def complete_text_deepseek(prompt, model="deepseek-r1", temperature=0.5, log_file=None, stream=False, **kwargs):
    """ Call the DeepSeek API to complete a prompt."""
    max_attempts = 10
    for attempt in range(max_attempts):
        response = client.chat.completions.create(model=f"deepseek-ai/{model}", messages=[{"role": "user", "content": prompt}], temperature=temperature, stream=stream, **kwargs)
        try:
            completion = response.choices[0].message.content
            if log_file is not None:
                log_to_file(log_file, prompt, completion, model)
            return completion
        except Exception as e:
            print(e)
            print(f"Attempt {attempt+1} failed. Retrying...")
    raise LLMError("Failed to complete the prompt.")

def complete_text(prompt, log_file, model, **kwargs):
    """ Complete text using the specified model with appropriate API. """

    if model.startswith("claude"):
        completion = complete_text_claude(prompt, stop_sequences=[anthropic.HUMAN_PROMPT, "Observation:"], log_file=log_file, model=model, **kwargs)
    elif model.startswith("gpt") or model.startswith("o1") or model.startswith("o3"):
        completion = complete_text_openai(prompt, log_file=log_file, model=model, **kwargs)
    elif model.startswith("deepseek"):
        completion = complete_text_deepseek(prompt, log_file=log_file, model=model, **kwargs)
        print(completion)
    return completion

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
