# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 11:49:25 2018

@author: Rybakov
"""

from functools import reduce
import utils as ut
import jdfun

#-------------------------------------------------------------------------------
# Microprocessor.
#-------------------------------------------------------------------------------
            
class CPU:
    """
    Microprocessor.
    """            
    
#-------------------------------------------------------------------------------

    def __init__(self, name, cores_count, freq, tfs, is_acc = False):
        """
        Constructor.
        
        Arguments:
            name -- name,
            cores_count -- cores count,
            freq -- frequency (GHz),
            tfs -- peak performance (TFLOPS),
            is_acc -- check if CPU is an accelerator.
        """
        
        self.name = name
        self.cores_count = cores_count
        self.freq = freq
        self.tfs = tfs
        self.is_acc = is_acc
    
#-------------------------------------------------------------------------------

    def copy(self):
        """
        Copy.
        
        Result:
            Copy.
        """
        
        return CPU(name = self.name, 
                   cores_count = self.cores_count, 
                   freq = self.freq, 
                   tfs = self.tfs, 
                   is_acc = self.is_acc)

#-------------------------------------------------------------------------------

    def __repr__(self):
        """
        String representation.
        
        Result:
            String.
        """
        
        return self.name \
               + "/c" + str(self.cores_count) \
               + "/f" + str(self.freq) \
               + "/t" + str(self.tfs)

#-------------------------------------------------------------------------------

    def Intel_Xeon_E5450():
        """
        Harpertown microprocessor (Intel Xeon E5450).
        
        Result:
            Harpertown microprocessor.
        """
        
        return CPU("Intel Xeon E5450 Harpertown",
                   cores_count = 4, freq = 3.0, tfs = 0.048)

#-------------------------------------------------------------------------------

    def Intel_Xeon_E5_2667():
        """
        Ivy Bridge microprocessor (Intel Xeon E5-2667).
        
        Result:
            Ivy Bridge microprocessor.
        """
        
        return CPU("Intel Xeon E5-2667 Ivy Bridge",
                   cores_count = 8, freq = 3.3, tfs = 0.2112)

#-------------------------------------------------------------------------------

    def Intel_Xeon_Phi_7120D():
        """
        Knights Corner microprocessor in Petastream (Intel Xeon Phi 7120D).
        
        Result:
            Knights Corner microprocessor.
        """
        
        return CPU("Intel Xeon Phi 7120D KNC",
                   cores_count = 61, freq = 1.238, tfs = 1.208,
                   is_acc = True)

#-------------------------------------------------------------------------------

    def Intel_Xeon_E5_2690():
        """
        Sandy Bridge microprocessor (Intel Xeon E5-2690).
        
        Result:
            Sandy Bridge microprocessor.
        """
        
        return CPU("Intel Xeon E5-2690 Sandy Bridge",
                   cores_count = 8, freq = 2.9, tfs = 0.1856)

#-------------------------------------------------------------------------------

    def Intel_Xeon_Phi_7110X():
        """
        Knights Corner microprocessor in Tornado (Intel Xeon Phi 7110X).
        
        Result:
            Knights Corner microprocessor.
        """
        
        return CPU("Intel Xeon Phi 7110X KNC",
                   cores_count = 61, freq = 1.1, tfs = 1.0736,
                   is_acc = True)

#-------------------------------------------------------------------------------

    def Intel_Xeon_E5_2697v3():
        """
        Haswell microprocessor (Intel Xeon E5-2697v3).
        
        Result:
            Haswell microprocessor.
        """
        
        return CPU("Intel Xeon E5-2697v3 Haswell",
                   cores_count = 14, freq = 2.6, tfs = 0.5824)

#-------------------------------------------------------------------------------

    def Intel_Xeon_E5_2697Av4():
        """
        Broadwell microprocessor (Intel Xeon E5-2697Av4).
        
        Result:
            Broadwell microprocessor.
        """
        
        return CPU("Intel Xeon E5-2697Av4 Broadwell",
                   cores_count = 16, freq = 2.6, tfs = 0.6656)
    
#-------------------------------------------------------------------------------

    def Intel_Xeon_Phi_7290():
        """
        Knights Landing microprocessor (Intel Xeon Phi 7290).
        
        Result:
            Knights Landing microprocessor.
        """
        
        return CPU("Intel Xeon Phi 7290 KNL",
                   cores_count = 72, freq = 1.5, tfs = 3.456)

#-------------------------------------------------------------------------------

    def Intel_Xeon_X5675():
        """
        Westmere microprocessor (Intel Xeon X5675).
        
        Result:
            Westmere microprocessor.
        """
        
        return CPU("Intel Xeon X5675 Westmere",
                   cores_count = 6, freq = 3.06, tfs = 0.14488)

#-------------------------------------------------------------------------------

    def NVIDIA_Tesla_M2090():
        """
        Tesla microprocessor (NVIDIA Tesla M2090).
        
        Result:
            Tesla microprocessor.
        """
        
        return CPU("NVIDIA Tesla M2090",
                   cores_count = 512, freq = 1.3, tfs = 0.665,
                   is_acc = True)
    
#-------------------------------------------------------------------------------

    def single_property(self, cpu_fun):
        """
        Single property.
        
        Arguments:
            cpu_fun -- function for process CPU level.
            
        Result:
            Single property.
        """
        
        # Only possible case is cpu_fun != None.        
        return cpu_fun(self)
    
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
            cpus -- cpus (list of tuples) with RAM
                [(cpu1, count1, ram1), (cpu2, count2, ram2), ...].
        """
        
        self.name = name
        self.cpus = cpus

