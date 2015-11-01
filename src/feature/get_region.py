#!/usr/bin python
import sys
sys.path.append("../src/segment")
sys.path.append("../src/tool")
import os

import cv2 as cv
import numpy as np

from segmentor import segmentor
from disjoin_set import disjoin_set

'''
The SegmentorWrapper designed for easy use selective search segment
algorithm.
Here provide two ways to the segmentor:
     1th: get the region for a picture and return the boundingbox list
     2th: get the region for a batch of picuture and save the region in
          a folder as picture
'''
class SegmentorWrapper:
    def __init__(self,thresh=0,k=0,height=128,width=128):
        ''' 
        thresh is the fitler to maintain a region alive and it must be (0,1]
        if thresh==0 : then all region will be alived
        k is the slack variable for segmentor
        (width,heigh) is the standard size for segmentor
        '''
        self.thresh = thresh
        self.k = k
        self.height = height
        self.width = width
    def set_thresh(self,thresh):
        self.thresh = thresh
    def set_slack(self,k):
        self.slack = k
    def set_standsize(self,size):
        self.height = size[0]
        self.width = size[1]

    def __getOnePictureRegion(self,img):
        '''
        get region of the picture
        return:
             the boundingbox list of the image 
             and it save as ((xmin,ymin),(xmax,ymax))
        '''
        if img!=None:
            h_cof = float(img.shape[0])/self.height
            w_cof = float(img.shape[1])/self.width
            #resize the img to standard scale
            img = cv.resize(img,(self.height,self.width))
            #blur the image to remove the noise
            img = cv.GaussianBlur(img,(5,5),0.8,0.8,0)
            #get the edge set of the image
            e_set = []
            for i in range(0,self.height):
                for j in range(0,self.width):
                    ij_edge=[]
                    if j<self.width-1:
                        similar = abs(img.item(i,j)-img.item(i,j+1))
                        ij_edge.append((i*self.width+j+1,similar))
                    if i<self.height-1:
                        similar = abs(img.item(i,j)-img.item(i+1,j))
                        ij_edge.append(((i+1)*self.width+j,similar))
                    if j<self.width-1 and i<self.height-1:
                        similar = abs(img.item(i,j)-img.item(i+1,j+1))
                        ij_edge.append(((i+1)*self.width+(j+1),similar))
                    e_set.append(ij_edge)
            #do segment
            img_seg = segmentor.grap_base_seg(e_set,self.k)
            #return result in boundingbox list
            bbs = {}
            for i in range(0,len(img_seg)):
                raw = i//self.width
                column = i-raw*self.width
                region = disjoin_set.find(img_seg[i])
                if bbs.has_key(region):
                    if bbs[region][0] > column:
                        bbs[region][0] = column
                    if bbs[region][2] < column:
                        bbs[region][2] = column
                    if bbs[region][1] > raw:
                        bbs[region][1] = raw
                    if bbs[region][3] < raw:
                        bbs[region][3] = raw
                else:
                    bbs[region] = [column,raw,column,raw]
            regions = []
            filter_size = self.height*self.width*self.thresh
            for key in bbs:
                if (bbs[key][2]-bbs[key][0])\
                        *(bbs[key][3]-bbs[key][1])>=filter_size:
                            regions.append(
                                    [int(bbs[key][0]*w_cof),\
                                    int(bbs[key][1]*h_cof),\
                                    int(bbs[key][2]*w_cof),\
                                    int(bbs[key][3]*h_cof)]
                                    )
            return regions

    def get_region(self,img_path,region_path=None):
        '''
        img_path is the image full path
        if img_path is file then it will be called as the 1th method
        if img_path is a dictionary it will be called as the 2th method
        return:
            the bounding box list of the region in 1th method
            the region number in 2th method
        '''
        if os.path.isfile(img_path):
            #then is the 1th method
            img = cv.imread(img_path,0)
            if img==None:
                sys.stderr.write("Error in Loading "+img_path+'\n')
                return -1
            #do segment
            return self.__getOnePictureRegion(img)
        elif os.path.isdir(img_path):
            if not os.path.isdir(region_path):
                sys.stderr.write(region_path+" should be directory\n")
                return -1
            #process each img here
            filelist = os.listdir(img_path)
            count=0
            for file in filelist:
                if os.path.splitext(file)[1]==".JPEG":
                    img = cv.imread(img_path+file)
                    if img==None:
                        sys.stderr.write("Error in loading "+file+'\n')
                        continue
                    count += 1
                    gray_img = None
                    if len(img.shape)==3:
                        gray_img = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
                    else:
                        gray_img = img
                    #do segment
                    bbs = self.__getOnePictureRegion(gray_img)
                    #save the result
                    i=0
                    for bb in bbs:
                        i+=1
                        #note draw and sotre is different
                        region= img[bb[1]:bb[3]+1,bb[0]:bb[2]+1]
                        cv.imwrite(
                                region_path+os.path.splitext(file)[0]\
                                        +'_'+str(i)+".jpg",
                                        region)
                else:
                    continue
            return count
        else:
            sys.stderr.write(img_path+" is not a file or path!")
            return []
