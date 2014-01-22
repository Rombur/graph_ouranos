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

  def __init__(self,tasks,method,n_processors) :

    super(Branch_and_bound,self).__init__()
    self.tasks = tasks
    self.n_tasks = len(tasks)
    self.method = method
    self.n_processors = n_processors
    self.current_directions = []

#----------------------------------------------------------------------------#

  def create_node(self,given_procs,given_tasks,parent_node) :
    """Create a new node given a processor combination, a task combination,
    and a node."""

    n_tasks = len(given_tasks)
    used_procs = set()

    for task in given_tasks :
      if task.subdomain_id in given_procs and\
          task.subdomain_id not in used_procs:
            n_tasks -= 1
            used_procs.add(task.subdomain_id)
# Check that the processor and the task combination exist
    if n_tasks==0 :
      new_graph = parent_node.graph[:]
      current_level = []
      new_tasks_done = parent_node.tasks_done.copy()
      new_tasks_ready = parent_node.tasks_ready[:]
      for task in given_tasks :
        current_level.append(task)
        new_tasks_done.add(task)
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
# The min_bound is given by the largest number of tasks left for one
# processors
      n_tasks_proc = [0 for i in xrange(self.n_processors)]
      for task in self.tasks :
        if task not in new_tasks_done :
          n_tasks_proc[task.subdomain_id] += 1
      new_min_bound = new_cost + max(n_tasks_proc)
# The max_bound is reached when all the remaining tasks are executed serially
      new_max_bound = new_cost + self.n_tasks-len(new_tasks_done)
# Create the new node
      node = Node(new_graph,new_tasks_done,new_tasks_ready,new_cost,
          new_min_bound,new_max_bound)
    else :
# The node given by the processor combination and the task combination does
# not exist. cost, min_bound, and max_bound are set to 2*len(self.tasks)
      node = Node(parent_node.graph,parent_node.tasks_done,
          parent_node.tasks_ready,2*len(self.tasks),2*len(self.tasks),
          2*len(self.tasks))

    return node  

#----------------------------------------------------------------------------#

  def solve(self) :
    """Solve the SOP using branch-and-bound algorithm."""

# Create the first node
    self.nodes = []
    graph = []
    tasks_done = set()
    tasks_ready = []
    cost = 0 
    min_bound = self.n_tasks/self.n_processors
    max_bound = self.n_tasks
# Build the tasks_ready list. This list constains all the tasks that are ready
# to be executed. At first, these tasks are the one that do not require
# another task.
    for task in self.tasks :
      if task.n_required_tasks==0 :
        tasks_ready.append(task)
    first_node = Node(graph,tasks_done,tasks_ready,cost,min_bound,max_bound)
    self.nodes.append(first_node)

    subdomains_list = range(0,self.n_processors)
    done = False
    best_first = False
    continuation_set = set()
    while not done :
      lowest_bound = 2*len(self.tasks)
      n_tasks_done = 0
      pos = 0
      counter = 0
      max_continuation_number = 0
      continuation_list = []
      max_most_waiting_number = 0
      most_waiting_list = []
      max_most_blocking_number = 0
      most_blocking_list = []
# When a processor is working on a direction, we would like that it keeps
# working on that direction similar to what happens on the regular case. This
# operation also favors the nodes that use at least as many processors as
# their parent.
      for node in self.nodes :
        continuation_number = 0
        most_waiting_number = 0
        most_blocking_number = 0
        if len(node.graph)!=0 :
          for task in node.graph[-1] :
            tmp = (task.subdomain_id,task.idir)
            if tmp in continuation_set :
              continuation_number += 1
            most_waiting_number += task.n_total_waiting_tasks
            if task.n_total_waiting_tasks>most_blocking_number :
              most_blocking_number = task.n_total_waiting_tasks
          if continuation_number>max_continuation_number :
            max_continuation_number = continuation_number
        continuation_list.append(continuation_number)  
        most_waiting_list.append(most_waiting_number)
        most_blocking_list.append(most_blocking_number)

      max_level = 0
      for node in self.nodes :
        if best_first==False :
          if continuation_list[counter]==max_continuation_number :
# Most-processors search
            if self.method=='BBMP' :
              if n_tasks_done<len(node.tasks_done) :
                pos = counter
                n_tasks_done = len(node.tasks_done)
# Most-processors most-waiting search
            elif self.method=='BBMPMW' :
              if n_tasks_done<len(node.tasks_done) :
                pos = counter
                n_tasks_done = len(node.tasks_done)
                max_most_waiting_number = most_waiting_list[counter]
              elif n_tasks_done==len(node.tasks_done) :
                if most_waiting_list[counter]>max_most_waiting_number :
                  pos = counter
                  max_most_waiting_number = most_waiting_list[counter]
# Most-processors most-blocking search
            elif self.method=='BBMPMB' :
              if n_tasks_done<len(node.tasks_done) :
                pos = counter
                n_tasks_done = len(node.tasks_done)
                max_most_blocking_number = most_blocking_list[counter]
              elif n_tasks_done==len(node.tasks_done) :
                if most_blocking_list[counter]>max_most_blocking_number :
                  pos = counter
                  max_most_blocking_number = most_blocking_list[counter]
