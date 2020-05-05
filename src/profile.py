import datetime

class Profile:

  def __init__(self, entry):
    self.__id = entry[1]
    self.__first_name = entry[2]
    self.__last_name = entry[3]
    self.__dob = entry[4]
    self.__current_weight = entry[5]
    self.__height = entry[6]
    self.__sex = entry[7]
    self.__activity_rating = entry[8]
    self.__goals_completed = entry[9]

  def get_first_name(self):
    return str(self.__first_name)

  def get_last_name(self):
    return str(self.__last_name)

  def get_dob(self):
    return self.__dob

  def get_age(self):
    today = datetime.date.today()
    difference = datetime.date.today() - self.__dob
    age = difference.days / 365.25
    return age

  def get_current_weight(self):
    try:
      weight = float(self.__current_weight)
    except ValueError:
      print()
      print("Cannot get weight.")
    else:
      return weight

  def get_weight(self):
    return self.get_current_weight()

  def get_height(self):
    try:
      height = float(self.__height)
    except ValueError:
      print()
      print("Cannot get height.")
    else:
      return height

  def get_sex(self):
    return self.__sex

  def get_activity_rating(self):
    try:
      rating = int(self.__activity_rating)
    except ValueError:
      print()
      print("Cannot get activity rating.")
    else:
      return rating
  
  def get_goals_completed(self):
    try:
      goals_completed = int(self.__goals_completed)
    except ValueError:
      print()
      print("Cannot get goals completed")