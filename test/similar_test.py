#!/usr/bin python

import sys
sys.path.append("../src/segment")

from similar import pixel_similar
from similar import region_similar
import numpy as np

def pixel_similar_test():
    A=np.zeros((5,6),np.uint8)
    A=A+1
    A[0:5,3:6]+=1
    similar = pixel_similar.normalize_dif((2,2),(2,3),A,5)
    print A
    print similar
def region_similar_test():
    region1=[[1],[1],[2],[2],[3],[3],[4],[4],[5],[5]]
    region2=region1
    print region_similar.Scolour(region1,region2,5,5)

if __name__=="__main__":
    if len(sys.argv)!=2:
        sys.stderr.write("Please choose from [pixel or region]")
        sys.exit(1)
    else:
        if sys.argv[1]=="pixel":
            pixel_similar_test()
        elif sys.argv[1]=="region":
            region_similar_test()
        else:
            pass
