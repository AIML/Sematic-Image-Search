#!/usr/bin python
import sys
sys.path.insert(0,'/home/william/caffe-master/python')
import os

import numpy as np
import matplotlib.pyplot as plt
import caffe

'''
The wrapper for calling the deep-net to get the feature of the region
Here will provide two way for calling:
    One: provide the folder where storage the image
    Two: provide a image to extract the feature
'''
class NetWrapper(object):
    
    def __init__(self,cpu_only,model,proto):
        '''
        Inital the net paramter:
        cpu_only: true for use cpu,false for use GPU
        model: the mode have been trained
        proto: the prototxt defining the net structure used for testing 
        '''
        if cpu_only:
            caffe.set_mode_cpu()
        else:
            caffe.set_device(0)
            caffe.set_mode_gpu()
        self.net = caffe.Net(proto,model,caffe.TEST)
    def preprocess(self,
            transpose=(2,0,1),
            scale=225,
            mean=np.array([104,117,123]),
            channel_swap=(2,1,0)
            ):
        '''
        preprocess the image to feat to the net model
        This is very import for second usage: provide a image
        '''
        self.transformer = caffe.io.Transformer(
                {'data':self.net.blobs['data'].shape}
                )
        self.transformer.set_transpose('data',transpose)
        self.transformer.set_mean('data',mean)
        self.transformer.set_raw_scale('data',scale)
        self.transformer.set_channel_swap('data',channel_swap)
    def getfeature(
            self,
            image=None,
            aux_file=None,
            out_layer=None,
            feature_layer=None,
            feature_path=None
            ):
        '''
        get the feature
        input:
        if the image provided, then this net used for getting the
        feature for one image
        if the image stay None, then this net used for getting the
        feature for the picture in the test database
        loop_num is the time call for net forward pass
        batch size is the number of data feat to net each pass
        total num is the number of test image
        the data of out_layer contains  the predict result 
        the data of feature_layer contains the feature result
        labels_file contians the label of input data
        feature_file used for save the result
        return:
          the result will stored in feature_file
        '''
        #reshape the net inpurt layer
        shape=self.net.blobs['data'].data.shape
        channel=shape[1]
        width=shape[2]
        height=shape[3]
        self.net.blobs['data'].reshape(
                1,
                channel,
                width,
                height
                )

        if aux_file!=" ":
            try:
                labels = open(aux_file,'r')
            except:
                sys.stderr.write("load label file error! "+aux_file+'\n')
                return -1
            try:
                res = open(feature_path+'feature','w+')
            except:
                sys.stderr.write("load feature file error! "+featuere_path+'\n')
                return -1
            if not os.path.isdir(image):
                sys.stderr.write("image should be path of folder for storing picture!\n")
                return -1
            cur_batch = 0
            for line in labels:
                line_sp = line.rstrip('\n').split('\t')
                label = line_sp[1]
                img_path = image+line_sp[0]
                self.net.blobs['data'].data[...]=\
                        self.transformer.preprocess(
                                'data',
                                caffe.io.load_image(img_path)
                                )
                out = self.net.forward()
                #get the label and the feature
                feat = self.net.blobs[feature_layer].data[0]
                s=''
                for item in feat:
                    s += str(item)+' '
                s += label+'\n'
                res.write(s)
                cur_batch += 1
            return cur_batch
        else:
            if not os.path.isfile(image):
                sys.stderr.write(image+" is not a valiuable file name!\n")
                return -1
            self.net.blobs['data'].data[...]=\
                    self.transformer.preprocess(
                            'data',
                            caffe.io.load_image(image)
                            )
            out = self.net.forward()
            #just test
            #print feature
            feat = self.net.blobs[feature_layer].data[0]
            print feat
            #print predicted result
            print("Predicted class is #{}."\
                    .format(out[out_layer][0].argmax()))

