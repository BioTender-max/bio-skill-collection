#调用dorado basecaller前需保证相关dorado model已安装
pod5dir=$1 
ref=$2
out=$3
#需根据实际dorado路径调整
../dorado-0.9.1-linux-x64/bin/dorado basecaller hac,5mCG_5hmCG --models-directory ./model/ $pod5dir --reference $ref > $out