# Python code
# Author: Bruno Turcksin
# Date: 2013-09-13 16:18:26.884255

#----------------------------------------------------------------------------#
## Class Graph_sweeps                                                       ##
#----------------------------------------------------------------------------#

"""This module contains the Graph_sweeps class."""

class Graph_sweeps(object) :
  """Solve the SOP create by the sweeps on parallel."""

  def __init__(self,tasks,method) :

    super(Graph_sweeps,self).__init__()
    self.tasks = tasks
    self.graph = []
    self.method = method

#----------------------------------------------------------------------------#

  def use_fifo(self) :
    """Use FIFO (first-in first-out) method to determine the next task."""

    used_procs = set()
# Execute the first task that is ready.
    used_procs.add(self.tasks_ready[0].subdomain_id)
    self.tasks_done.add(self.tasks_ready[0])
    current_level = [self.tasks_ready.pop(0)]
# Add one task per other processor. Because they can be executed at the same
# time than the first task, the cost is zero.
    for task in self.tasks_ready :
      if task.subdomain_id not in used_procs :
        self.tasks_done.add(task)
        used_procs.add(task.subdomain_id)
        current_level.append(self.tasks_ready.pop(self.tasks_ready.index(task)))

    return current_level

#----------------------------------------------------------------------------#

  def solve(self) :
    """Solve the SOP"""

# Cost of the graph. The lower, the better.
    self.cost = 0
# Build the tasks_ready list. This list constains all the tasks that are ready
# to be executed. At first, these tasks are the one that do not require
# another task.
    self.tasks_ready = []
    for task in self.tasks:
      if task.n_required_tasks==0 :
        self.tasks_ready.append(task)

# Build the graph. The while-loop ends when all the tasks are in the graph.
    self.tasks_done = set()
    self.graph = []
    while len(self.tasks_done)!=len(self.tasks) :
      if self.method=='FIFO' :
        current_level = self.use_fifo()
      self.graph.append(current_level)
# Add new tasks to the tasks_ready list.
      for task in self.tasks :
        if task not in self.tasks_done :
          ready = True
          counter = 0
          for required_task in task.required_tasks :
            if required_task not in self.tasks_done :
              ready = False
          if ready==True :
            if task not in self.tasks_ready :
              self.tasks_ready.append(task)

#----------------------------------------------------------------------------#

  def output_results(self,filename) :
    """Output the results, i.e. the cost and the graph, in a file."""

    file = open(filename+'.txt','w')
    file.write('Minimum cost: '+str(len(self.graph))+'\n\n')
    
    for level in self.graph :
      file.write('-------------\n')
      for task in level :
        file.write('subdomain_id: '+str(task.subdomain_id)+'\n')
        file.write('Id: '+str(task.ID)+'\n')
      file.write('\n')
    file.close()  
