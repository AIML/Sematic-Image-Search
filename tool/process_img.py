#!/usr/bin python

import sys
import os

import cv2 as cv
import numpy as np

def process(img_path,res_path,new_size,channel_swap):
    if os.path.isfile(img_path) and not os.path.isdir(res_path):
        img = cv.imread(img_path,1)
        if img==None:
            sys.stderr.write("Error in Loading image: ",img_path)
            return 1
        else:
            img = cv.resize(img,new_size)
            img = img.transpose(channel_swap)
            im.write(res_path,img)
    elif os.path.isdir(img_path) and os.path.isdir(res_path):
        filelist = os.listdir(img_path)
        count=0
        for file in filelist:
            img = cv.imread(img_path+file,1)
            if img==None:
                continue
            count += 1
            img = cv.resize(img,new_size)
            img2 = img.transpose((2,0,1))
            img2 = img2[channel_swap,:,:]
            img2 = img2.transpose((1,2,0))
            cv.imwrite(res_path+file,img2)
        return count
    else:
        sys.stderr.write("Plese input aviluable path!")
        return -1
if __name__=='__main__':
    if len(sys.argv)==8:
        print process(
                sys.argv[1],
                sys.argv[2],
                (int(sys.argv[3]),int(sys.argv[4])),
                (int(sys.argv[5]),int(sys.argv[6]),int(sys.argv[7]))
                )
    else:
        sys.stderr.write("Usage: img_path res_path new_h new_w transpose\n")
        sys.exit(1)
