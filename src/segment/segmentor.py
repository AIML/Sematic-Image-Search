#!/usr/bin python

import sys
sys.path.append("../tool")
import cv2 as cv

from disjoin_set import disjoin_set
from sort import sort_tool

#The implimention of image segment method
class vertex_node(object):
    '''
    Used for save the vertex
    '''
    #for the disjoin_set
    parent = None
    next = None
    rank = 0
    #save the Inter-component differnces of a region (short as Int(C))
    value = 0
    #save the threshold of a belive level for a boundary evidence
    coefficient = 1

    def __init__(self,v):
        self.parent = self
        self.next = None
        self.rank = 0
        self.value = 0
        self.coefficient = 1

class edge_node(object):
    '''
    Used for save the edge
    '''
    v1=-1
    v2=-1
    w=0
    def __init__(self,v1,v2,w):
        self.v1=v1
        self.v2=v2
        self.w=w
def cmp_e(e1,e2):
    '''
    Used for order the edge
    '''
    if e1.w>e2.w:
        return 1
    elif e1.w==e2.w:
        return 0
    else:
        return -1

class segmentor(object):

    @staticmethod
    def grap_base_seg(e_set,k):
        '''
        Here we will implimention the graph based iamge segment method
        which proposed by Pedro F.Felzenszwalb and Daniel P.Huttenlocher
        in the paper "Efficient Graph-Based Image Segmentation"
        This method based on Kruskal's algorithm and use the disjoin set
        as the data structure
        The interpretation of arguments:
            e_set : is the  list of edge's weight, and it saved in a 
            symmetric matrix. And the index is the position of pixel 
            which ordered by column first, raw second.As the matrix will
            be very sparse, so here use link chain to store
            k : is the coefficent multiplier
        The result will stored in the disjoin set
        '''
        #Zero: order the edge in e_set by weight in Ascending order        
        ord_e = []
        for i in range(0,len(e_set)):
            for j in range(0,len(e_set[i])):
                ord_e.append(edge_node(i,e_set[i][j][0],e_set[i][j][1]))
        ord_e.sort(cmp_e)
        #First: initialize the segment,v_set will maintains the result
        v_set = []
        for raw in range(0,len(e_set)):
            v_set.append(vertex_node(0))
        #Second, split loop, for each edge do the follow
        for e in ord_e:
            region1 = disjoin_set.find(v_set[e.v1])
            region2 = disjoin_set.find(v_set[e.v2])
            if region1!=region2:
                Int1 = region1.value +  k/region1.coefficient
                Int2 = region2.value +  k/region2.coefficient
                Int = Int1
                if Int1 > Int2:
                    Int = Int2
                if e.w <= Int: #then the two region can be merged
                    region = disjoin_set.union(region1,region2)
                    region.value = e.w #the max w in MST of region
                    region.coefficient = region1.coefficient + region2.coefficient
            else:
                continue
        #Third, return the result
        return v_set
