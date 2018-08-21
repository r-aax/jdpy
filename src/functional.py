# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 14:47:36 2018

@author: Rybakov
"""

#-------------------------------------------------------------------------------

def is_all(a, pred):
    """
    Check all elements with predicate.
    
    Arguments:
        a -- list,
        pred -- predicate.
        
    Result:
        True -- if all pred(a[i]) are true,
        False -- if there is pred(a[i]) that is not true.
    """
    
    if a == []:
        return True
    
    if not pred(a[0]):
        return False
    
    return is_all(a[1:], pred)

#-------------------------------------------------------------------------------

def is_any(a, pred):
    """
    Check if any pred(a[i]) is true.
    
    Arguments:
        a -- list,
        pred -- predicate.
    
    Result:
        True -- is there is pred(a[i]) that is true,
        False -- if all pred(a[i]) are false.
    """
    
    if a == []:
        return False
    
    if pred(a[0]):
        return True
    
    return is_any(a[1:], pred)

#-------------------------------------------------------------------------------
# Tests.
#-------------------------------------------------------------------------------

if __name__ == "__main__":
    assert is_all([1, 2, 3], lambda x: x < 5), "is_all fault 01"
    assert not is_all([1, 2, 3], lambda x: x < 2), "is_all fault 02"
    assert is_all([], lambda x: x == 100), "is_alll_fault 03"
    #
    assert not is_any([1, 2, 3], lambda x: x > 10), "is_any fault 01"
    assert is_any([1, 2, 3], lambda x: x > 2), "is_any fault 02"
    assert not is_any([], lambda x: x == 10), "is_any fault 03"

#-------------------------------------------------------------------------------
