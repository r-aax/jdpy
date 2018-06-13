# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 18:20:16 2018

@author: Rybakov
"""

#------------------------------------------------------------------------------

def merge(a, b):
    """
    Merge two lists.
    
    Keyword arguments:
        a -- the first list,
        b -- the second list.
    
    Result:
        Merged list.
        
    Examples:
        merge([1, 1, 1], [2, 2, 2]) -> [1, 2, 1, 2, 1, 2]
        merge([1, 1, 1, 1], [2, 2]) -> [1, 2, 1, 2, 1, 1]
        merge([1, 1], [2, 2, 2, 2]) -> [1, 2, 1, 2, 2, 2]
    """
    
    # Check the case when one list is empty.
    if a == []:
        return b
    if b == []:
        return a

    # Both lists are non empty.
    h = [a[0], b[0]]
    return h + merge(a[1 :], b[1 :])

#------------------------------------------------------------------------------