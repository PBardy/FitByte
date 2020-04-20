from input_validation import *

class Goal:

  def __init__(self, entryid, target, metric, start_date, end_date, interval, id):
    self.__entryid = entryid
    self.__target = target
    self.__metric = metric
    self.__start_date = start_date
    self.__end_date = end_date
    self.__interval = interval
    self.__id = id
    self.__completion = 0
    self.__achieved = False

  def __repr__(self):
    return "Goal"

  def get_properties(self):
    properties = [
      str(self.__target),
      str(self.__metric),
      str(self.__start_date),
      str(self.__end_date),
      str(self.get_goal_duration()),
      str(self.__interval),
      str(self.__completion),
      str(self.__achieved)
    ]
    
    return properties

  def get_entryid(self):
    return self.__entryid

  def get_target(self):
    return self.__target

  def get_metric(self):
    return self.__metric

  def get_start_date(self):
    return self.__start_date
    
  def get_end_date(self):
    return self.__end_date

  def get_interval(self):
    return int(self.__interval)

  def get_set_interval(self):
    return self.get_interval()
    
  def get_id(self):
    return self.__id

  def get_account_id(self):
    return self.get_id()

  def get_completion(self):
    return self.__completion

  def get_goal_duration(self):
    return (self.__end_date - self.__start_date).days

  def get_achieved(self):
    return self.__achieved

  def set_target(self, target):
    self.__target = target

  def set_metric(self, metric):
    self__metric = metric

  def set_start_date(self, start_date):
    self.__start_date = start_date

  def set_end_date(self, end_date):
    self.__end_date = end_date

  def set_interval(self, interval):
    self.__interval = interval

  def set_completion(self, perc):
    self.__completion = perc

  def set_achieved(self, status):
    self.__achieved = status


"""
  Prompts the user to edit each field
  of a goal, and update accordingly.
"""
def update_goal(goal):
  
  print()
  print("For each part, leave blank if you want to keep the value the same.")

  # Prompt user to edit target information

  print()
  target = get_float("Target: ", 0, 10000, allowEmpty = True)
  print()

  # Prompt user to edit metric info
   
  print()
  print("Metric")
  print()
  metric, metric_table, metric_name = get_metric(allowReturn = -1, allowEmpty = True)

  # Prompt user to edit start date info

  print()
  start_date = get_date("Start date: ", allowEmpty = True)
  print()

  # Prompt user to edit end data info

  print()
  end_date = get_date("End date: ", allowEmpty = True)
  print()

  # Prompt the user to edit the interval data

  print()
  interval = get_float("Interval: ", 0, 10, allowEmpty = True)
  print()

  # Update goal entry locally

  if target != "":
    goal.set_target(target)

  if metric != "":
    goal.set_metric(metric)

  if start_date != "":
    goal.set_start_date(start_date)

  if end_date != "":
    goal.set_end_date(end_date)

  if interval != "":
    goal.set_interval(interval)

  return goal


"""
  Converts a database entry (represented as a 
  tuple of fields) into a goal object. 
"""
def make_goal(db_entry):
  return Goal(db_entry[0], db_entry[1], db_entry[2], db_entry[3], db_entry[4], db_entry[5], db_entry[6])