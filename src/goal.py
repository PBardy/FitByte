class Goal:

  def __init__(self, target, metric, start_date, end_date, interval, id):
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

  def get_target(self):
    return self.__target

  def get_metric(self):
    return self.__metric

  def get_start_date(self):
    return self.__start_date
    
  def get_end_date(self):
    return self.__end_date

  def get_interval(self):
    return self.__interval

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

  def set_completion(self, perc):
    self.__completion = perc

  def set_achieved(self, status):
    self.__achieved = status


def make_goal(db_entry):
  return Goal(db_entry[1], db_entry[2], db_entry[3], db_entry[4], db_entry[5], db_entry[6])