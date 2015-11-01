#########################################################################
# File Name: train.sh
# Author: williamchen
# mail: 767004082@qq.com
# Created Time: 2015年10月29日 星期四 07时57分11秒
#########################################################################
#!/bin/bash
#Extract the feature of train label
if [ $# != 3 ]; then
	echo "Usage: data_path aux_file label"
	echo "Note aux_file must has the format img_path \\t img_label \\n"
	exit 1
fi
data_path=$1
aux_file=$2
label=$3

#make db
if [ -d ../data/$label ]; then
	echo "$label dictory already exists!"
	exit 1
fi
mkdir ../data/$label
mkdir ../data/$label/feature
cp $aux_file ../data/$label/train.txt
./create_db.sh ../data/$label $data_path ../data/$label \
	../../caffe-master/build/tools

#extract feature
echo "extract feature"
total_num=`wc -l ../data/$label/train.txt | awk '{ print $1 }'`
let loop_num=$total_num/10+1 
python ../test/get_feature_test.py ../model/bvlc_googlenet.caffemodel \
	../model/test.prototxt $loop_num 10 $total_num prob loss3/classifier \
	../data/$label/feature/
echo "done"
