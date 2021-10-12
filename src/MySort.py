# -*- coding: cp1252 -*-
"""
Created on Mon Apr 27 10:29:14 2015

@author: ggrbill
"""

def MySort( SortList, ExtraList ):
    ct = 0
    try:
        size = len( SortList )
    except:
        size = SortList.size
    while 1:
        ct += 1
        resp = 1
        for i in range( size - 1 ):
            if SortList[i] > SortList[i+1]:
                lista_i = SortList[i]
                SortList[i] = SortList[i+1]
                SortList[i+1] = lista_i
                
                lista_i = ExtraList[i]
                ExtraList[i] = ExtraList[i+1]
                ExtraList[i+1] = lista_i    
                
                resp = 0
                
        if resp == 1:
            break


if __name__ == '__main__':
    import random
    a = range( 10 )
    b = range( 10 )
    
    for i in range( 10 ):
        a[i] = random.randrange(0, 10);
        b[i] = random.random()
    
    print a
    print b

    MySort( a, b )
    print a
    print b