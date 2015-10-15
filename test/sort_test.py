import sys
sys.path.append("../src/tool")
sys.path.append("../src/segment")

from sort import sort_tool
from segmentor import edge_node
from segmentor import cmp_e

def main(data):
    value=[]
    for item in data:
        value.append(item.w)
    print "The data is: "+"\t".join(value)
    sort_tool.quick_sort(data,cmp_e)
    value=[]
    for item in data:
        value.append(item.w)   
    print "The sort result is: "+"\t".join(value)

if __name__=="__main__":
    if len(sys.argv)<2:
        sys.stderr.write("Plese input the data\n")
        sys.exit(1)
    else:
        data=[]
        for i in  range(1,len(sys.argv)):
            data.append(edge_node(0,0,sys.argv[i]))
        main(data)
