#!/usr/bin python
import sys
sys.path.append("../tool")

import numpy as np
import math

'''
Here I will implement the methods to caculate the similar between two pixels
First is the most simple one, which use the differ in light intensity,
as the common sense that edge is the discontinuity of light intensity.
Second is the advanced version of the First. Intuitively, 
'''
class pixel_similar(object):
    @staticmethod
    def normalize_dif(p1,p2,img,size):
        '''
        p1 and p2 is a tuples each contanis the coordinate of the pixels
        (x,y)
        img is the image contanis p1 and p2, and it must be a grayscale
        size is the size of region around p1 and p2 to take into account
        note it must be positive and odd
        normlize_dif between two pixel:
               |I(p1)-I(p2)|/var(region(p1,p2))
        '''
        w=0
        h=0
        if type(size)==int:
            w=h=size
        else:
            w=size[0]
            h=size[1]

        if img.shape[0] < p1[0]+h//2 or p1[0] < h//2 \
                or img.shape[1] < p1[1]+w//2 or p1[1] < w//2 \
                or img.shape[0] < p2[0]+h//2 or p2[0] < h//2 \
                or img.shape[1] < p2[1]+w//2 or p2[1] < w//2:
                    pass
        else:
            h_min=h_max=w_min=w_max=0
            if p1[0] >= p2[0]:
                h_min = p2[0]
                h_max = p1[0]
            else:
                h_min = p1[0]
                h_max = p2[0]
            if p1[1] >= p2[1]:
                w_min = p2[1]
                w_max = p1[1]
            else:
                w_min = p1[1]
                w_max = p2[1]
            array = np.array(img[h_min-h//2:h_max+h//2+1,\
                    w_min-w//2:w_max+w//2+1],int)
            mean = float(array.sum())/array.size
            dif = (array - mean)*(array - mean)
            var = math.sqrt(float(dif.sum())/(array.size-1))
            if var!=0:
                return abs(img.item(p1[0],p1[1])-img.item(p2[0],p2[1])/var)
        return abs(img.item(p1[0],p1[1])-img.item(p2[0],p2[1]))

class region_similar(object):
    @staticmethod
    def histogram(region,bins,Max=255):
        '''
        region sotres the value
        caculate the histogram of region
        bins is the number of bins in the histogram
        Max is the max value may appears in region
        '''
        channels = len(region[0])
        his = np.zeros(bins*channels,np.float)
        inter = float(Max+1)/bins
        for item in region:
            for channel in range(0,channels):
                his[item[channel]//inter+channel*bins] += 1
        return his

    @staticmethod
    def Scolour(his1,his2):
        '''
        This used to cauculate the color similar of the two regions
        his1,his2 : the colour historgram
        Here the value of similar will be [0,1], and use L1 norm 
           similar = sum(min(his1[i],his2[i])) (i=0 to bins)
        '''
        if len(his1)!=len(his2):
            return 0
        similar = 0
        for i in range(0,len(his1)):
            if his1[i] <= his2[i]:
                similar += his1[i]
            else:
                similar += his2[i]
        return similar
    @staticmethod
    def Ssize(region1_size,region2_size,img_size):
        '''
        This used to caculate the size similar of the two regions
        '''
        return 1-float(region1_size+region2_size)/img_size

    @staticmethod
    def Sfill(region1_size,region2_size,region_bb_size,img_size):
        '''
        This used to caculate the fittness betweeen region1 and region2
        region_bb is the bounding box around region1 and region2
        '''
        return 1-float(region_bb_size-(region1_size+region2_size))/img_size
