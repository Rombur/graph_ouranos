# Python code
# Author: Bruno Turcksin
# Date: 2013-09-13 14:49:16.009810

#----------------------------------------------------------------------------#
## Class Task                                                               ##
#----------------------------------------------------------------------------#

"""This module contains the Task class."""

class Task(object) :
  """This class contains all the data needed to fully define a task."""

  def __init__(self) :

    super(Task,self).__init__()
    self.subdomain_id = 0
    self.ID = 0
    self.idir = 0
    self.n_waiting_tasks = 0
    self.n_required_tasks = 0
    self.waiting_tasks_data = [[]]
    self.required_tasks_data = [[]]
    self.n_downstream_tasks = 0
    self.n_downstream_procs = 0

#----------------------------------------------------------------------------#

  def convert_tasks_data_to_data(self,tasks) :
    """Convert the tasks_data to actual tasks."""

    self.waiting_tasks = []
    self.required_tasks = []

    for task in tasks :
      if len(self.waiting_tasks_data[0])!=0 :
        for waiting_task in self.waiting_tasks_data :
          if waiting_task[0]==task.subdomain_id and waiting_task[1]==task.ID :
            self.waiting_tasks.append(task)
      if len(self.required_tasks_data[0])!=0 :
        for required_task in self.required_tasks_data :
          if required_task[0]==task.subdomain_id and required_task[1]==task.ID :
            self.required_tasks.append(task)

#----------------------------------------------------------------------------#

  def set_downstream_values(self,tasks) :
    """Set the downstream values (tasks and processors) of the current
    task."""

    self.total_waiting_tasks = set()
    self.total_waiting_processors = set()
    self.total_waiting_processors.add(self.subdomain_id)
    tmp_b_level = 0
    for task in tasks :
      if task in self.waiting_tasks :
        self.total_waiting_tasks.add(task)
        for tmp in task.total_waiting_tasks :
          self.total_waiting_tasks.add(tmp)
        self.total_waiting_processors.add(task.subdomain_id)
        for tmp in task.total_waiting_processors :
          self.total_waiting_processors.add(tmp)
        if tmp_b_level<task.b_level :
          tmp_b_level = task.b_level

    self.b_level = tmp_b_level+1
    self.n_total_waiting_tasks = len(self.total_waiting_tasks)
    self.n_total_waiting_processors = len(self.total_waiting_processors)-1

#----------------------------------------------------------------------------#

  def set_dfds_level(self,tasks,max_b_level) :
    """Set the level priorities for DFDS heuristic."""

    tmp_dfds_level = 0
    if self.n_total_waiting_processors!=0 :
      for task in tasks :
        if task in self.waiting_tasks :
          if task.subdomain_id!=self.subdomain_id :
            if tmp_dfds_level<task.b_level+max_b_level :
              tmp_dfds_level = task.b_level+max_b_level
          else :
            if tmp_dfds_level<task.dfds_level-1 :
              tmp_dfds_level = task.dfds_level-1
