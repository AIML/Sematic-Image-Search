#!/usr/bin python
import sys
sys.path.insert(0,'/home/william/caffe-master/python')
import numpy as np
import matplotlib.pyplot as plt
import caffe

'''
The wrapper for calling the deep-net to get the feature of the region
Here will provide two way for calling:
    One: provide the database, which path is stored in the test layer of
         the test net prototxt
    Two: provide a image to extract the feature
'''
class NetWrapper(object):
    
    def __init__(self,caffe_path,cpu_only,model,proto):
        '''
        Inital the net paramter:
        caffe_path : used for load the caffe model
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
            loop_num=0,
            batch_size=0,
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
        the data of out_layer contains  the predict result 
        the data of feature_layer contains the feature result
        labels_file contians the label of input data
        feature_file used for save the result
        return:
          the result will stored in feature_file
        '''
        if image==None:
            '''
            try:
                labels = np.loadtxt(labels_file,str,delimiter='\t')
            except:
                print 'load label file error!'
                return
            '''
            for i in range(0,loop_num):
                out = self.net.forward()
                try:
                    file_id = open(feature_path+'feature'+str(i),'w+')
                except:
                    print 'open file error: '+str(i)
                    return
                #get the label and the feature
                for j in range(0,batch_size):
                    features = self.net.blobs[feature_layer].data[j]
                    file_id.write('\t'.join(list(features))+'\n')
                file_id.close()
        else:
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
            self.net.blobs['data'].data[...]=\
                    self.transformer.preprocess(
                            'data',
                            caffe.io.load_image(image)
                            )
            out = self.net.forward()
            #just test
            print("Predicted class is #{}."\
                    .format(out['prob'][0].argmax()))