#-------------------------------------------------------------------------------

    def copy(self):
        """
        Copy.
        
        Result:
            Copy.
        """

        copy_cpu_tuple_fun = lambda x: (x[0].copy(), x[1], x[2])
        return Node(name = self.name,
                    cpus = [copy_cpu_tuple_fun(x) for x in self.cpus])

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

    def properties_tree(self,
                        node_fun = None,
                        cpu_tuple_fun = None,
                        cpu_fun = None):
        """
        Get properties tree (nested array).
        
        Arguments:
            node_fun -- function for process node,
            cpu_tuple_fun -- function for process cpu tuple,
            cpu_fun -- function for process cpu.
            
        Result:
            Properties tree.
        """
        
        # Simple characteristic of node.              
        if node_fun != None:
            return node_fun(self)
        
        # Check for cpu_tuple function.
        if cpu_tuple_fun != None:
            return list(map(cpu_tuple_fun, self.cpus))
        
        # Generate properties trees for all cpus.
        fun = lambda x: x[0].single_property(cpu_fun)
        return [fun(x) for x in self.cpus]

#-------------------------------------------------------------------------------

    def filter(self,
               cpu_tuple_filter = jdfun.true_predct(),
               cpu_filter = jdfun.true_predct()):
        """
        Filter function for segment.
        
        Arguments:
            node_tuple_filter -- filter for node tuple,
            node_filter -- function for nodes filter.
            
        Result:
            New node object.
        """
        
        r = self.copy()
        
        # Final filter.
        fun = lambda x: x[1] > 0 \
                        and cpu_tuple_filter(x) \
                        and cpu_filter(x[0])
        r.cpus = list(filter(fun, r.cpus))
        
        return r

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
            nodes -- nodes (list of tuples)
                [(node1, count1), (node2, count2), ...],
            watts -- power,
            pue -- power usage effectiveness.
        """

        self.name = name
        self.nodes = nodes
        self.watts = watts
        self.pue = pue
        
#-------------------------------------------------------------------------------

    def copy(self):
        """
        Copy.
        
        Result:
            Copy.
        """
        
        copy_node_tuple_fun = lambda x: (x[0].copy(), x[1])
        return Segment(name = self.name,
                       nodes = [copy_node_tuple_fun(x) for x in self.nodes],
                       watts = self.watts,
                       pue = self.pue)

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

    def properties_tree(self,
                        segment_fun = None,
                        node_tuple_fun = None,
                        node_fun = None,
                        cpu_tuple_fun = None,
                        cpu_fun = None):
        """
        Get properties tree (nested array).
        
        Arguments:
            segment_fun -- function for proceess segment,
            node_tuple_fun -- function for process (node, ...) tuple,
            node_fun -- function for process node,
            cpu_tuple_fun -- function for process (cpu, ...) tuple,
            cpu_fun -- function for process cpu.
            
        Result:
            Properties tree.
        """
        
        # Simple characteristic of segment.              
        if segment_fun != None:
            return segment_fun(self)
        
        # Check node_tuple_fun.
        if node_tuple_fun != None:
            return list(map(node_tuple_fun, self.nodes))
        
        # Generate properties trees for all nodes.
        fun = lambda x: x[0].properties_tree(node_fun,
                                             cpu_tuple_fun,
                                             cpu_fun)
        return [fun(x) for x in self.nodes]

#-------------------------------------------------------------------------------    

    def filter(self,
               node_tuple_filter = jdfun.true_predct(),
               node_filter = jdfun.true_predct(),
               cpu_tuple_filter = jdfun.true_predct(),
               cpu_filter = jdfun.true_predct()):
        """
        Filter function for segment.
        
        Arguments:
            node_tuple_filter -- filter for node tuple,
            node_filter -- function for nodes filter,
            cpu_tuple_filter -- filter for CPU tuple,
            cpu_filter -- function for CPUs filter.
            
        Result:
            New node object.
        """

        r = self.copy()

        # Filter from leafs.
        fun = lambda x: (x[0].filter(cpu_tuple_filter, cpu_filter), x[1])
        r.nodes = [fun(x) for x in r.nodes]

        # Final filter.
        fun = lambda x: x[0].cpus != [] \
                        and x[1] > 0 \
                        and node_tuple_filter(x) \
                        and node_filter(x[0])
        r.nodes = list(filter(fun, r.nodes))

        return r
        
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
                [segment1, segment1, ...].
        """
        
        self.name = name
        self.segments = segments

