# -*- coding: utf-8 -*-
"""
Ecomonic functionality.

Created on Mon Jul  2 15:45:53 2018

@author: Rybakov
"""

import utils as ut
from functools import reduce
import numpy as np


#-------------------------------------------------------------------------------
# Class smart money.
#-------------------------------------------------------------------------------

class money:
    """
    Peace of money for financial manipulations.
    """
    
    ten = 10            # Alias for 10.
    hundred = 100       # Alias for 100.
    digits_in_group = 3 # Digits count in group when number represented 
                        # as "1 000 000" (three digits in this case).
    delim = " "         # Delimiter for parts of numerical value.
    vat = 0.18          # VAT value.
    
#-------------------------------------------------------------------------------    
    
    def __init__(self, v, is_vat = False):
        """
        Constructor from value (float or string).
        
        Arguments:
            v -- value.
        """
        
        # Process VAT flag.
        self.is_vat = is_vat
        
        # Process value.
        if type(v) is float:
            # Just float value.
            self.init_f(v)
        elif type(v) is str:
            # It it is string we must delete all spaces, 
            # because we want to process strings like "1 000 000.00".
            self.init_f(float(v.replace(money.delim, "")))
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
        self.amount = int(round(v * money.hundred))
        
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
        
        chopped = ut.str_chop(str(self.hi()), -3)
        merged = ut.li_merge(chopped, [money.delim] * (len(chopped) - 1))
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

        # Check for type.
        if not (type(self.amount) is int):
            raise TypeError("Money amount must be stored as integer.")

        return self.hi_str() + "." + self.lo_str()

#-------------------------------------------------------------------------------
        
    def distribute(self, ks):
        """
        Distribute money value between len(ks) money objects according
        with given coefficients.
        
        Arguments:
            ks -- numpy array of coefficients.
        
        Result:
            Distributed money (numpy array).
        """
    
        # Count of coefficients.
        n = len(ks)
        
        if n == 0:
            # No distribution.
            raise ValueError("No factors for distribute money.")
        
        if n == 1:
            # Only one factor.
            return self
        
        # First normalize list.
        nks = ut.li_norm(ks)
        
        # Create array for new moneys.
        ms = [0] * n
        
        # Cycle of initialization array of amounts for new moneys.
        rest = self.amount
        for i in range(n - 1):
            am = int(round(self.amount * nks[i]))
            rest -= am
            ms[i] = money(0.0)
            ms[i].amount = am
            
        # The last element calculate from rest.
        ms[n - 1] = money(0.0)
        ms[n - 1].amount = rest
        
        # Create money objects.
        return ms
    
#-------------------------------------------------------------------------------
        
    def split(self, k):
        """
        Split money.
        
        Arguments:
            k -- split value (from 0.0 to 1.0).

        Result:
            Tuple of splitted values.
        """
        
        if (k < 0.0) or (k > 1.0):
            # Check split factor.
            raise ValueError("Split factor must be in [0.0, 1.0] segment.")

        return self.distribute(np.array([k, 1.0 - k]))

#-------------------------------------------------------------------------------

    def add_vat(self):
        """
        Add VAT to amount.
        """
        
        # It is possible to add VAT only once.
        if self.is_vat:
            raise RuntimeError("Re-charging VAT.")
        
        # Charge VAT.
        self.amount = int(round((self.amount * (1.0 + self.vat))))
        self.is_vat = True

#-------------------------------------------------------------------------------
        
    def sub_vat(self):
        """
        Sub VAT from amount.
        """
        
        # It is possible to sub VAT only once.
        if not self.is_vat:
            raise RuntimeError("Re-extraction VAT.")
        
        # Extract VAT.
        self.amount = int(round(self.amount / (1.0 + self.vat)))
        self.is_vat = False
        
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
