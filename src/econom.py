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
    is_vat_ctrl = False # Control correct VAT processing.
    
#-------------------------------------------------------------------------------    
    
    def __init__(self, v = 0.0, is_vat = False):
        """
        Constructor from value (float or string).
        
        Arguments:
            v -- value,
            is_vat -- set initial VAT or not.
        """
        
        # Process VAT flag.
        self.is_vat = is_vat
        
        # Process value.
        if type(v) is float:
            # Just float value.
            self.init_f(v)
        elif type(v) is str:
            # If it is string we must delete all spaces, 
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
        
        # Store money value multiplied on 100 (in kopecks, cents, etc.).
        self.amount = int(round(v * money.hundred))

#-------------------------------------------------------------------------------

    def from_amount(a, is_vat):
        """
        Make money from high and low parts.
        
        Arguments:
            a -- amount,
            is_vat -- VAT flag.
        
        Result:
            New money value.
        """
        
        m = money()
        m.amount = a
        m.is_vat = is_vat
        return m
        
#-------------------------------------------------------------------------------

    def hi(self):
        """
        High part of money (rubles, dollars, etc.).
        
        Result:
            High part of money.
        """
        
        if self.amount < 0:
            return -((-self.amount) // money.hundred)
        else:
            return self.amount // money.hundred
    
#-------------------------------------------------------------------------------

    def lo(self):
        """
        Low part of money (kopecks, cents, etc.).
        
        Result:
            Low part of money.
        """
        
        if self.amount < 0:
            return (-self.amount) % money.hundred
        else:
            return self.amount % money.hundred
    
#-------------------------------------------------------------------------------

    def hi_str(self):
        """
        High part string representation in form "1 000 000".
        
        Result:
            High part string representation.
        """
        
        # Sign.
        hi = self.hi()
        sign = "-" if hi < 0 else ""
        
        # Take absulute value.
        if hi < 0:
            hi = -hi
        
        chopped = ut.str_chop(str(hi), -3)
        merged = ut.li_merge(chopped, [money.delim] * (len(chopped) - 1))
        return sign + reduce(lambda a, b: a + b, merged)
                    
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

        # VAT str.
        vat_str = "[V]" if self.is_vat else "[ ]"

        return self.hi_str() + "." + self.lo_str() + " " + vat_str

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
        nks = ut.npa_norm(ks)
        
        # Create array for new moneys.
        ms = [0] * n
        
        # Cycle of initialization array of amounts for new moneys.
        rest = self.amount
        for i in range(n - 1):
            am = int(round(self.amount * nks[i]))
            rest -= am
            ms[i] = money.from_amount(am, self.is_vat)
            
        # The last element calculate from rest.
        ms[n - 1] = money.from_amount(rest, self.is_vat)
        
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
        
        Result:
            New money with VAT.
        """
        
        # It is possible to add VAT only once.
        if self.is_vat_ctrl:
            if self.is_vat:
                raise RuntimeError("Re-charging VAT.")
        
        # Charge VAT.
        self.amount = int(round((self.amount * (1.0 + money.vat))))
        self.is_vat = True
        
        return self

#-------------------------------------------------------------------------------
        
    def sub_vat(self):
        """
        Sub VAT from amount.
        
        Result:
            New money without VAT.
        """
        
        # It is possible to sub VAT only once.
        if self.is_vat_ctrl:
            if not self.is_vat:
                raise RuntimeError("Re-extraction VAT.")
        
        # Extract VAT.
        self.amount = int(round(self.amount / (1.0 + money.vat)))
        self.is_vat = False
        
        return self
        
#-------------------------------------------------------------------------------
        
    def __add__(self, y):
        """
        Add another money value.
            
        Arguments:
            y -- added money value.
        
        Result:
            New money value.
        """

        if self.is_vat_ctrl:            
            if self.is_vat != y.is_vat:
                raise RuntimeError("VAT flags for added values must be equal.")
                
        return money.from_amount(self.amount + y.amount, self.is_vat)
        
#-------------------------------------------------------------------------------
        
    def __sub__(self, y):
        """
        Sub another money value.
        
        Arguments:
            y -- subtracted money value.
        
        Result:
            New money value.
        """

        if self.is_vat_ctrl:        
            if self.is_vat != y.is_vat:
                raise RuntimeError("VAT flags for sub valus must be equal.")
            
        return money.from_amount(self.amount - y.amount, self.is_vat)
    
#-------------------------------------------------------------------------------
        
    def __mul__(self, y):
        """
        Multiplication on float value.
        
        Arguments:
            y -- multiplication factor.
        
        Result:
            New money value.
        """
        
        return money.from_amount(int(round(self.amount * y)), self.is_vat)
            
#-------------------------------------------------------------------------------
# Calculation tree.
#-------------------------------------------------------------------------------

class calc_tree:
    """
    Calculation tree accumulating money.
    """
    
#-------------------------------------------------------------------------------

    def __init__(self, s):
        """
        Constructor.
        
        Arguments:
            str -- string (node name).
        """
        
        # Init by defaul.
        self.name = s
        self.children = []
        self.money = []

#-------------------------------------------------------------------------------

    def add_child(self, ch):
        """
        Add child to children list.
        
        Arguments:
            ch -- new child.
            
        Result:
            New child.
        """
        
        # Add to the list.
        self.children.append(ch)
        return ch

#-------------------------------------------------------------------------------
        
    def add_money(self, m):
        """
        Add money.
        
        Arguments:
            m -- money.
        """
        
        # Add to the money list.
        self.money.append(m)
    
#-------------------------------------------------------------------------------

    def is_list(self):
        """
        Check if node is list.
        
        Result:
            True -- if node is a list,
            False -- if node is not a list.
        """
        
        return self.children == []

#-------------------------------------------------------------------------------

    def value(self):
        """
        Get node value.
        
        Result:
            Value of the node.
        """
        
        return reduce(lambda x, y: x + y, self.money, money());

#-------------------------------------------------------------------------------

    def calculate(self):
        """
        Calculate money for all nodes in the tree.
        """
    
        if not self.is_list():
            m = money()
            for ch in self.children:
                ch.calculate()
                m = m + ch.value()
            self.money = [m]

#-------------------------------------------------------------------------------
        
    def print(self, indent = 0):
        """
        Print the whole tree.
        
        Arguments:
            indent -- indent of print.
        """
        
        # Indent string.
        if indent == 0:
            indent_string = "#"
        else:
            indent_string = "    " * (indent - 1) + "|--->"         
        
        # Prepare category name.
        cat_name = indent_string + " " + self.name
        
        # Print node as list.
        print("%-96s | %18s" % (cat_name, str(self.value())))
        if not self.is_list():
            for ch in self.children:
                ch.print(indent + 1)
            
        
#-------------------------------------------------------------------------------
# Person.
#-------------------------------------------------------------------------------
         
class person:
    """
    Person with salary and vacation days.
    """

    months = 12               # Months count.
    mean_days_in_month = 29.4 # Mean days count in one month.

#-------------------------------------------------------------------------------

    def __init__(self, salary, vacation = 28):
        """
        Constructor.
        
        Arguments:
            salary -- salary,
            vacation -- vacation days.
        """
            
        self.salary = salary
        self.vaction = vacation
        
#-------------------------------------------------------------------------------

    def year_salary_full(self):
        """
        Get full salary for year.
        
        Result:
            Year salary.
        """
        
        return self.salary * person.months
    
#-------------------------------------------------------------------------------

    def year_salary_add(self):
        """
        Get additional salary for year.
        
        Result:
            Year additional salary.
        """
        
        k = (1.0 / person.months) \
            * (1.0 / person.mean_days_in_month) \
            * self.vaction
        return self.year_salary_full() * k

#-------------------------------------------------------------------------------

    def year_salary_main(self):
        """
        Get main salary for year.
        
        Result:
            Year main salary.
        """
        
        return self.year_salary_full() - self.year_salary_add()

#-------------------------------------------------------------------------------

    def print(self):
        """
        Print information about person.
        """
        
        print("    person : salary = %16s (%16s + %16s), vacation = %2d" \
              % (str(self.year_salary_full()),
                 str(self.year_salary_main()),
                 str(self.year_salary_add()),
                 self.vaction))

#-------------------------------------------------------------------------------
# Persons group.
#-------------------------------------------------------------------------------

class persons_group:
    """
    Group of persons.
    """

#-------------------------------------------------------------------------------

    def __init__(self, name):
        """
        Constructor.
        
        Arguments:
            name -- name of group.
        """
        
        self.name = name
        self.persons = []

#-------------------------------------------------------------------------------

    def add(self, person, count = 1):
        """
        Add person (or several copies of person).
        
        Arguments:
            person -- person,
            count -- copies count of the person.
        
        Result:
            Curent persons count.
        """
        
        # Add persons.
        for i in range(count):
            self.persons.append(person)
        
        return len(self.persons)

#-------------------------------------------------------------------------------

    def year_salary_full(self):
        """
        Get year full salary.
        
        Result:
            Year full salary.
        """
        
        s = money()
        
        for person in self.persons:
            s = s + person.year_salary_full()
            
        return s

#-------------------------------------------------------------------------------

    def year_salary_add(self):
        """
        Get year additional salary.
        
        Result:
            Year adiitional salary.
        """
        
        s = money()
        
        for person in self.persons:
            s = s + person.year_salary_add()
            
        return s

#-------------------------------------------------------------------------------

    def year_salary_main(self):
        """
        Get year main salary.
        
        Result:
            Year main salary.
        """
        
        return self.year_salary_full() - self.year_salary_add()

#-------------------------------------------------------------------------------

    def print(self):
        """
        Print info about group of persons.
        """
        
        print("Group : " + self.name + " (" + \
              str(len(self.persons)) + " persons)")
        
        for person in self.persons:
            person.print()
            
        add = self.year_salary_add()
        main = self.year_salary_main()
        full = self.year_salary_full()
            
        if full.amount != 0:
            print("Total : salary = %17s (%17s + %17s), perc = %2.2f%%" \
                  % (str(full),
                     str(main),
                     str(add),
                     100.0 * add.amount / main.amount))            

#-------------------------------------------------------------------------------



