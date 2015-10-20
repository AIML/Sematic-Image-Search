#!/usr/bin python

import sys
sys.path.append("../tool")
import cv2 as cv
import numpy as np


from segmentor import vertex_node
from segmentor import segmentor
from disjoin_set import disjoin_set
from similar import pixel_similar
from similar import region_similar


'''
Here I implement the "selectvie search" which proposed by
J.R.R Uijlings K.E.A van de Sande T.Gevers A.W.M Smeulders
in paper "Selective Search for Object Recognizition",the 
authors use the Greedy method to group the region together
by the pro-defined similar level in a hierarchy manner.
And reapeat this process util the region equals the iamge.
And in order to cover various scene and light conditions.
The Author use different group strategy, and use follow three
aspect to make the strategy:
    1 different colour space
    2 different similar measures
    3 different inital regions
And combine the object hypotheses together
'''
def merge_bb(bb1,bb2):
    bb=[[bb1[0][0],bb1[0][1]],[bb1[1][0],bb1[1][1]]]
    if bb1[0][0] > bb2[0][0]:
        bb[0][0] = bb2[0][0]
    elif bb1[0][1] > bb2[0][1]:
        bb[0][1] = bb2[0][1]
    else:
        pass
    if bb1[1][0] < bb2[1][0]:
        bb[1][0] = bb2[1][0]
    elif bb1[1][1] < bb2[1][1]:
        bb[1][1] = bb2[1][1]
    else:
        pass
    return bb
class region_node(object):
    colour_his = []         #save the colour historgram use L1-norm to normalize
    size = 0                #the area of the region by piexl
    bounding_box = None     #store the up_lift and down_right pointer of the box around region
    region_value = []       #store the value of region,here is color of each pixel in region
    def __init__(self,c_h=None,s=0,bb=[]):
        self.colour_his = c_h
        self.size = s
        self.bounding_box = []
        self.region_value = []
    def add_p(self,pixel,color):
        '''
        Insert a pixel into the region
        Here for 
        '''
        self.region_value.append(color)
        self.size += 1
        if self.size==1: #first pointer
            self.bounding_box=[[pixel[0],pixel[1]],[pixel[0],pixel[1]]]
        else:
            if self.bounding_box[0][0] > pixel[0]:
                self.bounding_box[0][0] = pixel[0]
            elif self.bounding_box[1][0] < pixel[0]:
                self.bounding_box[1][0] = pixel[0]
            else:
                pass
            if self.bounding_box[0][1] > pixel[1]:
                self.bounding_box[0][1] = pixel[1]
            elif self.bounding_box[1][1] < pixel[1]:
                self.bounding_box[1][1] = pixel[1]
            else:
                pass
    def merge(self,region):
        self.bounding_box = merge_bb(
                self.bounding_box,
                region.bounding_box
                );
        for i in range(0,len(self.colour_his)):
            self.colour_his[i] = float((self.size*self.colour_his[i])\
                    +(region.size*region.colour_his[i]))/(self.size\
                    +region.size)
        self.size += region.size

