import datetime
from operator import itemgetter
"""
  Calculates a person's BMR using the Mifflin-St Jeor 
  equation.
"""
def mifflin_st_jeor(weight, height, age, sex):

  if sex.lower() == "m":
    return (10 * weight) + (6.25 * height) - (5 * age) + 5
  if sex.lower() == "f":
    return (10 * weight) + (6.25 * height) - (5 * age) - 161


"""
  Calculates a person's BMR using the revised Harris-Benedict 
  equation.
"""
def revised_harris_benedict(weight, height, age, sex):

  if sex.lower() == "m":
    return (13.397 * weight) + (4.799 * height) - (5.677 * age) + 88.362
  if sex.lower() == "f":
    return (9.247 * weight) + (3.098 * height) - (4.330 * age) + 447.593


"""
  Returns the number of calories a person should consume daily to maintain
  their BMR for different activity levels.
"""
def calories_for_activity_level(activity_level):

  if activity_level == 1:
    return 2378
  if activity_level == 2:
    return 2724
  if activity_level == 3:
    return 2903
  if activity_level == 4:
    return 3071
  if activity_level == 5:
    return 3418


def get_data_points(results):
  table, data = results
  data.sort(key = lambda datapoint: datapoint[0])
  x = [str(value[0])   for value in data]
  y = [float(value[1]) for value in data]
  return table, x, y