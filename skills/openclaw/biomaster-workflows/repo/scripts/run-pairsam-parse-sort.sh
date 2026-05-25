#!/bin/bash
if [ $# -le 2 ] ; then
    echo "Usage: bash run-pairsam-parse-sort.sh BAM OUTPUT_PREFIX CHR_SIZES THREADS COMPRESS_PROGRAM"
    echo ""
    echo "A example of a run-pairsam-parse-sort.sh pipeline"
    echo ""
    echo "positional arguments:"
    echo ""
    echo "BAM             The path to a BAM file."
    echo "CHR_SIZES       The path to a chromosome sizes file."
    echo "OUTDIR          The output directory."
    echo "OUTPUT_PREFIX   The prefix to the paths of generated outputs. "
    echo "THREADS         Number of threads"
    echo "COMPRESS_PROGRAM    Program for file compression"
    echo ""
    echo ""

    exit 0
fi

set -o errexit
set -o nounset
set -o pipefail

BAM=$1
CHR_SIZES=$2
OUTDIR=$3
OUTPREFIX=$4
THREADS=${5:-8}
COMPRESS_PROGRAM=${6:=lz4c}
SORTED_PAIRS_PATH=${OUTDIR}/${OUTPREFIX}.sam.pairs.gz

if [[ ${OUTDIR} != "." ]]; then
  mkdir -p ${OUTDIR}
fi

samtools view -h "${BAM}" | {
    # Classify Hi-C molecules as unmapped/single-sided/multimapped/chimeric/etc
    # and output one line per read, containing the following, separated by \\v:
    #  * triu-flipped pairs
    #  * read id
    #  * type of a Hi-C molecule
    #  * corresponding sam entries
    pairtools parse -c $CHR_SIZES --add-columns mapq
} | {
    # Block-sort pairs together with SAM entries
    pairtools sort --nproc ${THREADS} \
    --memory 48G \
    --compress-program ${COMPRESS_PROGRAM} \
    --tmpdir ${OUTDIR} \
    --output ${SORTED_PAIRS_PATH}
}

