# -*- coding: utf-8 -*-
"""
Utils functions.

Created on Mon Jul  2 15:34:59 2018

@author: Rybakov
"""

import numpy as np

#-------------------------------------------------------------------------------
# Lists (names start with li_*).
#-------------------------------------------------------------------------------

def li_merge(a, b):
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
    return [a[0], b[0]] + li_merge(a[1 :], b[1 :])

#-------------------------------------------------------------------------------
# Numpy arrays (names start with npa_*).    
#-------------------------------------------------------------------------------
    
def npa_norm(a):
    """
    Normalize numerical numpy array.
    
    Arguments:
        a -- array.
    
    Result:
        Normalized array.
    """

    return a / sum(a)

#-------------------------------------------------------------------------------
# Strings (names start with str_*).
#-------------------------------------------------------------------------------

def str_chop(s, size = 1):
    """
    Chop string.
    
    Arguments:
        s -- string,
        size -- chop size (if size is positive then the string is chopped
                from the beginning to its end, if size is negative then the
                string is chopped from the end to its beginning).
    
    Result:
        List of chunks - chopped string.
    
    Examples:
        chop("123456789", 4) -> ["1234", "5678", "9"]
        chop("123456789", -4) -> ["1", "2345", "6789"]
    """
    
    if len(s) <= abs(size):
        # The string is too short to chop.
        return [s]
    
    if size > 0:
        # Positive chop size - chop from its head.
        r = str_chop(s[size : ], size)
        r.insert(0, s[ : size])
        return r
    elif size < 0:
        # Negative chop size - chop from its end.
        r = str_chop(s[: size], size)
        r.append(s[size : ])
        return r
    else:
        # Chop size must not be zero.
        raise ValueError("Zero chop size.")
        
#-------------------------------------------------------------------------------
# Tests.
#-------------------------------------------------------------------------------

if __name__ == "__main__":
    assert li_merge([1, 1], [2, 2]) == [1, 2, 1, 2], "li_merge fault"
    assert li_merge([1], [2, 2, 2]) == [1, 2, 2, 2], "li_merge fault"
    assert li_merge([1, 1, 1], [2]) == [1, 2, 1, 1], "li_merge fault"
    #
    assert str_chop("123456789", 4) == ["1234", "5678", "9"], "str_chop fault"
    assert str_chop("123456789", -4) == ["1", "2345", "6789"], "str_chop fault"

#-------------------------------------------------------------------------------
        
    