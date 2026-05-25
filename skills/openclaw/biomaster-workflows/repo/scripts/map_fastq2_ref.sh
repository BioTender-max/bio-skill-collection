fq=$1 
sam=$2
ref=$3
numcore=$4
sed -i 's/U/T/g' $fq
#需根据实际minimap2路径调整
../minimap2/minimap2 -ax map-ont -t $numcore $ref $fq > $sam
echo "minimap2 has finished aligning samples to the reference with 'minimap2 align -x rnaseq -t $numcore -r $ref -d $fq -o $sam'."