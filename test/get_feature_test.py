#!/usr/bin python
'''
Test for get feature
'''
import sys
sys.path.append('../src/feature')

import numpy as np
import matplotlib.pyplot as plt

from get_feature import NetWrapper

cpu_only=True

def test1(
        model,
        deploy_proto,
        image,
        out_layer,
        feature_layer
        ):
    my_net = NetWrapper(
            cpu_only,
            model,
            deploy_proto
            )
    my_net.preprocess()
    my_net.getfeature(
            image,
            " ",
            out_layer,
            feature_layer
            )
def test2(
        model,
        test_proto,
        img_path,
        aux_file,
        outlayer,
        featurelayer,
        feature_path
        ):
    my_net = NetWrapper(
            cpu_only,
            model,
            test_proto
            )
    my_net.preprocess()
    return my_net.getfeature(
            img_path,
            aux_file,
            outlayer,
            featurelayer,
            feature_path
            )

if __name__=='__main__':
    if len(sys.argv)!=6 and len(sys.argv)!=8:
        print "Usage:\tsys.argv[0]\tmodel\tproto\
                \t[image\
                \taux_file\
                \tout_layer\tfeature_layer\
                \tfeature_path]"
        sys.exit(1)
    else:
        if len(sys.argv)==6:
            test1(
                    sys.argv[1],
                    sys.argv[2],
                    sys.argv[3],
                    sys.argv[4],
                    sys.argv[5]
                    )
        else:
            print test2(
                    sys.argv[1],
                    sys.argv[2],
                    sys.argv[3],
                    sys.argv[4],
                    sys.argv[5],
                    sys.argv[6],
                    sys.argv[7]
                    )
