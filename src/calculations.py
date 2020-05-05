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
def calories_for_activity_level(bmr, activity_level):

  if activity_level == 1:
    return bmr * 1.2
  if activity_level == 2:
    return bmr * 1.45
  if activity_level == 3:
    return bmr * 1.65
  if activity_level == 4:
    return bmr * 1.85
  if activity_level == 5:
    return bmr * 2.2


"""
  Sorts data by date and provides the data points
  for the graphing program to plot.
"""
def get_data_points(results):
  table, data = results
  data.sort(key = lambda datapoint: datapoint[0])
  x = [str(value[0])   for value in data]
  y = [float(value[1]) for value in data]
  return table, x, y
