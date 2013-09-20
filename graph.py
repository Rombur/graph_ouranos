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

# Input files
file_names = ['0.txt','1.txt','2.txt']

# Method use to to solve the SOP problem:
#   - FIFO: first-in first-out
method = 'FIFO'

# Read the input files
tasks = []
for name in file_names :
  file = open(name,'r')
  for line in file :
    if 'subdomain_id' in line :
      task = Task.Task()
      task.subdomain_id = int(line.split()[1])
    if 'ID' in line :
      task.ID = int(line.split()[1])
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

for task in tasks :
  task.convert_tasks_data_to_data(tasks)

graph_sweeps = Graph_sweeps.Graph_sweeps(tasks,method)
graph_sweeps.solve()
graph_sweeps.output_results('output')
