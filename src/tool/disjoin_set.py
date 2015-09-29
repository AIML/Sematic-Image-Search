#!/usr/bin python
#encoding=utf8
import sys

#The implimention of the disjoint set forest
#node definition
class node(object):

    parent = None    #the pointer to his parent
    value = None     #save the value of this node
    next = None      #save the connection info  
    rank = 0         #the depth of the tree

    def __init__(self,v=None,p=None,r=0):
        '''
        if p==self : then it is a special case
        which parent is himself
        '''
        if p=="self":
            self.parent = self
            self.value = v
            self.rank = r
        else:
            self.parent = p
            self.value = v
            self.rank = r

class disjoin_set(object): 

    '''
    to mantain the tree root in the forest
    it will be used for the region container
    '''
    __forest = []      
    '''
    __container will mantain the refer of every item
    the most important thing shou pay attention
    ervery item will be refered by it's index in data
    '''
    __container = []

    def __init__(self,data=[]):
        '''
        here if data is not null
        all data will be in his self set
        data should be a list
        '''
        if len(data)!=0:
            for item in data:
                ref = node(item,"self")
                self.__container.append(ref)
    def union(self,item1,item2):
        '''
        item1 and item2 will be a item (the index of it)
        which may not be a representative element
        and the union of item1 and item2 will
        result in union of the two tree
        '''
        self.__link(self.find(item1),self.find(item2))
    def __link(self,root1,root2):
        '''
        union the two set
        which representative by item1 and item2
        use "union by rank"
        '''
        if root1.rank > root2.rank:
            root2.parent = root1
        else:
            root1.parent = root2
            if root1.rank==root2.rank:
                root2.rank += 1
    def find(self,item):
        '''
        return the representative element of item
        use "path compression"
        item is the index in data
        '''
        item = self.__container[int(item)]
        if item!=item.parent:
            item.parent=self.find(item.parent.value)
        return item.parent
    def get_forest(self,item):
        '''
        find the root of the tree in forest
        '''
        for item in self.__container:
            if item==item.parent:
                self.__forest.append(item)
        return __self.forest
    def Print(self):
        '''
        It just for test
        '''
        for tree in self.__forest:
            p = tree
            while p!=None:
                print str(p.value)+"\t"+str(p.parent)
                p=p.next
