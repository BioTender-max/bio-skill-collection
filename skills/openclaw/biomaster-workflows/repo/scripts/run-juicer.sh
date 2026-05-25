#!/bin/bash

fastq1=$1
fastq2=$2
index_file=$3
fasta=$4
chromsize_file=$5
restriction_file=$6
ncore=$7
outdir=$8

cd $outdir

# unzip index
tar -xzf $index_file
index=`ls -1 *.bwt | head -1 | sed 's/\.bwt//g'`

# reference fasta 
# (they must have the same prefix as the contents of the index file 
# and they should be in the same directory.)
if [[ $fasta =~ \.gz$ ]]
then
  gunzip $fasta
  fasta=${fasta/%\.gz/}
fi
cp $fasta ./$index

# unzip fastq files
if [[ $fastq1 =~ \.gz$ ]]
then
  gunzip $fastq1
  fastq1=${fastq1/%\.gz/}
fi

if [[ $fastq2 =~ \.gz$ ]]
then
  gunzip $fastq2
  fastq2=${fastq2/%\.gz/}
fi


juicer_dir=/usr/local/bin/juicer/
cwd=$(pwd)
echo $cwd 1>&2
mkdir -p $cwd/data_dir/fastq 1>&2
#cp $fastq1 $cwd/data_dir/fastq/data_R1.fastq 1>&2
#cp $fastq2 $cwd/data_dir/fastq/data_R2.fastq 1>&2
sed 's/\.1 / /g' $fastq1 > $cwd/data_dir/fastq/data_R1.fastq
sed 's/\.2 / /g' $fastq2 > $cwd/data_dir/fastq/data_R2.fastq
juicer.sh -t $ncore -z $index -d $cwd/data_dir -p $chromsize_file -y $restriction_file -D $juicer_dir -S early 1>&2
#mv $cwd/data_dir/fastq $cwd/data_dir/splits $cwd/data_dir/aligned/ $outdir
