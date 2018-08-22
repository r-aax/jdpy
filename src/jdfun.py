# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 14:47:36 2018

@author: Rybakov
"""

"""
Functions for functional programming.
"""

#-------------------------------------------------------------------------------

def is_all(a, pred):
    """
    Check all elements with predicate.
    
    Arguments:
        a -- deep list (which elements can be deep lists too),
        pred -- predicate.
        
    Result:
        True -- if all elemens are true,
        False -- if there is an element for which predicate is not true.
    """
    
    # Empty list.
    if a == []:
        return True
    
    # Not a list at all, but single element.
    if not isinstance(a, list):
        return pred(a)
        
    # General case.
    return is_all(a[0], pred) and is_all(a[1:], pred)

#-------------------------------------------------------------------------------

def is_any(a, pred):
    """
    Check is there an element for which the predicate is true.
    
    Arguments:
        a -- deep list (which elements can be deep lists too),
        pred -- predicate.
    
    Result:
        True -- is there is an element for which the predicate is true,
        False -- if the predicate is false for all elements.
    """
    
    # Empty list.
    if a == []:
        return False
    
    # Not a list at all, but single element.
    if not isinstance(a, list):
        return pred(a)
    
    # General case.
    return is_any(a[0], pred) or is_any(a[1:], pred)

#-------------------------------------------------------------------------------
    
def zip_with(a, b, fun):
    """
    Zip two deep lists with the given function.
    
    Arguments:
        a -- the first deep list,
        b -- the second deep list,
        fun -- zip function.
        
    Result:
        Zipped deep list.
    """
    
    # Check for empty lists (and check the shapes of a and b are equal).
    is_a = a == []
    is_b = b == []
    if is_a != is_b:
        raise RuntimeError("zip_with: deep arrays a and b shapes differ")
    if is_a:
        return []
    
    # Check if a or b is a single element (and check shapes again).
    is_a = isinstance(a, list)
    is_b = isinstance(b, list)
    if is_a != is_b:
        raise RuntimeError("zip_with: deep arrays a and b shapes differ")
    if not is_a:
        return fun(a, b)
    
    # General case: a and b are deep lists.
    return list(map(lambda c: zip_with(c[0], c[1], fun),
                    list(zip(a, b))))

#-------------------------------------------------------------------------------

def zip_tuple(a, b):
    """
    Zip two deep lists into tuple.
    
    Arguments:
        a -- the first deep list,
        b -- the second deep list.
        
    Result:
        Zipped deep list.
    """
    
    return zip_with(a, b, lambda x, y: (x, y))

#-------------------------------------------------------------------------------

def zip_add(a, b):
    """
    Zip two lists with add function.
    
    Arguments:
        a -- the first deep list,
        b -- the second deep list.
        
    Result:
        Zipped deep list.
    """
    
    return zip_with(a, b, lambda x, y: x + y)

#-------------------------------------------------------------------------------

def zip_sub(a, b):
    """
    Zip two lists with sub function.
    
    Arguments:
        a -- the first deep list,
        b -- the second deep list.
        
    Result:
        Zipped deep list.
    """
    
    return zip_with(a, b, lambda x, y: x - y)

#-------------------------------------------------------------------------------

def zip_mul(a, b):
    """
    Zip two lists with mul function.
    
    Arguments:
        a -- the first deep list,
        b -- the second deep list.
        
    Result:
        Zipped deep list.
    """
    
    return zip_with(a, b, lambda x, y: x * y)

#-------------------------------------------------------------------------------

def zip_div(a, b):
    """
    Zip two lists with div function.
    
    Arguments:
        a -- the first deep list,
        b -- the second deep list.
        
    Result:
        Zipped deep list.
    """
    
    return zip_with(a, b, lambda x, y: x / y)

#-------------------------------------------------------------------------------
# Tests.
#-------------------------------------------------------------------------------

if __name__ == "__main__":
    assert is_all([1, 2, 3], lambda x: x < 5), "is_all fault 01"
    assert not is_all([1, 2, 3], lambda x: x < 2), "is_all fault 02"
    assert is_all([], lambda x: x == 100), "is_all fault 03"
    assert is_all([1, [2, [4, 4]]], lambda x: x < 5), "is_all fault 04"
    assert not is_all([4, [2, [10]], 1], lambda x: x < 5), "is_all fault 05"
    #
    assert not is_any([1, 2, 3], lambda x: x > 10), "is_any fault 01"
    assert is_any([1, 2, 3], lambda x: x > 2), "is_any fault 02"
    assert not is_any([], lambda x: x == 10), "is_any fault 03"
    assert not is_any([1, [2, [8, 8]], 3], lambda x: x > 10), "is_any fault 01"
    assert is_any([1, [2], [[3]]], lambda x: x > 2), "is_any fault 02"
    #
    assert zip_with([1, [2, 3]], [4, [5, 6]],
                    lambda x, y: x + y) == [5, [7, 9]], "zip_with fault 01"
    assert zip_tuple([1, [[2]]], [3, [[4]]]), "zip_tupple fault 01"

#-------------------------------------------------------------------------------