#-------------------------------------------------------------------------------

    def copy(self):
        """
        Copy.
        
        Result:
            Copy.
        """

        return Resources(name = self.name,
                         segments = [x.copy() for x in self.segments])

#-------------------------------------------------------------------------------

    def JSCC():
        """
        Joint supercomputer center supercomputers.
        
        Result:
            Supercomputers of Joint supercomputer center.
        """
        
        return Resources \
        (
            name = "JSCC",
            segments =
            [
                Segment
                (
                    name = "100K",
                    nodes =
                    [
                        (
                            Node
                            (
                                name = "100K",
                                cpus =
                                [
                                    (CPU.Intel_Xeon_E5450(), 2, 8)
                                ]
                            ),
                            110
                        )
                    ],
                    watts = 36, pue = 2.0
                ),
                Segment
                (
                    name = "Petastream",
                    nodes =
                    [
                        (
                            Node
                            (
                                name = "Petastream",
                                cpus =
                                [
                                    (CPU.Intel_Xeon_E5_2667(), 1, 8),
                                    (CPU.Intel_Xeon_Phi_7120D(), 8, 16)
                                ]
                            ),
                            8
                        )
                    ],
                    watts = 15, pue = 1.25
                ),
                Segment
                (
                    name = "Tornado",
                    nodes =
                    [
                        (
                            Node
                            (
                                name = "Tornado",
                                cpus =
                                [
                                    (CPU.Intel_Xeon_E5_2690(), 2, 64),
                                    (CPU.Intel_Xeon_Phi_7110X(), 2, 16)
                                ]
                            ),
                            207
                        )
                    ],
                    watts = 223, pue = 1.25
                ),
                Segment
                (
                    name = "Haswell",
                    nodes =
                    [
                        (
                            Node
                            (
                                name = "Haswell",
                                cpus =
                                [
                                    (CPU.Intel_Xeon_E5_2697v3(), 2, 128)
                                ]
                            ),
                            42
                        )
                    ],
                    watts = 28, pue = 1.06
                ),
                Segment
                (
                    name = "Broadwell",
                    nodes = 
                    [
                        (
                            Node
                            (
                                name = "Broadwell",
                                cpus =
                                [
                                    (CPU.Intel_Xeon_E5_2697Av4(), 2, 128)
                                ]
                            ),
                            136
                        )
                    ],
                    watts = 91, pue = 1.06
                ),
                Segment
                (
                    name = "KNL",
                    nodes =
                    [
                        (
                            Node
                            (
                                name = "KNL",
                                cpus =
                                [
                                    (CPU.Intel_Xeon_Phi_7290(), 1, 96)
                                ]
                            ),
                            38
                        )
                    ],
                    watts = 29, pue = 1.06
                ),
                Segment
                (
                    name = "NVIDIA",
                    nodes =
                    [
                        (
                            Node
                            (
                                name = "NVIDIA",
                                cpus =
                                [
                                    (CPU.Intel_Xeon_X5675(), 2, 192),
                                    (CPU.NVIDIA_Tesla_M2090(), 8, 48)
                                ]
                            ),
                            6
                        )
                    ],
                    watts = 19, pue = 2.0
                )
            ]
        )

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

    def properties_tree(self,
                        resources_fun = None,
                        segment_fun = None,
                        node_tuple_fun = None,
                        node_fun = None,
                        cpu_tuple_fun = None,
                        cpu_fun = None):
        """
        Get properties tree (nested array).
        
        Arguments:
            resources_fun -- function for process resources,
            segment_fun -- function for proceess segment,
            node_tuple_fun -- fucntion for process (node, ...) tuple,
            node_fun -- function for process node level,
            cpu_tuple_fun -- function for process (cpu, ...) tuple,
            cpu_fun -- function for process cpu level.
            
        Result:
            Properties tree.
        """
        
        # Simple characteristic of resources.              
        if resources_fun != None:
            return resources_fun(self)
        
        # Generate properties tries for all segments.
        fun = lambda x: x.properties_tree(segment_fun,
                                          node_tuple_fun,
                                          node_fun,
                                          cpu_tuple_fun,
                                          cpu_fun)
        return [fun(x) for x in self.segments]

