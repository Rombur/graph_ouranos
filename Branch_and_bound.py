# Python code
# Author: Bruno Turcksin
# Date: 2013-09-24 14:35:13.044256

#----------------------------------------------------------------------------#
## Classes Branch_and_bound and Node                                        ##
#----------------------------------------------------------------------------#

"""This module contains the class Branch_and_bound that solve the SOP using
banch-and-bound algorithm and the class Node that represent the different node
of the graph created by the branch-and-bound algorithm."""

import itertools

class Node(object) :
  """Class representing a node in the tree created by the branch-and-bound
  algorithm."""

  def __init__(self,graph,used_tasks,tasks_ready,min_bound,max_bound) :
    
    super(Node,self).__init__()
    self.graph = graph
    self.used_tasks = used_tasks
    self.tasks_ready = tasks_ready
    self.min_bound = min_bound
    self.max_bound = max_bound

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#

class Branch_and_bound(object) :
  """Class solving the SOP using branch-and-bound algorithm."""

  def __init__(self,tasks,n_processors) :

    super(Branch_and_bound,self).__init__()
    self.tasks = tasks
    self.n_tasks = len(tasks)
    self.n_processors = n_processors

#----------------------------------------------------------------------------#

  def solve(self) :
    """Solve the SOP using branch-and-bound algorithm."""

    subdomains_list = range(1,self.n_processors+1)
    while len(nodes)!=0 :
      lowest_bound = 2*len(self.tasks)
# Best first search
      pos = 0
      counter = 0
      for node in nodes :
        if node.min_bound<lowest_bound :
          pos = counter
        counter += 1

      for i in xrange(1,self.n_processors+1) :
# itertools create a generator, i.e., a list of iterator than can be used only
# once. If we want to reuse the list, we need to recell itertools
        procs_comb = itertools.combinations(subdomains_list,i)
        for used_procs in procs :
          tasks_perm = itertools.permutations(nodes[pos].tasks_ready,i)
          node = create_possible_node(procs_comb,tasks_perm,nodes[pos])
          if node.min_bound!=2*len(self.tasks) :
            nodes.append(node)

# Every possible children from the nodes was created, thus the node itself can
# be deleted.
      nodes.pop(pos)
# Delete all the nodes that have min_bound larger than the smallest max_bound
      min_max_bound = 2*len(self.tasks)
      for node in nodes :
        if node.max_bound<min_max_bound :
          min_max_bound = node.max_bound
      for node in nodes :
        if node.min_bound>min_max_bound :
          nodes.remove(node)
