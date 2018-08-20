# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 11:49:25 2018

@author: Rybakov
"""

from functools import reduce

#-------------------------------------------------------------------------------
# Microprocessor.
#-------------------------------------------------------------------------------
            
class CPU:
    """
    Microprocessor.
    """            
    
#-------------------------------------------------------------------------------

    def __init__(self, name, cores, freq, tfs):
        """
        Constructor.
        
        Arguments:
            name -- name,
            cores -- cores count,
            freq -- frequency (GHz),
            tfs -- peak performance (TFLOPS).
        """
        
        self.name = name
        self.cores = cores
        self.freq = freq
        self.tfs = tfs
    
#-------------------------------------------------------------------------------

    def __repr__(self):
        """
        String representation.
        
        Result:
            String.
        """
        
        return self.name \
               + "/c" + str(self.cores) \
               + "/f" + str(self.freq) \
               + "/t" + str(self.tfs)

#-------------------------------------------------------------------------------

    def HT():
        """
        Harpertown microprocessor (Intel Xeon E5450).
        
        Result:
            Harpertown microprocessor.
        """
        
        return CPU("HT", cores = 4, freq = 3.0, tfs = 0.048)

#-------------------------------------------------------------------------------

    def IB():
        """
        Ivy Bridge microprocessor (Intel Xeon E5-2667).
        
        Result:
            Ivy Bridge microprocessor.
        """
        
        return CPU("IB", cores = 8, freq = 3.3, tfs = 0.2112)

#-------------------------------------------------------------------------------

    def KNC_ps():
        """
        Knights Corner microprocessor in Petastream (Intel Xeon Phi 7120D).
        
        Result:
            Knights Corner microprocessor.
        """
        
        return CPU("KNC", cores = 61, freq = 1.238, tfs = 1.208)

#-------------------------------------------------------------------------------

    def SB():
        """
        Sandy Bridge microprocessor (Intel Xeon E5-2690).
        
        Result:
            Sandy Bridge microprocessor.
        """
        
        return CPU("SB", cores = 8, freq = 2.9, tfs = 0.1856)

#-------------------------------------------------------------------------------

    def KNC_tr():
        """
        Knights Corner microprocessor in Tornado (Intel Xeon Phi 7110X).
        
        Result:
            Knights Corner microprocessor.
        """
        
        return CPU("KNC", cores = 61, freq = 1.1, tfs = 1.0736)

#-------------------------------------------------------------------------------

    def HW():
        """
        Haswell microprocessor (Intel Xeon E5-2697v3).
        
        Result:
            Haswell microprocessor.
        """
        
        return CPU("HW", cores = 14, freq = 2.6, tfs = 0.5824)

#-------------------------------------------------------------------------------

    def BW():
        """
        Broadwell microprocessor (Intel Xeon E5-2697Av4).
        
        Result:
            Broadwell microprocessor.
        """
        
        return CPU("BW", cores =16, freq = 2.6, tfs = 0.6656)
    
#-------------------------------------------------------------------------------

    def KNL():
        """
        Knights Landing microprocessor (Intel Xeon Phi 7290).
        
        Result:
            Knights Landing microprocessor.
        """
        
        return CPU("KNL", cores = 72, freq = 1.5, tfs = 3.456)

#-------------------------------------------------------------------------------

    def WM():
        """
        Westmere microprocessor (Intel Xeon X5675).
        
        Result:
            Westmere microprocessor.
        """
        
        return CPU("WM", cores = 6, freq = 3.06, tfs = 0.14488)

#-------------------------------------------------------------------------------

    def Tesla():
        """
        Tesla microprocessor (NVIDIA Tesla M2090).
        
        Result:
            Tesla microprocessor.
        """
        
        return CPU("TL", cores = 512, freq = 1.3, tfs = 0.665)
    
#-------------------------------------------------------------------------------
# Segment.
#-------------------------------------------------------------------------------
        
class Node:
    """
    Supercomputer node.
    """
        
#-------------------------------------------------------------------------------

    def __init__(self, name, cpus):
        """
        Constructor.
        
        Arguments:
            name -- name of node,
            cpus -- cpus (list of tuples) with RAM.
                [(cpu1, count1, ram1), (cpu2, count2, ram2), ...]
        """
        
        self.name = name
        self.cpus = cpus

#-------------------------------------------------------------------------------

    def MVS100K():
        """
        MVS-100K node.
        
        Result:
            MVS-100K node.
        """
        
        return Node("100K",
                    cpus = [(CPU.HT(), 2, 8)])

#-------------------------------------------------------------------------------

    def Petastream():
        """
        Petastream node.
        
        Result:
            Petastream node.
        """
        
        return Node("Petastream",
                    cpus = [(CPU.IB(), 1, 8), (CPU.KNC_ps(), 8, 16)])
    
#-------------------------------------------------------------------------------

    def Tornado():
        """
        Tornado node.
        
        Result:
            Tornado node.
        """
        
        return Node("Tornado",
                    cpus = [(CPU.SB(), 2, 64), (CPU.KNC_tr(), 2, 16)])

#-------------------------------------------------------------------------------

    def Haswell():
        """
        Haswell node.
        
        Result:
            Haswell node.
        """
        
        return Node("Haswell",
                    cpus = [(CPU.HW(), 2, 128)])

#-------------------------------------------------------------------------------

    def Broadwell():
        """
        Broadwell node,
        
        Result:
            Broadwell node.
        """
        
        return Node("Broadwell",
                    cpus = [(CPU.BW(), 2, 128)])

#-------------------------------------------------------------------------------

    def KNL():
        """
        KNL node.
        
        Result:
            KNL node.
        """
        
        return Node("KNL",
                    cpus = [(CPU.KNL(), 1, 96)])

#-------------------------------------------------------------------------------

    def NVIDIA():
        """
        NVIDIA node.
        
        Result:
            NVIDIA node.
        """
        
        return Node("NVIDIA",
                    cpus = [(CPU.WM(), 2, 192), (CPU.Tesla(), 8, 48)])

#-------------------------------------------------------------------------------

    def __repr__(self):
        """
        String representation.
        
        Result:
            String representation.
        """
        
        r = "N. " + self.name + " : ["
        
        for c in self.cpus:
            (cpu, cpu_count, ram) = c
            r += str(cpu_count) + "x " + str(cpu) + ", " + str(ram) + "GB; "
          
        # Delete last coma.
        if self.cpus != []:
            r = r[:-2]
            
        return r + "]"

#-------------------------------------------------------------------------------    
# Segment.
#-------------------------------------------------------------------------------

class Segment:
    """
    Supercomputer segment.
    """
    
#-------------------------------------------------------------------------------

    def __init__(self, name, nodes, watts, pue):
        """
        Constructor.
        
        Arguments:
            name -- name,
            nodes -- nodes (list of tuples).
                [(node1, count1), (node2, count2), ...],
            watts -- power,
            pue -- power usage effectiveness
        """

        self.name = name
        self.nodes = nodes
        self.watts = watts
        self.pue = pue
        
#-------------------------------------------------------------------------------

    def MVS100K():
        """
        MVS-100K segment.
        
        Result:
            MVS-100K segment.
        """
        
        return Segment("100K",
                       nodes = [(Node.MVS100K(), 110)],
                       watts = 36,
                       pue = 2.0)

#-------------------------------------------------------------------------------

    def Petastream():
        """
        Petastream segment.
        
        Result:
            Petastream segment.
        """
        
        return Segment("Petastream",
                       nodes = [(Node.Petastream(), 8)],
                       watts = 15,
                       pue = 1.25)
    
#-------------------------------------------------------------------------------

    def Tornado():
        """
        Tornado segment.
        
        Result:
            Tornado segment.
        """
        
        return Segment("Tornado",
                       nodes = [(Node.Tornado(), 207)],
                       watts = 223,
                       pue = 1.25)

#-------------------------------------------------------------------------------

    def Haswell():
        """
        Haswell segment.
        
        Result:
            Haswell segment.
        """
        
        return Segment("Haswell",
                       nodes = [(Node.Haswell(), 42)],
                       watts = 28,
                       pue = 1.06)

#-------------------------------------------------------------------------------

    def Broadwell():
        """
        Broadwell segment,
        
        Result:
            Broadwell segment.
        """
        
        return Segment("Broadwell",
                       nodes = [(Node.Broadwell(), 136)],
                       watts = 91,
                       pue = 1.06)

#-------------------------------------------------------------------------------

    def KNL():
        """
        KNL segment.
        
        Result:
            KNL segment.
        """
        
        return Segment("KNL",
                       nodes = [(Node.KNL(), 38)],
                       watts = 29,
                       pue = 1.06)

#-------------------------------------------------------------------------------

    def NVIDIA():
        """
        NVIDIA segment.
        
        Result:
            NVIDIA segment.
        """
        
        return Segment("NVIDIA",
                       nodes = [(Node.NVIDIA(), 6)],
                       watts = 19,
                       pue = 2.0)

#-------------------------------------------------------------------------------

    def __repr__(self):
        """
        String representation.
        
        Result:
            String representation.
        """
        
        r = "S. " + self.name + " : ["
        
        for c in self.nodes:
            r += str(c) + ", "
          
        # Delete last coma.
        if self.nodes != []:
            r = r[:-2]
            
        return r + "], w/p = " + str(self.watts) + "/" + str(self.pue)

#-------------------------------------------------------------------------------   
# Supercpmputer resources. 
#-------------------------------------------------------------------------------

class Resources:
    """
    Supercomputer resources.
    """

#-------------------------------------------------------------------------------

    def __init__(self, name, segments):
        """
        Constructor.
        
        Arguments:
            name -- name of resources,
            segments -- list of segments
        """
        
        self.name = name
        self.segments = segments

#-------------------------------------------------------------------------------

    def JSCC():
        """
        Joint supercomputer center supercomputers.
        
        Result:
            Supercomputers of Joint supercomputer center.
        """
        
        return Resources("JSCC",
                         [Segment.MVS100K(),
                          Segment.Petastream(),
                          Segment.Tornado(),
                          Segment.Haswell(),
                          Segment.Broadwell(),
                          Segment.KNL(),
                          Segment.NVIDIA()])

#-------------------------------------------------------------------------------

    def __repr__(self):
        """
        String representation.
        
        Result:
            String representation.
        """
        
        return reduce(lambda x, y: x + str(y) + "\n",
                      self.segments,
                      "# " + self.name + " #\n")
    
#-------------------------------------------------------------------------------

