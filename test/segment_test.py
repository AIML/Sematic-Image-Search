#!/usr/bin python

import sys
sys.path.append("../src/segment")
sys.path.append("../src/tool")

import cv2 as cv
import numpy as np
import random   #for test
from segmentor import segmentor
from segmentor import vertex_node
from disjoin_set import disjoin_set
from similar import pixel_similar

def main(img_path,thresh):
    #load the image
    raw_img = cv.imread(img_path)
    img = cv.cvtColor(raw_img,cv.COLOR_RGB2GRAY) #use gray image
    if img==None:
        sys.stderr.write("error happened in Loading img!")
        return
    cv.namedWindow('image',cv.WINDOW_NORMAL) # create a can resize window
    cv.imshow('image',img) #draw image in window named "image"
    cv.waitKey(0)          #until a key stroke, it will continue
    #resize the iamge
    img = cv.resize(img,(128,128))
    raw_img = cv.resize(raw_img,(128,128))
    #blur to remove the noise
    img = cv.GaussianBlur(img,(5,5),0.8,0.8,0)
    #Get the edge set of the image
    e_set=[]
    height = img.shape[0]
    width = img.shape[1]
    for i in range(0,height):
        for j in range(0,width):
            ij_edge=[]
            if j<width-1:
                similar = abs(img.item(i,j)-img.item(i,j+1))
                #similar = pixel_similar.normalize_dif((i,j),(i,j+1),img,5)
                ij_edge.append((i*width+j+1,similar))
            if i<height-1:
                similar = abs(img.item(i,j)-img.item(i+1,j))
                #similar = pixel_similar.normalize_dif((i,j),(i+1,j),img,5)
                ij_edge.append(((i+1)*width+j,similar))
            if j<width-1 and i<height-1:
                similar = abs(img.item(i,j)-img.item(i+1,j+1))
                #similar = pixel_similar.normalize_dif((i,j),(i+1,j+1),img,5)
                ij_edge.append(((i+1)*width+(j+1),similar))
            e_set.append(ij_edge)
    print "The number of vertex is: "+str(len(e_set))
    #do segment
    k=350   #(which is good for image with size: 128*128)
    img_seg = segmentor.grap_base_seg(e_set,k)
    print len(img_seg)
    count=0
    for item in img_seg:
        if item == item.parent:
            count+=1
    print "region number is: "+str(count)
    #draw the result
    regions = {}
    '''
    for i in range(0,len(img_seg)):
        raw = i//width
        column = i-(raw*width)
        region = disjoin_set.find(img_seg[i])
        if regions.has_key(region):
            if regions[region][0]>raw:
                regions[region][0]=raw
            elif regions[region][1]<raw:
                regions[region][1] = raw
            else:
                pass
            if regions[region][2]>column:
                regions[region][2] = column
            elif regions[region][3]<column:
                regions[region][3] = column
            else:
                pass
        else:
            regions[region]=[raw,raw,column,column]
    '''
    for i in range(0,len(img_seg)):
        raw = i//width
        column = i-(raw*width)
        region = disjoin_set.find(img_seg[i])
        if regions.has_key(region):
            regions[region].append((raw,column))
        else:
            regions[region]=[(raw,column)]
    pixel_num = 0 
    for region in regions:
        color=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        pixel_num += len(regions[region])
        if len(regions[region]) > thresh:
            for p in regions[region]:
                raw_img[p[0],p[1]] = color
    print "The number of pixel in region is: "+str(pixel_num)
    cv.imshow('res',raw_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

    '''
    count=0
    for region in regions:
        count += 1
        # if count>50:
        #     break
        
        #note rectangle's coordinate is inverse with opencv's
        
        up_left = (regions[region][2],regions[region][0])
        down_right = (regions[region][3],regions[region][1])
        if (down_right[0]-up_left[0])*(down_right[1]-up_left[1]) < thresh:
            continue
        print "region"+str(count)+": "+str(up_left[0])+" "+str(up_left[1])\
                +" "+str(down_right[0])+" "+str(down_right[1])
        cv.rectangle(img,up_left,down_right,255,1)
    raw_input()
    cv.imshow("result",img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    '''
if __name__=="__main__":
    if len(sys.argv)!=3:
        sys.stderr.write("Plese input the path of the image and area threshold\n")
        sys.exit(1)
    else:
        main(sys.argv[1],int(sys.argv[2]))
