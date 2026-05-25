#调用dorado basecaller前需保证相关dorado model已安装
pod5dir=$1 
out=$2
#需根据实际dorado路径调整
../dorado-0.9.1-linux-x64/bin/dorado basecaller hac --models-directory ./model/ $pod5dir > $out