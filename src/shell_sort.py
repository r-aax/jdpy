# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 13:44:47 2018

@author: Rybakov
"""

import math
import numpy as np
import utils as ut
import jdfun

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

def ds_fib(n):
    """
    Fibbonacci's ds sequence.
    
    Arguments:
        n -- the length of array to be sorted.
        
    Result:
        ds array.
    """
    
    # Begin of fib list.
    r = [1, 2]
    
    # Main loop.
    while ut.li_last(r) < n:
        r += [sum(r[-2:])]
        
    # Filter and return the result.
    return list(filter(lambda x: x < n, r))[::-1]

#-------------------------------------------------------------------------------

def shell_stat(a, ds):
    """
    Shell sort statistics print.
    
    Arguments:
        a -- array,
        ds -- array of gaps.
        
    Result:
        Sorted list.
    """
    
    n = len(a)
    
    o_stats = []
    v_stats = []
    
    # d-loop
    for d in ds[:-1]:
        
        o_stat = 0
        v_stat = 0
        inner_lens = []
        
        # i-loop
        i = d
        while i < n:
        
            t = a[i]
            
            inner_len = 0
            
            # j-loop
            j = i
            while j >= d:

                inner_len += 1
                                
                if t < a[j - d]:                    
                    a[j] = a[j - d]
                else:
                    break
                
                j -= d
                                
            a[j] = t
            i += 1
            
            o_stat += inner_len
            inner_lens.append(inner_len)
            if len(inner_lens) == min(16, d):
                v_stat += max(inner_lens)
                inner_lens = []
        
        if (len(inner_lens) > 0):
            v_stat += max(inner_lens)
            inner_lens = []
        
        o_stats.append(o_stat)
        v_stats.append(v_stat)
        
    # Final print.
#    print(o_stats)
#    print(v_stats)
#    print(jdfun.zip_div(o_stats, v_stats))
    so = sum(o_stats)
    sv = sum(v_stats)
    print("so/sv/sp = ", so, sv, so / sv)
    
#-------------------------------------------------------------------------------
