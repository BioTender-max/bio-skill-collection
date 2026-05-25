numcore=$1 
sam=$2
sortedBam=$3
samtools view -@ $numcore -S $sam -b | samtools sort -o $sortedBam - ; samtools index $sortedBam