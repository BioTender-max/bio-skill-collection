# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import os
# os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   # see issue #152
# os.environ["CUDA_VISIBLE_DEVICES"]= '0,1,2,3'

from datasets import load_dataset
import torch
from tokenizers import Tokenizer
import pandas as pd
import numpy as np

from transformers import TrainerCallback, TrainingArguments, Trainer


# Downloaded GitHub Repo from https://github.com/salesforce/progen/tree/main/progen2
# The README also contains download links for the models

from progen.progen2.models.progen.modeling_progen import ProGenForCausalLM

if torch.cuda.is_available():
    device = torch.device('cuda:1') # # gather device

# ProGen2 pretrained on medium with 764M parameters
model = ProGenForCausalLM.from_pretrained('./models/progen2-base', torch_dtype=torch.float32).to(device)

from transformers import PreTrainedTokenizerFast

# Loading in tokenizer for ProGen2
def create_tokenizer_custom(file):
    with open(file, 'r') as f:
        return Tokenizer.from_str(f.read())

tokenizer = create_tokenizer_custom(file='./progen/progen2/tokenizer.json')

tokenizer.save("progen_custom_tokenizer.json")
tokenizer = PreTrainedTokenizerFast(tokenizer_file="progen_custom_tokenizer.json") #, return_tensors='pt')

# Define new special tokens
new_special_tokens = ['[LC]', '[SEP]']

tokenizer.vocab.pop('2', None)
tokenizer.vocab.pop('1', None)

# Add special tokens to the tokenizer
tokenizer.add_special_tokens({'additional_special_tokens': new_special_tokens})

# Manually adding these in to be sure
tokenizer.pad_token = '<|pad|>'
tokenizer.eos_token = '<|eos|>'


print('Tokenizer vocab size: ' + str(tokenizer.vocab_size))

input_seqs = pd.read_csv('./final_inputs_full-model_v2_24-03-12.csv', index_col=0)


# Using 1 and seperator and 2 as unknown AA (replacing X)
input_seqs['SEQ'] =  input_seqs['antigen_seq'] + '[SEP]' + input_seqs['VH_abnum'] + '[LC]' + input_seqs['VL_abnum']
# input_seqs['SEQ'] = input_seqs['SEQ'].apply(lambda x: x.replace('X', '1'))
input_seqs = input_seqs[~input_seqs['SEQ'].isna()]
input_seqs['SEQ'].apply(len).max()
print(input_seqs.shape)

from sklearn.model_selection import train_test_split
from datasets import Dataset

# Functions for tokenization and creation of datasets
def tokenize_sequences(sequences, tokenizer, max_length=None):
    tokenized_sequences = []
    for sequence in sequences:
        # Tokenize with padding, truncation, and ensure that labels are properly formatted
        tokens = tokenizer(sequence, add_special_tokens=True, truncation=True, padding="max_length", max_length=max_length)
        tokens['labels'] = tokens['input_ids'].copy()
        tokenized_sequences.append(tokens)
    return tokenized_sequences

def create_dataset(sequences, tokenizer, test_frac, val_frac, max_length):
    tokenized_sequences = tokenize_sequences(sequences, tokenizer, max_length=max_length)

    # Split the data into test and train
    train_data, test_data = train_test_split(tokenized_sequences, test_size=test_frac, random_state=42)

    # Convert to HuggingFace Dataset format
    train_dataset = Dataset.from_dict({k: [dic[k] for dic in train_data] for k in train_data[0]})
    test_dataset = Dataset.from_dict({k: [dic[k] for dic in test_data] for k in test_data[0]})    

    return train_dataset, test_dataset #, val_dataset


# Input array or list of sequences (here, I am calling the column from the DF with the sequences)
train_dataset, test_dataset = create_dataset(input_seqs['SEQ'], tokenizer, val_frac = 0.1, test_frac = 0.1, max_length=1024) #, val_dataset

print('Train size: ' + str(len(train_dataset)))
print('Test size: ' + str(len(test_dataset)))

np.save('test_data_full_model_v2_24-03-12', test_dataset)

import logging
from transformers import logging as hf_logging,TrainerCallback

# Configure HuggingFace logging
hf_logging.set_verbosity_info()

# Create a logger
logger = hf_logging.get_logger()

# Set up a file handler
file_handler = logging.FileHandler('training_metrics.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

from sklearn.metrics import accuracy_score
from transformers import TrainerCallback, TrainingArguments, Trainer
from transformers import EvalPrediction
import logging


class MetricsLoggingCallback(TrainerCallback):
    def on_epoch_end(self, args, state, control, **kwargs):
        # Log metrics at the end of each epoch
        if state.is_local_process_zero:
            logger.info(f"Epoch: {state.epoch}, Training Loss: {state.global_step}, {state.log_history[-1]}")


from transformers import Trainer, TrainingArguments
import torch
import torch.nn.functional as F


def cross_entropy(logits, target, reduction='mean'):
    return torch.nn.functional.cross_entropy(input=logits, target=target, weight=None, size_average=None, reduce=None, reduction=reduction)


class CustomNLLEntropyLossTrainer(Trainer):
    def __init__(self, *args, separator_token_id=31, **kwargs):
        super().__init__(*args, **kwargs)
        self.separator_token_id = separator_token_id


    def masked_sep_loss(model, batch, device):
        targets = batch['input_ids']
        shifted_targets = torch.zeros_like(targets)  # Initialize a tensor of zeros with the same shape as targets
        shifted_targets[:, :-1] = targets[:, 1:]
        targets = shifted_targets.to(device)

        outputs = model(batch['input_ids'].to(device)).logits

        sep_token_id = tokenizer.vocab['[SEP]']
        pad_token_id = tokenizer.vocab['<|pad|>']

        batch_size, sequence_length = targets.shape

        # Create a tensor representing positions [0, 1, 2, ..., sequence_length-1] for comparison
        positions = torch.arange(sequence_length).unsqueeze(0).expand(batch_size, -1).to(targets.device)

        # Identify the position of the SEP token. Assuming SEP token is the first occurrence in the sequence.
        sep_positions = (targets == sep_token_id).long().argmax(dim=1)

        # Create a mask where positions greater than sep_positions are True
        sep_mask = positions > sep_positions.unsqueeze(-1)
        pad_mask = targets != pad_token_id  # True for non-pad tokens

        # Combine masks to ignore positions after SEP and pad positions
        mask = sep_mask & pad_mask

        # Using a softmax layer followed by a cross-entropy loss
        softmax_logits = F.softmax(outputs, dim=2)
        log_probs = softmax_logits.log()  # Get log probabilities
        loss = F.nll_loss(log_probs.transpose(1, 2), targets, reduction='none')   # Calculate loss, transposing log_probs to match expected input shape of nll_loss

        # Apply the mask to the loss
        masked_loss = loss * mask.float()

        # final_loss is now the mean loss for the positions after the SEP token across the batch
        final_loss = masked_loss.sum() / mask.sum()

        return final_loss


# Arugments for input to HuggingFace Trainer
training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=1e-5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=5,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=500, 
    evaluation_strategy='steps',
    save_strategy = 'epoch',
    save_total_limit=3,
    eval_steps = 200,
    remove_unused_columns=True
)

from torch.nn.parallel import DistributedDataParallel as DDP

# HuggingFace trainer - this automates batching and iteration
trainer = CustomNLLEntropyLossTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,  
    tokenizer=tokenizer,
    # compute_metrics=compute_metrics,
    callbacks=[MetricsLoggingCallback()]
)


trainer.train()

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
