fastq=$1
out=$2
# filter reads: Q≥10、500-10kbp 
cat $fastq | NanoFilt -q 10 -l 500 > $out