#-------------------------------------------------------------------------------

    def pt_cpu_mark(self):
        """
        CPUs marks.
        
        Result:
            CPUs marks.
        """
        
        return self.properties_tree(cpu_fun = lambda x: 1) 

#-------------------------------------------------------------------------------

    def pt_node_mark(self):
        """
        Nodes marks.
        
        Result:
            Nodes marks.
        """
        
        return self.properties_tree(node_fun = lambda x: 1)

#-------------------------------------------------------------------------------

    def pt_segment_mark(self):
        """
        Segments marks.
        
        Result:
            Segments marks.
        """
        
        return self.properties_tree(segment_fun = lambda x: 1)

#-------------------------------------------------------------------------------

    def pt_cpu_cores_count(self):
        """
        Properties tree on cpu cores count.
        
        Result:
            Propertie tree on cpu cores count.
        """
        
        return self.properties_tree(cpu_fun = lambda x: x.cores_count)
        
#-------------------------------------------------------------------------------

    def pt_cpu_freq(self):
        """
        Properties tree on cpu frequency.
        
        Result:
            Propertie tree on cpu frequency.
        """
        
        return self.properties_tree(cpu_fun = lambda x: x.freq)
        
#-------------------------------------------------------------------------------

    def pt_cpu_tfs(self):
        """
        Properties tree on cpu TFLOPS.
        
        Result:
            Propertie tree on cpu TFLOPS.
        """
        
        return self.properties_tree(cpu_fun = lambda x: x.tfs)

