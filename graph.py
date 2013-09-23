#! /usr/bin/env python
#----------------------------------------------------------------------------#
# Python code
# Author: Bruno Turcksin
# Date: 2013-09-13 14:31:08.039359
#----------------------------------------------------------------------------#

"""This script reads the output files created by ouranos and build the graph
associated to the tasks. Then, looks to solve the sequential ordering
problem (SOP)."""

import Graph_sweeps
import Task

def compute_downstream_tasks(tasks,n_dir) :
  """Compute the number of tasks and of processors downstream the task."""
  
# To compute the number of tasks downstream, we need to sweep the mesh in the
# reverse order.
  for idir in xrange(n_dir) :
    tasks_ready = []
    for task in tasks :
      if task.n_waiting_tasks==0 and task.idir==idir :
        tasks_ready.append(task)
    
    tasks_done = set()
    while len(tasks_ready)!=0 :
      tasks_ready[0].set_downstream_values(tasks)
      tasks_done.add(tasks_ready[0])
      tasks_ready.pop(0)
      for task in tasks :
        if task.idir==idir and task not in tasks_done :
          ready = True
          for waiting_task in task.waiting_tasks :
            if waiting_task not in tasks_done :
              ready = False
          if ready==True :
            if task not in tasks_ready :
              tasks_ready.append(task)

# Input files
file_names = ['0.txt','1.txt','2.txt']

# Method use to to solve the SOP problem:
#   - FIFO: first-in first-out
#   - MTW: most tasks waiting
#   - MPW: most processors waiting
#   - Rajouter les heuristiques de Pautz
#   - Rajouter branch-and-bound: besoin de 2 bounds. Min bound: utiliser
#   Michael's bound ou, plus simple, plus grand nombres de cells sur un
#   processeur. Max bound: nombre de cells restantes.
methods = ['FIFO','MTW','MPW']
method = methods[2]

# Read the input files
tasks = []
n_dir = 0
for name in file_names :
  file = open(name,'r')
  for line in file :
    if 'subdomain_id' in line :
      task = Task.Task()
      task.subdomain_id = int(line.split()[1])
    if 'ID' in line :
      task.ID = int(line.split()[1])
    if 'idir' in line :
      task.idir = int(line.split()[1])
      if task.idir>n_dir :
        n_dir = task.idir
    if 'sweep order' in line :
      task.sweep_order = int(file.next())
    if 'waiting tasks' in line :
      task.n_waiting_tasks = int(line.split()[2])
      for i in xrange(task.n_waiting_tasks) :
# Transform the list of strings in a list of integers
        if i==0 :
          task.waiting_tasks_data[0] = map(int,file.next().split())
        else :
          task.waiting_tasks_data.append(map(int,file.next().split()))
    if 'required tasks' in line :
      task.n_required_tasks = int(line.split()[2])
      for i in xrange(task.n_required_tasks) :
        if i==0 :
          task.required_tasks_data[0] = map(int,file.next().split())
        else :
          task.required_tasks_data.append(map(int,file.next().split()))
      tasks.append(task)

n_dir += 1

for task in tasks :
  task.convert_tasks_data_to_data(tasks)

if method!='FIFO' :
  compute_downstream_tasks(tasks,n_dir)

graph_sweeps = Graph_sweeps.Graph_sweeps(tasks,method,len(file_names))
graph_sweeps.solve()
graph_sweeps.output_results('output_'+method.lower())
