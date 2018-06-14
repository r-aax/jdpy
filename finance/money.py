# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 23:03:54 2018

@author: Rybakov
"""

from utils import lists, strings
from functools import reduce

class money:
    """
    Peace of money for financial manipulations.
    """
    
    ten = 10            # Alias for 10.
    hundred = 100       # Alias for 100.
    digits_in_group = 3 # Digits count in group when number represented 
                        # as "1 000 000" (three digits in this case).
    
#-------------------------------------------------------------------------------   
    
    def __init__(self, v):
        """
        Constructor from value (float or string).
        
        Arguments:
            v -- value.
        """
        
        if type(v) is float:
            # Just float value.
            self.init_f(v)
        elif type(v) is str:
            # It it is string we must delete all spaces, 
            # because we want to process strings like "1 000 000.00".
            self.init_f(float(v.replace(" ", "")))
        else:
            raise ValueError("Wrong money type.")
        
#-------------------------------------------------------------------------------   

    def init_f(self, v):
        """
        Init money from non-negative float value.
        
        Arguments:
            v -- value.
        """
        
        if v < 0.0:
            # Negative money values are not supported.
            raise ValueError("Wrong money value.")
            
        # Store money value multiplied on 100 (in kopecks, cents, etc.).
        self.amount = round(v * money.hundred)        
        
#-------------------------------------------------------------------------------   

    def hi(self):
        """
        High part of money (rubles, dollars, etc.).
        
        Result:
            High part of money.
        """
        
        return self.amount // money.hundred
    
#-------------------------------------------------------------------------------   

    def lo(self):
        """
        Low part of money (kopecks, cents, etc.).
        
        Result:
            Low part of money.
        """
        
        return self.amount % money.hundred
    
#-------------------------------------------------------------------------------   

    def hi_str(self):
        """
        High part string representation in form "1 000 000".
        
        Result:
            High part string representation.
        """
        
        chopped = strings.chop(str(self.hi()), -3)
        merged = lists.merge(chopped, [" "] * (len(chopped) - 1))
        return reduce(lambda a, b: a + b, merged)
                    
#-------------------------------------------------------------------------------   

    def lo_str(self):
        """
        Low part string representation in form "dd" (two digits).
        
        Result:
            Low part string representation.
        """
        
        s = str(self.lo())
        
        if len(s) == 1:
            # Add leading zero.
            return "0" + s
        elif len(s) == 2:
            # Pure string.
            return s
        else:
            raise ValueError("Wrong money low value.")

#-------------------------------------------------------------------------------   

    def __repr__(self):
        """
        Get money string representation.
        
        Result:
            String representation.
        """

        return self.hi_str() + "." + self.lo_str()

#-------------------------------------------------------------------------------
