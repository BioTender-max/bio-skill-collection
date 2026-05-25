fa=$1 
fastq=$2
out=$3
../minimap2/minimap2 -ax map-ont $fa $fastq | samtools view -b -f 4 > $out