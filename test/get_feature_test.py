#!/usr/bin python
'''

'''
import sys
sys.path.append('../src/feature')

import numpy as np
import matplotlib.pyplot as plt

from get_feature import NetWrapper

caffe_path='/home/william/caffe-master/'
model_path=caffe_path+'models/'
proto_path=caffe_path+'models/'
cpu_only=True

def test(model,proto,image):
    my_net = NetWrapper(
            caffe_path,
            cpu_only,
            model_path+model,
            proto_path+proto
            )
    my_net.preprocess()
    my_net.getfeature(image)

if __name__=='__main__':
    if len(sys.argv)!=4:
        print "Usage:\tsys.argv[0]\tmodel\tproto\timage"
        sys.exit(1)
    else:
        test(sys.argv[1],sys.argv[2],sys.argv[3])