class selective_search(object):
    @staticmethod
    def make_pair(img_size,similar_set,region_set,similar_coef,region1,region2):
        if region1!=region2 and not similar_set.has_key((region1,region2)) \
                and not similar_set.has_key((region2,region1)):
                    similar=0
                    if similar_coef[0]!=0:
                        similar += region_similar.Scolour(
                                region_set[region1].colour_his,
                                region_set[region2].colour_his
                                )
                    if similar_coef[1]!=0:
                        similar += region_similar.Ssize(
                                region_set[region1].size,
                                region_set[region2].size,
                                img_size
                                )
                    if similar_coef[2]!=0:
                        region_bb = merge_bb(
                                region_set[region1].bounding_box,
                                region_set[region2].bounding_box
                                )
                        region_bb_size = \
                                (region_bb[1][0]-region_bb[0][0])\
                                *(region_bb[1][1]-region_bb[0][1])
                        similar += region_similar.Sfill(
                                region_set[region1].size,
                                region_set[region2].size,
                                region_bb_size,
                                img_size
                                )
                    similar_set[(region1,region2)] = similar
        else:
            pass
    @staticmethod
    def initial_set(img,initial_regions,bins,similar_coef,similar_set,region_set,bb_set):
        width = img.shape[1]
        height = img.shape[0]
        img_size = img.size
        for i in range(0,len(initial_regions)):
            pixel = (i//width,i-(i//width)*width)
            color = img[pixel[0],pixel[1]]
            region = disjoin_set.find(initial_regions[i])
            if region_set.has_key(region):
                region_set[region].add_p(pixel,color)
            else:
                region_set[region] = region_node()
                region_set[region].add_p(pixel,color)
        for region in region_set:
            his = region_similar.histogram(
                    region_set[region].region_value,
                    bins)
            region_set[region].colour_his = his/his.sum()
            bb_set.append(region_set[region].bounding_box)
        for i in range(0,len(initial_regions)):
            raw = i//width
            column = i-raw*width
            if column < width-1:
                j = i+1
                region1 = disjoin_set.find(initial_regions[i])
                region2 = disjoin_set.find(initial_regions[j])
                if region1!=region2:
                    selective_search.make_pair(
                            img_size,
                            similar_set,
                            region_set,
                            similar_coef,
                            region1,
                            region2
                            )
            if raw < height-1:
                j = (raw+1)*width+column
                region1 = disjoin_set.find(initial_regions[i])
                region2 = disjoin_set.find(initial_regions[j])
                if region1!=region2:
                    selective_search.make_pair(
                            img_size,
                            similar_set,
                            region_set,
                            similar_coef,
                            region1,
                            region2
                            )
            if raw < height-1 and column < width-1:
                j = (raw+1)*width+(column+1)
                region1 = disjoin_set.find(initial_regions[i])
                region2 = disjoin_set.find(initial_regions[j])
                if region1!=region2:
                    selective_search.make_pair(
                            img_size,
                            similar_set,
                            region_set,
                            similar_coef,
                            region1,
                            region2
                            )

    @staticmethod
    def group(img,initial_regions,bins,similar_coef,thresh):
        '''
        img is the source img, note it was represent in a special colour-space
        initial_reigons is the start regions
        bins is the number of bins in colour historgram
              similar is the list of coefficient for indicating which similar is used
        thresh used for filter the start regions 
        '''
        region_set = {}  #store the region and it's propoerty
        similar_set = {} #store the similar of Neighbouring region
        bb_set = []      #store the result object hypothesis in bounding box
        height = img.shape[0]
        width = img.shape[1]
        img_size = img.size
        #first: get the similar of each region in initial regions
        selective_search.initial_set(
                img,
                initial_regions,
                bins,
                similar_coef,
                similar_set,
                region_set,
                bb_set
                )
        #just for test
        count=0
        for region in region_set:
            count += region_set[region].size
        print count
        for pair in similar_set:
            if pair[0]==pair[1]:
                print region_set[pair[0]].size,region_set[pair[1]].size
        #second: group the most similar region togather 
        #and repeat this process
        while len(similar_set)>1:
            merge_pair = None
            big_similar = 0
            for pair in similar_set:
                if big_similar < similar_set[pair]:
                    big_similar = similar_set[pair]
                    merge_pair = pair
            if merge_pair==None:
                print len(similar_set)
                for pair in similar_set:
                    print similar_set[pair]
            region1 = merge_pair[0]
            region2 = merge_pair[1]
            region_set[region1].merge(
                    region_set[region2]
                    )
            bb_set.append(region_set[region1].bounding_box)
            similar_set.pop((region1,region2))
            old_similar_set = similar_set.copy()
            for pair in old_similar_set:
                if region1 in pair:
                    similar_set.pop(pair)
                    if region1 == pair[0]:
                        selective_search.make_pair(
                                img_size,
                                similar_set,
                                region_set,
                                similar_coef,
                                region1,
                                pair[1]
                                )
                    else:
                        selective_search.make_pair(
                                img_size,
                                similar_set,
                                region_set,
                                similar_coef,
                                region1,
                                pair[0]
                                )
                elif region2 in pair:
                    similar_set.pop(pair)
                    if region2 == pair[0]:
                        selective_search.make_pair(
                                img_size,
                                similar_set,
                                region_set,
                                similar_coef,
                                region1,
                                pair[1]
                                )
                    else:
                        selective_search.make_pair(
                                img_size,
                                similar_set,
                                region_set,
                                similar_coef,
                                region1,
                                pair[0]
                                )
                else:
                    pass
        #return result
        return bb_set
