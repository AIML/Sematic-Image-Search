import sys
sys.path.append("../src/tool") 
from disjoin_set import disjoin_set

class node(object):
    parent = None
    value = None
    next = None
    rank = 0
    def __init__(self,v):
        self.parent = self
        self.value = v
        self.next = None
        self.rank = 0
def main(data):
    forest = []
    for item in data:
        forest.append(node(item))
    disjoin_set.union(forest[1],forest[2])
    disjoin_set.union(forest[3],forest[4])
    disjoin_set.union(forest[1],forest[4])
    for item in forest:
        if item==disjoin_set.find(item):
            print "item is:"+str(item)+"  value is:"+str(item.value)+"  parent is:"+str(item.parent)

if __name__=="__main__":
    if len(sys.argv)<6:
        sys.stderr.write('Plese input the data which is sotred in a list' \
                'and the length of list should not less than 5!'+"\n")
        sys.exit(1)
    else:
        data=[]
        for i in range(1,len(sys.argv)):
            data.append(sys.argv[i])
        main(data)
