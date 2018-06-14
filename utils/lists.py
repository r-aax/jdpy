# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 18:20:16 2018

@author: Rybakov
"""

import numpy as np

#-------------------------------------------------------------------------------

def duplicate(a, times):
    """
    Duplicate list.
    
    Arguments:
        a -- list,
        times -- fadctor of duplicating.
    
    Result:
        Duplicated list.
        
    Examples:
        duplicate([], 5) -> []
        duplicate([a, b], 3) -> [a, b, a, b, a, b]
        
    Note:
        This function is needed because we don't use list multiplication.
        This code uses numpy package where array multiplication means the
        different.
        [5] * 3 -> [5, 5, 5] for common arrays
        [5] * 3 -> [15] for numpy arrays
    """
    
    if a == []:
        # Empty list.
        return []
    
    if times == 1:
        # End of recursion.
        return a
    
    if times == 0:
        # Zero degree of list.
        return []
    
    # Recursion.
    new_a = a.append(duplicate(a, times - 1))
    return new_a
    
#-------------------------------------------------------------------------------

def merge(a, b):
    """
    Merge two lists.
    
    Arguments:
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

#-------------------------------------------------------------------------------
    
def normalize(a):
    """
    Normalize numerical numpy array.
    
    Arguments:
        li -- array.
    
    Result:
        Normalized array.
    """
    
    s = sum(a)
    return a / s

#-------------------------------------------------------------------------------