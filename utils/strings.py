# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 13:25:42 2018

@author: Rybakov
"""

#-------------------------------------------------------------------------------

def chop(s, size = 1):
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
        chop("123456789", -4) -> ["1", "2345", "6789'"]
    """
    
    if len(s) <= abs(size):
        # The string is too short to chop.
        return [s]
    
    if size > 0:
        # Positive chop size - chop from its head.
        r = chop(s[size : ], size)
        r.insert(0, s[ : size])
        return r
    elif size < 0:
        # Negative chop size - chop from its end.
        r = chop(s[: size], size)
        r.append(s[size : ])
        return r
    else:
        # Chop size must not be zero.
        raise ValueError("Zero chop size.")
        
#-------------------------------------------------------------------------------
