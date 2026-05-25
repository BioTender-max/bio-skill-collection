#!/usr/bin/env bash
if [ $# -le 2 ] ; then
    echo "Usage: bash run-pairsam-filter.sh PAIRSAM OUTPUT_PREFIX CHR_SIZES"
    echo ""
    echo "A example run-pairsam-filter.sh pipeline for processing sorted reads to get nodup pairs file"
    echo ""
    echo "positional arguments:"
    echo ""
    echo "PAIRSAM             The path to a PAIRSAM file."
    echo "OUTPUT_PREFIX       The prefix to the paths of generated outputs. "
    echo "CHR_SIZES           Chromosomes and their sizes "
    echo ""
    echo ""

    exit 0
fi
set -o errexit
set -o nounset
set -o pipefail

PAIRSAM=$1
OUTPREFIX=$2
CHR_SIZES=$3

UNMAPPED_SAMPAIRS=${OUTPREFIX}.unmapped.sam.pairs.gz
DEDUP_PAIRS=${OUTPREFIX}.dedup.pairs.gz
LOSSLESS_BAM=${OUTPREFIX}.lossless.bam
TEMPFILE=temp.gz
TEMPFILE1=temp1.gz

## Generate lossless bam
pairtools split --output-sam ${LOSSLESS_BAM} ${PAIRSAM}


# Select UU, UR, RU reads
pairtools select '(pair_type == "UU") or (pair_type == "UR") or (pair_type == "RU")' \
    --output-rest ${UNMAPPED_SAMPAIRS} \
    --output ${TEMPFILE} \
    ${PAIRSAM}

pairtools split --output-pairs ${TEMPFILE1} ${TEMPFILE}

pairtools select 'True' --chrom-subset ${CHR_SIZES} -o ${DEDUP_PAIRS} ${TEMPFILE1}

pairix ${DEDUP_PAIRS}  # sanity check & indexing    




