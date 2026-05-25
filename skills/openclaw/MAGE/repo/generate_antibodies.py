# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import argparse

def main():
    parser = argparse.ArgumentParser(description="Antibody generation against WT RBD prompt.")
    parser.add_argument('-n', '--n', type=int, required=True, help='Number of antibodes')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output file')

    args = parser.parse_args()

    output_file = args.output
    num_abs = args.n

    print(f"Number of antibodies: {num_abs}")
    print(f"Output file: {output_file}")


    import os
    from datasets import load_dataset
    import torch
    from tokenizers import Tokenizer
    import pandas as pd

    from transformers import TrainerCallback, TrainingArguments, Trainer, PreTrainedTokenizerFast
    from progen.progen2.models.progen.modeling_progen import ProGenForCausalLM

    if torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        print('No GPU detected')

    path_to_saved_model = './model_epoch4'
    # path_to_saved_model = '../base_v2/model/results_full_model_v2/checkpoint-8332'

    rbd_prompt = 'RVQPTESIVRFPNITNLCPFGEVFNATRFASVYAWNRKRISNCVADYSVLYNSASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSKVGGNYNYLYRLFRKSNLKPFERDISTEIYQAGSTPCNGVEGFNCYFPLQSYGFQPTNGVGYQPYRVVVLSFELLHAPATVCGPKKSTNLVKNKCVNF'

    model = ProGenForCausalLM.from_pretrained(path_to_saved_model)
    model.eval()
    model.to(device)

    tokenizer = PreTrainedTokenizerFast.from_pretrained(path_to_saved_model)

    def generate_sequences(model, antigen_seq, number_of_abs=1, top_p=0.9, temperature=1, max_length=1024):
        # Tokenize antigen sequence
        tokenized_sequence = tokenizer.encode(antigen_seq)
        seqs = []
        # Convert to PyTorch tensor and add batch dimension
        input_tensor = torch.tensor([tokenized_sequence]).to(device)
        count = 0

        with torch.no_grad():
            while count < (number_of_abs):            
                output = model.generate(input_tensor, max_length=max_length, pad_token_id=tokenizer.encode('<|pad|>')[0], do_sample=True, top_p=top_p, temperature=temperature, num_return_sequences=1)
                
                for i in output:
                    seq = tokenizer.decode(i)
                    seqs.append(seq)
                
                count += 1

        seq_df = pd.DataFrame(seqs)
        return seq_df

    prompt = rbd_prompt + '[SEP]'
    max_seq_len = len(prompt) + 250

    seq_df = generate_sequences(model, prompt, number_of_abs=num_abs, max_length=max_seq_len)
    seq_df.to_csv(output_file)



if __name__ == "__main__":
    main()

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
