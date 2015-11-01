#!/usr/bin python

import cv2 as cv
import numpy as np
import random

import sys
sys.path.append("../src/feature")
sys.path.append("../src/segment")
sys.path.append("../src/tool")

from segmentor import vertex_node
from disjoin_set import disjoin_set
from get_region import SegmentorWrapper

if len(sys.argv)!=4 and len(sys.argv)!=5:
    sys.stderr.write("Usage;\tsys.argv[0]\timg_path\tthresh\tslack\t[region_patn]\n")
    sys.exit(-1)

if len(sys.argv)==4:
    '''
    extract the feature for one image
    '''
    img_path = sys.argv[1]
    thresh = float(sys.argv[2])
    slack = int(sys.argv[3])
    my_segmentor = SegmentorWrapper(thresh,slack)
    bbs = my_segmentor.get_region(img_path)
    print len(bbs)
    #draw the result
    img = cv.imread(img_path,1)
    #img = cv.resize(img,(128,128))
    height = img.shape[0]
    width = img.shape[1]
    #img_copy = img.copy()
    for bb in bbs:
        cv.rectangle(img,(bb[0],bb[1]),(bb[2],bb[3]),[80,160,255],1)
    '''
    regions = {}
    for i in range(0,len(bbs)):
        region = disjoin_set.find(bbs[i])
        raw = i//width
        column = i-raw*width
        if regions.has_key(region):
            regions[region].append((raw,column))
        else:
            regions[region]=[(raw,column)]
    for region in regions:
        color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        for pixel in regions[region]:
            img[pixel[0],pixel[1]]=color
    '''
    cv.imshow("region",img)
    cv.waitKey(0)
    cv.destroyAllWindows()
else:
    img_path = sys.argv[1]
    thresh = float(sys.argv[2])
    slack = int(sys.argv[3])
    region_path = sys.argv[4]
    my_segmentor = SegmentorWrapper(thresh,slack)
    print my_segmentor.get_region(img_path,region_path)