# Most-waiting most-processors search
            elif self.method=='BBMWMP' :
              # Force depth-first
              if len(node.graph)>max_level :
                max_level = len(node.graph)
                pos = counter
                n_tasks_done = len(node.tasks_done)
                max_most_waiting_number = most_waiting_list[counter]
              elif len(node.graph)==max_level :
                if max_most_waiting_number<most_waiting_list[counter] :
                  pos = counter
                  n_tasks_done = len(node.tasks_done)
                  max_most_waiting_number = most_waiting_list[counter]
                elif max_most_waiting_number==most_waiting_list[counter] :
                  if n_tasks_done<len(node.tasks_done) :
                    pos = counter
                    n_tasks_done = len(node.tasks_done)
# Most-blocking most-processors search
            elif self.method=='BBMBMP' :
              # Force depth-first
              if len(node.graph)>max_level :
                max_level = len(node.graph)
                pos = counter
                n_tasks_done = len(node.tasks_done)
                max_most_blocking_number = most_blocking_list[counter]
              elif len(node.graph)==max_level :
                if max_most_blocking_number<most_blocking_list[counter] :
                  pos = counter
                  n_tasks_done = len(node.tasks_done)
                  max_most_blocking_number = most_blocking_list[counter]
                elif max_most_blocking_number==most_blocking_list[counter] :
                  if n_tasks_done<len(node.tasks_done) :
                    pos = counter
                    n_tasks_done = len(node.tasks_done)
            else :
              raise NotImplementedError
        else :
# Best-first search
          if node.min_bound<lowest_bound :
            pos = counter
        if node.min_bound<lowest_bound :
          lowest_bound = node.min_bound
        counter += 1
  
      for i in xrange(1,self.n_processors+1) :
# itertools create a generator, i.e., a list of iterators that can be used only
# once. If we want to reuse the list, we need to recall itertools
        proc_comb = itertools.combinations(subdomains_list,i)
        for used_procs in proc_comb :   
          task_comb = itertools.combinations(self.nodes[pos].tasks_ready,i)
          for used_tasks in task_comb :
            node = self.create_node(used_procs,used_tasks,self.nodes[pos])
            self.nodes.append(node)

# Store the direction-processor pairs. The very first graph is empty and needs
# to be skipped
      continuation_set = set();
      if len(self.nodes[pos].graph)!=0 :
        for task in self.nodes[pos].graph[-1] :
          continuation_set.add((task.subdomain_id,task.idir))

# Every possible children from the node was created, thus the node itself can
# be deleted.
      if self.nodes[pos].cost!=self.nodes[pos].min_bound :
        self.nodes.pop(pos)
# Delete all the nodes that have min_bound larger than the smallest max_bound
      min_max_bound = 2*len(self.tasks)
      for node in self.nodes :
        if node.max_bound<min_max_bound :
          min_max_bound = node.max_bound
      self.nodes = [node for node in self.nodes if node.min_bound<=min_max_bound]

      done = False
      tmp_node = []
      for node in self.nodes :
        if len(node.tasks_ready)==0 :
# If a solution has been found, switch to best-first algorithm
          best_first = True
# Stop if the solution is within 10% of the lowest bound
          if node.cost<=1.1*lowest_bound :
            done = True
            self.nodes[0] = node
            break
# Print the temporary solution
          else :
            if tmp_node is not node :
              print 'Output intermediate result because BB did not converge.'
              print 'Node cost: ',node.cost
              print 'Target: ',1.1*lowest_bound
              self.output_intermediate_results(node)
              tmp_node = node

#----------------------------------------------------------------------------#

  def output_results(self,filename) :
    """Output the results, i.e. the cost and the graph, in a file."""

    file = open(filename+'.txt','w')
    file.write('Minimum cost: '+str(self.nodes[0].cost)+'\n\n')
    for level in self.nodes[0].graph :
      file.write('-------------\n')
      for task in level :
        file.write('subdomain_id: '+str(task.subdomain_id)+'\n')
        file.write('Id: '+str(task.ID)+'\n')
      file.write('\n')
    file.close()  

#----------------------------------------------------------------------------#

  def output_intermediate_results(self,node) :
    """Output intermediate results when Branch-and-Bound does not converge."""

    if self.intermediate_cost not in globals() :
      self.intermediate_cost = 2*len(self.tasks)
      self.intermediate_number = 0

    if self.intermediate_cost<node.cost :
      file = open('output_intermediate_'+str(self.intermediate_number)+'.txt','w')
      file.write('Minimum cost: '+str(node.cost)+'\n\n')
      for level in node.graph :
        file.write('-------------\n')
        for task in level :
          file.write('subdomain_id: '+str(task.subdomain_id)+'\n')
          file.write('Id: '+str(task.ID)+'\n')
        file.write('\n')
      file.close()  
      self.intermediate_number += 1
