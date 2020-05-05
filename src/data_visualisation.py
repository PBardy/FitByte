import matplotlib.pyplot as plt

from tabulate import tabulate
from calculations import *
from goal import *


"""
  Prints badges in table format; each row shows the badge index
  and a description of the badge. 
"""
def print_badges(results):
  
  if len(results) > 0:
    headers = ["Description"]
    print(tabulate(results, headers=headers, showindex="always"))
  else:
    print("ERROR - Could not find badges")
    print()


"""
  Displays all personal informatics data
  associated with a user account in table
  form. 
"""
def print_all_data(data):
  
  table, results = data

  print()
  print("Printing data for %s" % table)
  print()

  if len(results) > 0:
    headers = ["Date", "Value"]
    print(tabulate(results, headers=headers, showindex="always"))
  else:
    print()
    print("No results to display")


"""
  Creates a graph with (x,y) data points.
"""
def create_graph(data):
  variable, x, y = data
  plt.plot(x, y, color='green')
  plt.xlabel('Time')
  plt.ylabel('%s' % variable)
  plt.title('Your %s against Time' % variable)
  plt.show()


"""
  Prints all goals associated with a particular user account 
  in table format. The results from the database are 
  converted into an abstract data type called goal, which
  performs additional calculations with its base data, such
  as calculation the duration of the goal. 
"""
def display_goals(goal_data):

  headers = ["Target", "Metric", "Start Date", "End Date", "Duration", "Checkups", "Data Completion %", "Achieved"]
  
  if len(goal_data) > 0:
    
    tabulated = tabulate(goal_data, headers=headers, showindex="always")
    
    print()
    print(tabulated)
    print()

  else:
    print()
    print("No goals to display")
    print()
  

"""
  Displays the leaderboard, ranked using a certain metric.
"""
def display_leaderboard(data, metric = False):
  pass
  