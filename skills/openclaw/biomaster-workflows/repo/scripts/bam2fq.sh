numcore=$1 
bam=$2
out=$3
samtools fastq -@ $numcore -n $bam > $out