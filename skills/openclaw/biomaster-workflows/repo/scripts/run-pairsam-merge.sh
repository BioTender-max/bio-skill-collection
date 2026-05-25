#!/bin/bash
if [ $# -le 2 ] ; then
    echo "Usage: bash run-pairsam-merge.sh OUTPUT_PREFIX THREADS PAIRSAM"
    echo ""
    echo ""
    echo "positional arguments:"
    echo ""
    echo "OUTPUT_PREFIX   The prefix to the paths of generated outputs. "
    echo "THREADS         Number of threads for merging."
    echo "PAIRSAM         Space separated pairsam " 
    echo ""
    echo ""

    exit 0
fi

set -o errexit
set -o nounset
set -o pipefail

OUTPREFIX=$1
THREADS=${2:-8}
INFILESTR=${@:3}
INFILES=(${INFILESTR// / })
MAXFILEMERGE=${#INFILES[@]}
echo "Merging $MAXFILEMERGE files..."
MEMORY=2G
MERGED_PAIRSAM=${OUTPREFIX}.merged.sam.pairs.gz
TEMPDIR=""

pairtools merge --max-nmerge ${MAXFILEMERGE} --nproc ${THREADS} --memory ${MEMORY} --output ${MERGED_PAIRSAM} ${INFILES[@]}
