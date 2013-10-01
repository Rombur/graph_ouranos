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

  def __init__(self,graph,tasks_done,tasks_ready,cost,min_bound,max_bound) :
    
    super(Node,self).__init__()
    self.graph = graph
    self.tasks_done = tasks_done
    self.tasks_ready = tasks_ready
    self.cost = cost
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

  def create_node(self,given_procs,given_tasks,parent_node) :
    """Create a new node given a processor combination, a task permutation,
    and a node."""

    n_tasks = len(given_tasks)
    used_procs = set()
    for task in given_tasks :
      if task.subdomain_id in given_procs and\
          task.subdomain_id not in used_procs:
            n_tasks -= 1
            used_procs.add(task.subdomain_id)
    
    if n_tasks==0 :
      new_graph = parent_node.graph[:]
      new_tasks_done = parent_node.tasks_done.copy()
      new_tasks_ready = parent_node.new_tasks_ready[:]
      current_level = []
      for task in given_tasks :
        current_level.append(task)
        new_task_done.add(task)
        new_tasks_ready.remove(task)
      new_graph.append(current_level)  
# Add new tasks to the tasks_ready list
      for task in self.tasks :
        if task not in new_tasks_done :
          ready = True
          for required_task in task.required_tasks :
            if required_task not in new_tasks_done :
              ready = False
              break
          if ready==True :
            if task not in new_tasks_ready :
              new_tasks_ready.append(task)
# The new cost is the cost of parent_node plus one
      new_cost = parent_node.cost + 1
# The min_bound is reached when all the remaining tasks are executed in
# parallel
      new_min_bound = new_cost + (self.n_tasks-len(new_tasks_done))/\
          self.n_processors
# The max_bound is reached when all the remaining tasks are executed serially
      new_max_bound = new_cost + self.n_tasks-len(new_tasks_done)
# Create the new node
      node = Node(new_graph,new_tasks_done,new_tasks_ready,new_min_bound,
          new_max_bound)
    else :
# The node given by the processor combination and the task permutation does
# not exist. cost, min_bound, and max_bound are set to 2*len(self.tasks)
      node = Node(parent_node.graph,parent_node.tasks_done,
          parent_node.tasks_ready,2*len(self.tasks),2*len(self.tasks),
          2*len(self.tasks))

    return node  

#----------------------------------------------------------------------------#

  def solve(self) :
    """Solve the SOP using branch-and-bound algorithm."""

# Create the firt node
    graph = []
    tasks_done = set()
    tasks_ready = []
    cost = 0 
    min_bound = self.n_tasks/n_processors
    max_bound = self.n_tasks
# Build the tasks_ready list. This list constains all the tasks that are ready
# to be executed. At first, these tasks are the one that do not require
# another task.
    for task in self.tasks :
      if task.n_required_tasks==0 :
        self.tasks_ready.append(task)

    subdomains_list = range(1,self.n_processors+1)
    done = False
    while not done :
      lowest_bound = 2*len(self.tasks)
# Best-first search
      pos = 0
      counter = 0
      for node in nodes :
        if node.min_bound<lowest_bound :
          pos = counter
        counter += 1

      for i in xrange(1,self.n_processors+1) :
# itertools create a generator, i.e., a list of iterators that can be used only
# once. If we want to reuse the list, we need to recall itertools
        proc_comb = itertools.combinations(subdomains_list,i)
        for used_procs in proc_comb :
          task_perm = itertools.permutations(nodes[pos].tasks_ready,i)
          for used_tasks in task_perm :
            node = self.create_node(used_procs,used_tasks,nodes[pos])

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

      done = True
      for node in nodes :
        if node.cost!=node.min_bound or node.cost!=node.max_bound :
          done = False
