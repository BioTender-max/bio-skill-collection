bam=$1 
transcripts_gtf=$2
out=$3
stringtie $bam -o transcripts.gtf -A $out