#-------------------------------------------------------------------------------

    def pt_cpu_core_tfs(self):
        """
        CPU core TFLOPS properties tree.
        
        Result:
            CPU core TFLOPS properties tree.
        """
        
        return jdfun.zip_div(self.pt_cpu_tfs(), self.pt_cpu_cores_count())
        
#-------------------------------------------------------------------------------

    def pt_node_cpus_count_m(self):
        """
        Properties tree on node cpus count.
        
        Result:
            Properties tree on node cpus count.
        """
        
        return self.properties_tree(cpu_tuple_fun = lambda x: x[1])

#-------------------------------------------------------------------------------

    def pt_node_cpus_count(self):
        """
        CPUs count property tree.
        
        Result:
            CPUscount property tree.
        """
        
        return jdfun.reduce_leafs_sum(self.pt_node_cpus_count_m())

#-------------------------------------------------------------------------------

    def pt_node_cores_count_m(self):
        """
        Properties tree on node cores count.
        
        Result:
            Properties tree on node cores count.
        """
        
        return jdfun.zip_mul(self.pt_cpu_cores_count(),
                             self.pt_node_cpus_count_m())

#-------------------------------------------------------------------------------

    def pt_node_cores_count(self):
        """
        Node cores count properties tree.
        
        Result:
            Node cores count properties tree.
        """
        
        return jdfun.reduce_leafs_sum(self.pt_node_cores_count_m())

#-------------------------------------------------------------------------------

    def pt_node_tfs_m(self):
        """
        Properties tree on node cpus TFLOPS.
        
        Result:
            Properties tree on node cpus TFLOPS.
        """
        
        return jdfun.zip_mul(self.pt_cpu_tfs(), self.pt_node_cpus_count_m())

#-------------------------------------------------------------------------------

    def pt_node_tfs(self):
        """
        Node TFLOPS properties tree.
        
        Result:
            Node FLOPS properties tree.
        """
        
        return jdfun.reduce_leafs_sum(self.pt_node_tfs_m())

#-------------------------------------------------------------------------------

    def pt_node_ram_m(self):
        """
        Node cpus RAMs properties tree.
        
        Result:
            Node cpus RAMs properties tree.
        """
        
        return self.properties_tree(cpu_tuple_fun = lambda x: x[2])

#-------------------------------------------------------------------------------

    def pt_node_ram(self):
        """
        Node RAM properties tree.
        
        Result:
            Node RAM property tree.
        """
        
        return jdfun.reduce_leafs_sum(self.pt_node_ram_m())

#-------------------------------------------------------------------------------
        
    def pt_segment_nodes_count_m(self):
        """
        Properties tree on segment nodes count.
        
        Result:
            Properties tree on segment nodes count.
        """
        
        return self.properties_tree(node_tuple_fun = lambda x: x[1])

#-------------------------------------------------------------------------------

    def pt_segment_nodes_count(self):
        """
        Segment nodes counts properties tree.
        
        Result:
            Segment nodes counts properties tree.
        """
        
        return jdfun.reduce_leafs_sum(self.pt_segment_nodes_count_m())

#-------------------------------------------------------------------------------

    def pt_segment_cpus_count_m(self):
        """
        Segment CPUs count properties tree.
        
        Result:
            Segment CPUs count properties tree.
        """
        
        return jdfun.zip_mul(self.pt_node_cpus_count(),
                             self.pt_segment_nodes_count_m())
        
#-------------------------------------------------------------------------------
        
    def pt_segment_cpus_count(self):
        """
        Segment CPU count properties tree.
        
        Result:
            Segment CPU count properties tree.
        """
        
        return jdfun.reduce_leafs_sum(self.pt_segment_cpus_count_m())
        
