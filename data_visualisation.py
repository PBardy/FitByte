from tabulate import tabulate
from goal import *

"""
  Prints all goals associated with a particular user account 
  in table format. The results from the database are 
  converted into an abstract data type called goal, which
  performs additional calculations with its base data, such
  as calculation the duration of the goal. 
"""
def print_goal_table(results):

  if len(results) > 0:
    headers = ["Target", "Metric", "Start Date", "End Date", "Duration", "Checkups"]
    table = [make_goal(result).get_properties() for result in results]
    print(tabulate(table, headers=headers, showindex="always"))
  else:
    print("You currently have no goals.")
    print()


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
