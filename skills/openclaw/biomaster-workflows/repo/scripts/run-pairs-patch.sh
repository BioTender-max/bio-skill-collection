#!/bin/bash

input_pairs=$1
outprefix=$2
gunzip -c $input_pairs | duplicate_header_remover.pl | column_remover.pl - sam1 sam2 | column_remover.pl -d - 8 | bgzip -c > $outprefix.pairs.gz
pairix -f $outprefix.pairs.gz


