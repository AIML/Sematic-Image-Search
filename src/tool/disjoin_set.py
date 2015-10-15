#!/usr/bin python
'''
The implimention of the disjoint set forest
Note if you want use follow functions you must have the parameter
have the following "node definition", which means the structure
must have follows fields
class node(object):
    parent = None    #the pointer to his parent
    value = None     #save the value of this node
    next = None      #save the connection info  
    rank = 0         #the depth of the tree
'''
class disjoin_set(object): 
    @staticmethod
    def union(item1,item2):
        '''
        item1 and item2 will be a item (the index of it)
        which may not be a representative element
        and the union of item1 and item2 will
        result in union of the two tree
        '''
        return disjoin_set.__link(disjoin_set.find(item1),disjoin_set.find(item2))
    @staticmethod
    def __link(root1,root2):
        '''
        union the two set
        which representative by item1 and item2
        use "union by rank"
        '''
        if root1.rank > root2.rank:
            root2.parent = root1
            return root1
        else:
            root1.parent = root2
            if root1.rank==root2.rank:
                root2.rank += 1
            return root2
    @staticmethod
    def find(item):
        '''
        return the representative element of item
        use "path compression"
        item is the index in data
        '''
        if item!=item.parent:
            item.parent = disjoin_set.find(item.parent)
        return item.parent
