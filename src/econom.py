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

class Money:
    """
    Peace of money for financial manipulations.
    """
    
    digits_in_group = 3 # Digits count in group when number represented 
                        # as "1 000 000" (three digits in this case).
    delim = " "         # Delimiter for parts of numerical value.
    vat = 0.18          # VAT value.
    is_ctrl_vat = False # Control correct VAT processing.
    
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
            self.init_f(float(v.replace(Money.delim, "")))
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
        self.amount = int(round(v * ut.Consts.HUNDRED))

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
        
        m = Money()
        m.amount = a
        m.is_vat = is_vat
        return m
        
#-------------------------------------------------------------------------------

    def value(self):
        """
        Get float value of money.
        
        Result:
            Value.
        """
        
        return self.amount / ut.Consts.HUNDRED

#-------------------------------------------------------------------------------
        
    def hi(self):
        """
        High part of money (rubles, dollars, etc.).
        
        Result:
            High part of money.
        """
        
        if self.amount < 0:
            return -((-self.amount) // ut.Consts.HUNDRED)
        else:
            return self.amount // ut.Consts.HUNDRED
    
#-------------------------------------------------------------------------------

    def lo(self):
        """
        Low part of money (kopecks, cents, etc.).
        
        Result:
            Low part of money.
        """
        
        if self.amount < 0:
            return (-self.amount) % ut.Consts.HUNDRED
        else:
            return self.amount % ut.Consts.HUNDRED
    
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
        
        chopped = ut.li_chop(str(hi), -3)
        merged = ut.li_merge(chopped, [Money.delim] * (len(chopped) - 1))
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
            ms[i] = Money.from_amount(am, self.is_vat)
            
        # The last element calculate from rest.
        ms[n - 1] = Money.from_amount(rest, self.is_vat)
        
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
        self.amount = int(round((self.amount * (1.0 + Money.vat))))
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
        if self.is_ctrl_vat:
            if not self.is_vat:
                raise RuntimeError("Re-extraction VAT.")
        
        # Extract VAT.
        self.amount = int(round(self.amount / (1.0 + Money.vat)))
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

        if self.is_ctrl_vat:            
            if self.is_vat != y.is_vat:
                raise RuntimeError("VAT flags for added values must be equal.")
                
        return Money.from_amount(self.amount + y.amount, self.is_vat)
        
#-------------------------------------------------------------------------------
        
    def __sub__(self, y):
        """
        Sub another money value.
        
        Arguments:
            y -- subtracted money value.
        
        Result:
            New money value.
        """

        if self.is_ctrl_vat:        
            if self.is_vat != y.is_vat:
                raise RuntimeError("VAT flags for sub valus must be equal.")
            
        return Money.from_amount(self.amount - y.amount, self.is_vat)
    
#-------------------------------------------------------------------------------
        
    def __mul__(self, y):
        """
        Multiplication on float value.
        
        Arguments:
            y -- multiplication factor.
        
        Result:
            New money value.
        """
        
        return Money.from_amount(int(round(self.amount * y)), self.is_vat)
            
#-------------------------------------------------------------------------------
# Calculation tree.
#-------------------------------------------------------------------------------

class CalcTree:
    """
    Calculation tree accumulating money.
    """
    
#-------------------------------------------------------------------------------

    def __init__(self, sname, name = ""):
        """
        Constructor.
        
        Arguments:
            sname -- short name,
            name -- name.
        """
        
        # Init by defaul.
        self.sname = sname
        self.name = name
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

    def find_node(self, sname):
        """
        Find node by string.
        
        Arguments:
            s -- short name.
            
        Result:
            Node found or None.
        """

        # Node is found.
        if self.sname == sname:
            return self
        
        # Find through all children nodes.
        for ch in self.children:
            r = ch.find_node(sname)
            if r != None:
                return r
        
        # Nothing is found.
        return None

#-------------------------------------------------------------------------------

    def value(self):
        """
        Get node value.
        
        Result:
            Value of the node.
        """
        
        return reduce(lambda x, y: x + y, self.money, Money());

#-------------------------------------------------------------------------------

    def calculate(self):
        """
        Calculate money for all nodes in the tree.
        """
    
        if not self.is_list():
            m = Money()
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
        cat_name = indent_string + " " + self.sname + " " + self.name
        
        # Print node as list.
        print("%-101s | %18s" % (cat_name, str(self.value())))
        if not self.is_list():
            for ch in self.children:
                ch.print(indent + 1)
            
        
#-------------------------------------------------------------------------------

    def tree_640():
        """
        Construct tree according to 640-th order.
        
        Result:
            Tree.
        """
        
        t = CalcTree("root 640")

        n_prjam = t.add_child(CalcTree("Прямые затраты"))
        n_prjam.add_child(CalcTree("ОТ1"))
        n_prjam.add_child(CalcTree("МЗ"))
        n_prjam.add_child(CalcTree("АМ1"))
        n_prjam.add_child(CalcTree("ИНЗ"))

        n_obsh = t.add_child(CalcTree("Общехозяйственные затраты"))
        n_obsh.add_child(CalcTree("КУ"))
        n_obsh.add_child(CalcTree("СНИ"))
        n_obsh.add_child(CalcTree("СОЦДИ"))
        n_obsh.add_child(CalcTree("АМ2"))
        n_obsh.add_child(CalcTree("УС"))
        n_obsh.add_child(CalcTree("ТУ"))
        n_obsh.add_child(CalcTree("ОТ2"))
        n_obsh.add_child(CalcTree("ПНЗ"))

        return t;
        
#-------------------------------------------------------------------------------
        
    def tree_200():
        """
        Construct tree according to 200-th order.
        
        Result:
            Tree.
        """
        
        t = CalcTree("root 200")

        # 01
        n01 = t.add_child(CalcTree("01", "Затраты на материалы - всего"))
        n01.add_child(CalcTree("02", "сырье и основные материалы"))
        n01.add_child(CalcTree("03", "вспомогательные материалы"))
        n01.add_child(CalcTree("04", "покупные полуфабрикаты"))
        n01.add_child(CalcTree("05", "возвратные отходы (вычитаются)"))
        n01.add_child(CalcTree("06", "комплектующие изделия"))
        n01.add_child(CalcTree("07", "работы и услуги сторонних организаций производственного характера"))
        n01.add_child(CalcTree("08", "транспортно-заготовительные расходы"))
        n01.add_child(CalcTree("09", "топливо на технологические цели"))
        n01.add_child(CalcTree("10", "энергия на технологические цели"))
        n01.add_child(CalcTree("11", "тара (невозвратная) и упаковка"))

        # 12
        n12 = t.add_child(CalcTree("12", "Затраты на оплату труда основных производственных рабочих - всего"))
        n12.add_child(CalcTree("13", "основная заработная плата"))
        n12.add_child(CalcTree("14", "дополнительная заработная плата"))
        
        # 15
        t.add_child(CalcTree("15", "Страховые взносы на обязательное социальное страхование"))

        # 16
        n16 = t.add_child(CalcTree("16", "Затраты на подготовку и освоение производства - всего"))
        n16.add_child(CalcTree("17", "затраты на подготовку и освоение новых производств, цехов и агрегатов (пусковые расходы)"))
        n16.add_child(CalcTree("18", "затраты на подготовку и освоение новых видов продукции и новых технологических процессов"))

        # Other.
        t.add_child(CalcTree("19", "Затраты на специальную технологическую оснастку"))
        t.add_child(CalcTree("20", "Специальные затраты"))
        t.add_child(CalcTree("21", "Общепроизводственные затраты"))
        t.add_child(CalcTree("22", "Общехозяйственные затраты"))
        t.add_child(CalcTree("23", "Прочие производственные затраты"))

        return t;        
    
#-------------------------------------------------------------------------------
        
    def tree_640_200():
        """
        Construct tree according to 640-th order with special
        positions from 200-th order.
        
        Result:
            Tree.
        """
        
        t = CalcTree("root 640/200")

        n_prjam = t.add_child(CalcTree("Прямые затраты"))
        n_OT1 = n_prjam.add_child(CalcTree("ОТ1"))
        n_OT1.add_child(CalcTree("ОТ1О"))
        n_OT1.add_child(CalcTree("ОТ1Д"))
        n_OT1.add_child(CalcTree("ОТ1С"))
        n_MZ = n_prjam.add_child(CalcTree("МЗ"))
        n_MZ.add_child(CalcTree("МЗЭ"))
        n_prjam.add_child(CalcTree("АМ1"))
        n_INZ = n_prjam.add_child(CalcTree("ИНЗ"))
        n_INZO = n_INZ.add_child(CalcTree("ИНЗО"))
        n_INZO.add_child(CalcTree("ИНЗОВ"))
        n_INZO.add_child(CalcTree("ИНЗОХ"))
        n_INZO.add_child(CalcTree("ИНЗОИ"))
        n_INZO.add_child(CalcTree("ИНЗОТ"))
        n_INZO.add_child(CalcTree("ИНЗОС"))

        n_obsh = t.add_child(CalcTree("Общехозяйственные затраты"))
        n_obsh.add_child(CalcTree("КУ"))
        n_obsh.add_child(CalcTree("СНИ"))
        n_obsh.add_child(CalcTree("СОЦДИ"))
        n_obsh.add_child(CalcTree("АМ2"))
        n_obsh.add_child(CalcTree("УС"))
        n_obsh.add_child(CalcTree("ТУ"))
        n_obsh.add_child(CalcTree("ОТ2"))
        n_obsh.add_child(CalcTree("ПНЗ"))
        
        return t;
            
#-------------------------------------------------------------------------------
# Person.
#-------------------------------------------------------------------------------
         
class Person:
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
        
        return self.salary * Person.months
    
#-------------------------------------------------------------------------------

    def year_salary_add(self):
        """
        Get additional salary for year.
        
        Result:
            Year additional salary.
        """
        
        k = (1.0 / Person.months) \
            * (1.0 / Person.mean_days_in_month) \
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
        
        print("    Person : salary = %16s (%16s + %16s), vacation = %2d" \
              % (str(self.year_salary_full()),
                 str(self.year_salary_main()),
                 str(self.year_salary_add()),
                 self.vaction))

#-------------------------------------------------------------------------------
# Persons group.
#-------------------------------------------------------------------------------

class PersonsGroup:
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
        
        s = Money()
        
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
        
        s = Money()
        
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
