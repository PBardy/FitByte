import datetime

POUNDS_TO_KILO_RATIO = 1/2.205
CM_TO_INCHES_RATIO = 1/2.54
KCAL_TO_KJ_RATIO = 1/4.184

"""
  Prompts user to enter a metric and returns
  the associated table with that metric. By 
  setting allowReturn to -1, the option to 
  return is left off. 
"""
def get_metric(allowReturn = 0, allowEmpty = False):

  metric_tables = [
    ('Calories', 'energy_intake'),
    ('Fat', 'fat_intake'),
    ('Fibre', 'fibre_intake'),
    ('Protein', 'protein_intake'),
    ('Salt', 'salt_intake'),
    ('Sugar', 'sugar_intake'),
    ('Weight', 'weight'),
    ('Return', None)
  ]

  choices = len(metric_tables) + allowReturn

  for i in range(0, choices):
    print("%d. %s" % (i + 1, metric_tables[i][0]))

  metric = get_menu_choice(choices, allowEmpty = allowEmpty)

  if metric != "":
    metric_name = metric_tables[metric - 1][0]
    metric_tble = metric_tables[metric - 1][1]
  else:
    metric_name = None
    metric_tble = None

  return metric, metric_tble, metric_name


"""
  Prompts user to enter a number corresponding
  to a menu choice. 
"""
def get_menu_choice(choices, min_choice = 1, allowEmpty = False):

  while True:
    try:
      raw = input(":")
      choice = int(raw)
    except ValueError:
      if allowEmpty and raw == "":
        return raw
      else:
        print("Invalid choice")
        print()
        continue
    else:
      if choice not in range(min_choice, choices + 1):
        print("Invalid choice")
        print()
        continue
      else:
        return choice


"""
  Prompts the user to enter a float between
  a minimum and maximum value.
"""
def get_float(prompt, min, max, allowEmpty = False):
  
  while True:
    try:
      raw = input(prompt)
      choice = float(raw)
    except ValueError:
      if allowEmpty and raw == "":
        return raw
      else:
        print("Input must be a decimal number")
        print()
    else:
      if choice <= min:
        print("Input must be greater than %d", min)
        print()
      elif choice >= max:
        print("Input must be less than %d", max)
        print()
      else:
        return choice


"""
  Prompts the user to enter a string of a certain 
  length, or an empty string. 
"""
def get_string(prompt, min, max, allowEmpty = False):

  while True:
    string = str(input(prompt))
    if allowEmpty and string == "":
      return string
    else:
      if len(string) >= min:
        if len(string) <= max:
          return string
        else:
          print()
          print("Input must be less than %d characters" % max)
      else:
        print()
        print("Input must be more than %d characters" % min)


"""
  Prompts the user to enter a data in year, month
  day format. Empty dates are also allowed if allow
  empty is set to true.
"""
def get_date(prompt, allowEmpty = False, allowFuture = True):
  
  print(prompt)

  while True:

    print()
    now = datetime.datetime.now()
    year = get_string("Year (1900-): ", 4, 4, allowEmpty = allowEmpty)
    month = get_string("Month (1-12): ", 1, 2, allowEmpty = allowEmpty)
    day = get_string("Day (1-31): ", 1, 2, allowEmpty = allowEmpty)

    entered_date = ("%s-%s-%s" % (year, month, day))

    try:
      datetime.datetime.strptime(entered_date, "%Y-%m-%d")
    except ValueError:
      if allowEmpty:
        return ""
      else:
        print("Date in incorrect format")
        print() 
    else:
      if allowFuture:
        return entered_date
      else:
        if datetime.datetime.strptime(entered_date, "%Y-%m-%d") > now:
          print()
          print("Dates cannot be in the future")
        else:
          return entered_date


"""
  Prompts user to enter a weight.
"""
def get_weight():
  
  print()
  print("Enter weight in:")
  print("1. kilograms")
  print("2. stone and pounds")
  print("3. pounds")

  choice = get_menu_choice(3)

  if choice == 1:
    kilos = get_float("Kilograms: ", 0, 1000)
    return kilos

  if choice == 2:
    stones = get_float("Stones: ", 0, 100)
    pounds = get_float("Pounds: ", 0, 14)
    return (stones * POUNDS_TO_KILO_RATIO * 14) + (pounds * POUNDS_TO_KILO_RATIO)
  
  if choice == 3:
    pounds = get_float("Pounds: ", 0, 1000)
    return pounds


"""
  Prompts user to enter a height.
"""
def get_height():
  
  print()
  print("Enter height in:")
  print("1. metres")
  print("2. feet and inches")

  choice = get_menu_choice(2)

  if choice == 1:
    metres = get_float("Metres: ", 0, 5)
    return metres * 100

  if choice == 2:
    feet = get_float("Feet: ", 0, 100)
    inches = get_float("Inches: ", 0, 12)
    return (feet * CM_TO_INCHES_RATIO * 12) + (inches * CM_TO_INCHES_RATIO)


"""
  Prompts the user to enter a sex
"""
def get_sex():

  while True:
    sex = get_string("Sex: ", 1, 1)
    if sex.lower() == "m" or sex.lower() == "f":
      return sex


"""
  Prompts the user to enter an activity rating.
"""
def get_activity_rating():

  print()
  print("Describe your activity: ")
  print("1. Extremely inactive")
  print("2. Sedentary (no excercise)")
  print("3. Moderately active (some excercise)")
  print("4. Vigorously active (lots of excersie)")
  print("5. Extremely active (i.e. an athelete)")
  print()

  choice = get_menu_choice(5)

  return choice


def get_calories():

  print()
  print("Enter calories as: ")
  print("1. kcal")
  print("2. kJ")
  print()

  units = get_menu_choice(2)

  print()
  value = get_float("Calories: ", 0, 100000)

  if units == 1:
    return value * KCAL_TO_KJ_RATIO
  else:
    return value