#-------------------------------------------------------------------------------

    def pt_segment_cores_count_m(self):
        """
        Segment cores count properties tree.
        
        Result:
            Segment cores count properties tree.
        """
        
        return jdfun.zip_mul(self.pt_node_cores_count(),
                             self.pt_segment_nodes_count_m())
        
#-------------------------------------------------------------------------------
        
    def pt_segment_cores_count(self):
        """
        Segment cores count properties tree.
        
        Result:
            Segment cores count properties tree.
        """
        
        return jdfun.reduce_leafs_sum(self.pt_segment_cores_count_m())
        
#-------------------------------------------------------------------------------

    def pt_segment_tfs_m(self):
        """
        Segment TFLOPS properties tree.
        
        Result:
            Segment TFLOPS properties tree.
        """

        return jdfun.zip_mul(self.pt_node_tfs(), self.pt_segment_nodes_count_m())

#-------------------------------------------------------------------------------

    def pt_segment_tfs(self):
        """
        Segment TFLOPS properties tree.
        
        Result:
            Segment TFLOPS properties tree.
        """
        
        return jdfun.reduce_leafs_sum(self.pt_segment_tfs_m())

#-------------------------------------------------------------------------------
        
    def pt_segment_ram_m(self):
        """
        Segment RAMs properties tree.
        
        Result:
            Segment RAMs properties tree.
        """
        
        return jdfun.zip_mul(self.pt_node_ram(),
                             self.pt_segment_nodes_count_m())
    
#-------------------------------------------------------------------------------    

    def pt_segment_ram(self):
        """
        Segment RAM properties tree.
        
        Result:
            Segment RAM properties tree.
        """
        
        return jdfun.reduce_leafs_sum(self.pt_segment_ram_m())

#-------------------------------------------------------------------------------

    def tfs(self):
        """
        Resources tfs.
        
        Result:
            Resources TFLOPS.
        """
        
        return jdfun.reduce_leafs_sum(self.pt_segment_tfs())
        
#-------------------------------------------------------------------------------

    def ram(self):
        """
        RAM.
        
        Result:
            RAM.
        """
        
        return jdfun.reduce_leafs_sum(self.pt_segment_ram())
        
#-------------------------------------------------------------------------------

    def nodes_count(self):
        """
        Nodes count.
        
        Result:
            Nodes count.
        """
        
        return jdfun.reduce_leafs_sum(self.pt_segment_nodes_count())

#-------------------------------------------------------------------------------

    def cpus_count(self):
        """
        CPUs count.
        
        Result:
            CPUs count.
        """
        
        return jdfun.reduce_leafs_sum(self.pt_segment_cpus_count())
    
#-------------------------------------------------------------------------------

    def cores_count(self):
        """
        Cores count.
        
        Result:
            Cores count.
        """

        return jdfun.reduce_leafs_sum(self.pt_segment_cores_count())    
    
#-------------------------------------------------------------------------------

    def filter(self,
               segment_filter = jdfun.true_predct(),
               node_tuple_filter = jdfun.true_predct(),
               node_filter = jdfun.true_predct(),
               cpu_tuple_filter = jdfun.true_predct(),
               cpu_filter = jdfun.true_predct()):
        """
        Filter function for resources.
        
        Arguments:
            segment_filter -- function for segments filter,
            node_tuple_filter -- filter for node tuple,
            node_filter -- function for nodes filter,
            cpu_tuple_filter -- filter for CPU tuple,
            cpu_filter -- function for CPUs filter.
            
        Result:
            New resources object.
        """
        
        r = self.copy()
        
        # Filter from leafs.
        fun = lambda x: x.filter(node_tuple_filter,
                                 node_filter,
                                 cpu_tuple_filter,
                                 cpu_filter)
        r.segments = [fun(x) for x in r.segments]
        
        # Final filter.
        fun = lambda x: (x.nodes != []) and segment_filter(x)
        r.segments = list(filter(fun, r.segments))
        
        return r

#-------------------------------------------------------------------------------        