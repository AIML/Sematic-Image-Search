#!/usr/bin python
#encoding=utf8

class sort_tool(object):
    
    @staticmethod
    def count_sort(cmp,data,max):
        '''
        the implemention of count sort
        note:
             cmp is a lambda which used for get the key
             the key must be postive interger and no bigger than max
             data contains the data
        the important thing is the data will be changed
        ''' 
        keys = []
        mid = []
        position = []
        for i in range(0,max+1):
            position.append(0)
        for item in data:
            keys.append(cmp(item))
            mid.append(item)
        for key in keys:
            position[key] += 1
        for i in range(1,len(position)):
            position[i] += position[i-1]
        for i in range(0,len(mid)):
            data[position[mid[i]]-1] = mid[i]
            position[mid[i]] -= 1
        return data

    @staticmethod
    def __partion(data,start,end):
        '''
        the sort part, partion the data into two part,and the index is p
        one partion is  than A[p+1,end] which is larger than A[p]=A[end]
        the other partion is less than A[start,p-1] is less than A[p]
        '''
        pivot = data[end]
        i=start-1
        j=start
        for j in range(start,end):
            if data[j]<=pivot:
                i += 1
                tmp = data[i]
                data[i] = data[j]
                data[j] = tmp
        data[end] = data[i+1]
        data[i+1] = pivot
        return i+1

    @staticmethod
    def quick_sort(data,start=-1,end=-1):
        '''
        the recursive implemention of origin quick sort
        note:
            cmp is a lambda which used for get the key
            data contains the data
        the important thing is the data will be changed
        '''
        if start==-1 and end==-1:
            start = 0
            end = len(data)-1
        if end-start > 0:
            part = sort_tool.__partion(data,start,end)
            if part-start>1:
                sort_tool.quick_sort(data,start,part-1)
            if end-part>1:
                sort_tool.quick_sort(data,part+1,end)
        return data
