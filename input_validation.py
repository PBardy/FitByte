import datetime

POUNDS_TO_KILO_RATIO = 1/2.205
CM_TO_INCHES_RATIO = 1/2.54
KCAL_TO_KJ_RATIO = 1/4.184

def get_menu_choice(choices):

  while True:
    try:
      choice = int(input(":"))
    except ValueError:
      print("Invalid choice")
      print()
      continue
    else:
      if choice not in range(1, choices + 1):
        print("Invalid choice")
        print()
        continue
      else:
        return choice


def get_float(prompt, min, max):
  
  while True:
    try:
      choice = float(input(prompt))
    except ValueError:
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


def get_string(prompt, min, max):

  while True:
    string = str(input(prompt))
    if len(string) >= min:
      if len(string) <= max:
        return string
      else:
        print()
        print("Input must be less than %d characters" % max)
    else:
      print()
      print("Input must be more than %d characters" % min)


def get_date(prompt):
  
  print(prompt)

  while True:

    print()
    now = datetime.datetime.now()
    year = get_string("Year (1900-): ", 4, 4)
    month = get_string("Month (1-12): ", 1, 2)
    day = get_string("Day (1-31): ", 1, 2)

    entered_date = ("%s-%s-%s" % (year, month, day))

    try:
      datetime.datetime.strptime(entered_date, "%Y-%m-%d")
    except ValueError:
      print("Date in incorrect format")
      print() 
    else:
      return entered_date


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


def get_sex():

  while True:
    sex = get_string("Sex: ", 1, 1)
    if sex.lower() == "m" or sex.lower() == "f":
      return sex


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