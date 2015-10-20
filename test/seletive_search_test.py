import sys
sys.path.append("../src/segment")
sys.path.append("../src/tool")

import cv2 as cv
import numpy as np

from segmentor import vertex_node
from segmentor import segmentor
from disjoin_set import disjoin_set
from similar import region_similar
from selective_search import region_node
from selective_search import selective_search as ssearch

def main():
    #make the image
    img = np.zeros((128,128),np.uint8)
    img[:,:] += 100
    #make the region
    region1 = region_node()
    for i in range(10,31):
        for j in range(10,41):
            region1.add_p((i,j),[200])
    his = region_similar.histogram(region1.region_value,25)
    region1.colour_his = his/his.sum()
    region2 = region_node()
    for i in range(30,61):
        for j in range(20,31):
            region2.add_p((i,j),[50])   
    his = region_similar.histogram(region2.region_value,25)
    region2.colour_his = his/his.sum()
    region3 = region_node()
    for i in range(10,21):
        for j in range(40,51):
            region3.add_p((i,j),[150])
    his = region_similar.histogram(region3.region_value,25)
    region3.colour_his = his/his.sum()
    region1.merge(region3)
    region1.merge(region2)
    #draw region
    print "region1's colour_his is:"
    print region1.colour_his
    print "region1's size is:"+str(region1.size)
    cv.rectangle(
            img,
            (region1.bounding_box[0][1],region1.bounding_box[0][0]),
            (region1.bounding_box[1][1],region1.bounding_box[1][0]),
            255)
    cv.imshow('region1',img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    '''
    region_set = {}
    similar_set = {}
    similar_coef = [1,1,1]
    region_set[1] = region1
    region_set[2] = region2
    region_set[3] = region3
    ssearch.make_pair(
            img.size,
            similar_set,
            region_set,
            similar_coef,
            1,
            2)
    ssearch.make_pair(
            img.size,
            similar_set,
            region_set,
            similar_coef,
            1,
            3)
    print similar_set[(1,2)],similar_set[(1,3)]
    '''
def ssearch_test(img_path):
    img = cv.imread(img_path)
    if img == None:
        sys.stderr.write("error happend in Loading image!\n")
        return
    cv.namedWindow('image',cv.WINDOW_NORMAL)
    cv.imshow('image',img)
    cv.waitKey(0)
    img = cv.resize(img,(128,128))
    img = cv.GaussianBlur(img,(5,5),0.8,0.8,0)
    lab_img = cv.cvtColor(img,cv.COLOR_RGB2LAB)
    '''
    for i in range(0,img.shape[0]):
        for j in range(0,img.shape[1]):
            if img.item(i,j,0) > 255 or img.item(i,j,0)<0\
                    or img.item(i,j,1) > 255 or img.item(i,j,1) < 0\
                    or img.item(i,j,2) > 255 or img.item(i,j,2) < 0:
                        print img[i,j]
    '''
    gray_img = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
    e_set=[]
    height = img.shape[0]
    width = img.shape[1]
    for i in range(0,height):
        for j in range(0,width):
            ij_edge=[]
            if j<width-1:
                similar = abs(gray_img.item(i,j)-gray_img.item(i,j+1))
                ij_edge.append((i*width+j+1,similar))
            if i<height-1:
                similar = abs(gray_img.item(i,j)-gray_img.item(i+1,j))
                ij_edge.append(((i+1)*width+j,similar))
            if j<width-1 and i<height-1:
                similar = abs(gray_img.item(i,j)-gray_img.item(i+1,j+1))
                ij_edge.append(((i+1)*width+(j+1),similar))
            e_set.append(ij_edge)
    k=150
    initial_regions = segmentor.grap_base_seg(e_set,k)
    count=0
    for item in initial_regions:
        if item == item.parent:
            count += 1
    print "The number of regions in initial is: "+str(count)
    bins = 25
    similar_coef = [1,1,1]
    bb_set = ssearch.group(lab_img,initial_regions,bins,similar_coef,0)
    #draw the result
    for item in bb_set:
        mid_img=img.copy()
        if (item[1][0]-item[0][0])*(item[1][1]-item[0][1]) < 900:
            continue
        cv.rectangle(mid_img,(item[0][1],item[0][0]),(item[1][1],item[1][0]),[255,255,255])
        cv.imshow('result',mid_img)
        cv.waitKey(0)
    cv.destroyAllWindows()

if __name__=='__main__':
    if len(sys.argv)==1:
        main()
    else:
        ssearch_test(sys.argv[1]);
