# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 13:44:47 2018

@author: Rybakov
"""

import math
import numpy as np
import utils as ut

#-------------------------------------------------------------------------------
# Functions for generating ds-sequence.
#-------------------------------------------------------------------------------

def ds_half(n):
    """
    Sequence ds
        d[0] = n // 2
        ...
        d[i] = d[i - 1] // 2
        ...
        d[k] = 1
    
    Arguments:
        n -- the length of array to be sorted.
        
    Result:
        ds array.
    """
    
    # There is nothing to sort.
    if n < 2:
        return []

    # Common case.
    n2 = n // 2
    return [n2] + ds_half(n2)    

#-------------------------------------------------------------------------------
    
def ds_hibbard(n):
    """
    Hibbard's ds sequence
        2**i - 1 for all values in segment [1, n].
        
    Arguments:
        n -- the length of array to be sorted.
        
    Result:
        ds array.
    """
    
    # There is nothing to sort.
    if n < 2:
        return []

    # Common case.
    hi_bound = int(math.log2(n + 1))
    return list(2 ** np.array(range(1, hi_bound + 1)) - 1)[::-1]

#-------------------------------------------------------------------------------
    
def ds_sedgewick(n):
    """
    Sedgewick's ds sequence.
        d_i = 9 * (2 ** i) - 9 * (2 ** (i / 2)) + 1, if i is even,
        d_i = 8 * (2 ** i) - 6 * (2 ** ((i + 1) / 2)) + 1, if i is odd.
        Maximum d_{i - 1} if 3 * d_i > n.
    
    Arguments:
        n -- the length of array to be sorted.
        
    Result:
        ds array.
    """
    
    # There is nothing to sort.
    if n < 2:
        return []
    
    # Function d[i].
    d = lambda i: 9 * (2 ** i) - 9 * (2 ** (i // 2)) + 1 if i % 2 == 0 \
                  else 8 * (2 ** i) - 6 * (2 ** ((i + 1) // 2)) + 1
    
    # Main loop.
    r = [1]
    i = 2
    while 3 * r[0] <= n:
        r = [d(i)] + r
        i += 1
        
    # Cut one element and return.
    if r != [1]:
        r = r[1:]
    return r
    
#-------------------------------------------------------------------------------
    
def ds_pratt(n):
    """
    Pratt's ds sequence.
        (2 ** i) * (3 ** j) <= n / 2 for all i, j > 0.
        
    Arguments:
        n -- the length of array to be sorted.
        
    Result:
        ds array.
    """

    # Get raw array.
    raw = [(2 ** i) * (3 ** j) \
           for i in range(0, int(math.log2(n / 2)) + 1) \
           for j in range(0, int(math.log(n / 2, 3)) + 1)]
    
    # Sort and uniq.
    su = ut.li_sort_uniq(raw)
    
    # Filter and reverse.
    return list(filter(lambda x: x <= n // 2, su))[::-1]

#-------------------------------------------------------------------------------
    
def shell(a, ds):
    """
    Shell sort.
    
    Arguments:
        a -- array,
        ds -- array of gaps.
        
    Result:
        Sorted list.
    """
    
    n = len(a)
    
    # d-loop
    for d in ds:
    
        arr_d = []
        
        # i-loop
        i = d
        while i < n:
        
            t = a[i]
            
            cnt_j = ut.Cnt()
            
            # j-loop
            j = i
            while j >= d:
                
                cnt_j.inc()
                
                if t < a[j - d]:
                    a[j] = a[j - d]
                else:
                    break
                
                j -= d
                
            arr_d += [cnt_j.v]
                
            a[j] = t
            i += 1  
        
        print(arr_d)
        
    # Result.
    return a
    
#-------------------------------------------------------------------------------
