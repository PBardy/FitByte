from database import *
from input_validation import *
from account import *
from profile import *

MAX_NAME_LENGTH = 35
MAX_USERNAME_LENGTH = 32
MAX_PASSWORD_LENGTH = 72
MIN_PASSWORD_LENGTH = 6


"""
  Adds a user goal to the database. 
"""
def add_user_goal(id):
  
  while True:

    print()
    print("Add a new goal")
    print()
    print("I want to track:")
    print()
    print("1. Energy intake (calories)")
    print("2. Fat intake")
    print("3. Fibre intake")
    print("4. Protein intake")
    print("5. Salt intake")
    print("6. Sugar intake")
    print("7. Weight")
    print("8. Return")
    print()

    metric = get_menu_choice(8)

    if metric == 1:
      metric = "energy_intake"
    elif metric == 2:
      metric = "fat_intake"
    elif metric == 3:
      metric = "fibre_intake"
    elif metric == 4:
      metric = "protein_intake"
    elif metric == 5:
      metric = "salt_intake"
    elif metric == 6:
      metric == "sugar_intake"
    elif metric == 7:
      metric = "weight"
    elif metric == 8:
      return 

    target = get_float("Target: ", 0, 100000)
    
    valid = False

    while not valid:

      start_date = get_date("Track from (start date): ")
      end_date = get_date("Track until (end date): ")

      if start_date < end_date:
        valid = True
    
    interval = get_float("Check progress how many times? ", 1, 10)

    create_user_goal(target, metric, start_date, end_date, interval, id)


"""
  Allows a user to change the parameters of a goal.
"""
def edit_user_goal(id):
  
  print()
  print("Edit a goal")
  print()

  display_user_goals(id)


"""
  Allows the user to cancel a goal.
"""
def cancel_user_goal(id):
  
  print()
  print("Cancel a goal")
  print()

  display_user_goals(id)


"""
  Allows the user to change their username or password.
"""
def edit_account_menu(id):
  
  print()
  print("Edit account information")
  print("Press enter to keep the same")
  print()

  username = get_string("Username: ", 0, MAX_NAME_LENGTH)
  password = get_string("Password: ", MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH)
  salt, hash = get_hash_and_salt(password)

  change_account_details(id, username, salt, hash)


"""
  Allows the user to edit their profile information, such
  as their current weight, or any other details they may
  have entered incorrectly during account creation.
"""
def edit_profile_menu(id):
  
  print()
  print("Edit profile information")
  print("Press enter to keep the same")
  print()

  first_name = get_string("First name: ", 0, MAX_NAME_LENGTH)
  last_name = get_string("Last name: ", 0, MAX_NAME_LENGTH)
  dob = get_date("Date of birth: ")
  current_weight = get_weight()
  height = get_height()
  sex = get_sex()
  activity_rating = get_activity_rating()

  change_profile_details(first_name, last_name, dob, current_weight, height, sex, activity_rating)


def view_all_data_menu(id):
  pass


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


"""
  Displays the users BMR using the Mifflin-St Jeor and the 
  Revised Harris-Benedict equation. The recommended calorie
  intake for their activity level is also displayed.
"""
def view_my_bmr(id):

  profile = get_profile(id)
  weight = profile.get_weight()
  height = profile.get_height()
  age = profile.get_age()
  sex = profile.get_sex()
  activity_level = profile.get_activity_rating()

  msj = mifflin_st_jeor(weight, height, age, sex)
  rhb = revised_harris_benedict(weight, height, age, sex)
  cpd = calories_for_activity_level(activity_level)

  print()
  print("Your BMR")
  print()
  print("Mifflin-St Jeor Equation: %f Calories/day" % msj)
  print("Revised Harris-Benedict Equation: %f Calories/day" %rhb)
  print()

  print("Based on your activity level you need %s Calories/day" %cpd)


def create_graph(metric, timescale):
  pass


def view_my_graphs_menu(id):
  
  while True:

    print()
    print("View my data as graphs")
    print()
    print("Graph:")
    print()
    print("1. My energy intake (calories)")
    print("2. My fat intake")
    print("3. My fibre intake")
    print("4. My protein intake")
    print("5. My salt intake")
    print("6. My sugar intake")
    print("7. My weight")
    print("8. Return")
    print()

    metric = get_menu_choice(8)

    if metric == 8:
      return
    
    print()
    print("Display graph with a")
    print()
    print("1. Weekly breakdown")
    print("2. Bi-weekly breakdown")
    print("3. Monthly breakdown")
    print("4. Yearly breakdown")

    timescale = get_menu_choice(4)

    create_graph(metric, timescale)


def add_informatics_data(id):
  
  while True:

    print()
    print("Add informatics data")
    print()
    print("1. Add calorie information")
    print("2. Add fat information")
    print("3. Add fibre information")
    print("4. Add protein information")
    print("5. Add salt information")
    print("6. Add sugar information")
    print("7. Add weight information")
    print("8. Return")
    print()

    choice = get_menu_choice(8)
    date = get_date("When did you record this data? ")

    if choice == 1:
      calories = get_calories()

    if choice == 7:
      weight = get_weight()       


def my_personal_data_menu(id):
  
  while True:

    print()
    print("My personal informatics data")
    print()
    print("1. View all data (as table)")
    print("2. View my BMR")
    print("3. View my graphs")
    print("4. Add data")
    print("5. Return")
    print()

    choice = get_menu_choice(5)

    if choice == 1:
      view_all_data_menu(id)
    if choice == 2:
      view_my_bmr(id)
    if choice == 3:
      view_my_graphs_menu(id)
    if choice == 4:
      add_informatics_data(id)
    if choice == 5:
      return


def my_goals_menu(id):
  
  while True:

    print()
    print("My goals")
    print()
    print("1. View current goals")
    print("2. View achieved badges")
    print("3. View all badges")
    print("4. Edit a goal")
    print("5. Add a new goal")
    print("6. Cancel a goal")
    print("7. Leaderboard")
    print("8. Return")
    print()

    choice = get_menu_choice(8)

    if choice == 1:
      display_user_goals(id)
    if choice == 2:
      display_user_badges(id)
    if choice == 3:
      display_all_badges()
    if choice == 4:
      edit_user_goal(id)
    if choice == 5:
      add_user_goal(id)
    if choice == 6:
      cancel_user_goal(id)
    if choice == 7:
      display_leadboard(id)
    if choice == 8:
      return
      

def main_menu(id):
  
  while True:

    print()
    print("Main menu")
    print()
    print("1. Edit account details")
    print("2. Edit profile details")
    print("3. My personal informatics data")
    print("4. My goals")
    print("5. Exit")
    print()

    choice = get_menu_choice(5)

    if choice == 1: 
      edit_account_menu(id)
    if choice == 2: 
      edit_profile_menu(id)
    if choice == 3:
      my_personal_data_menu(id)
    if choice == 4:
      my_goals_menu(id)
    if choice == 5:
      return 


def login_menu():
  
  print()
  print("Login")
  print()

  username = get_string("Username: ", 0, MAX_USERNAME_LENGTH)
  password = get_string("Password: ", MIN_PASSWORD_LENGTH, MAX_USERNAME_LENGTH)

  account_id = authenticate(username, password)

  if account_id == None:
    print()
    print("Authentication failed.")
    print("Your username or password was incorrect")
    print()
    print("1. Retry")
    print("2. Return to home")
    print()

    choice = get_menu_choice(2)

    if choice == 1:
      login_menu()
    if choice == 2:
      return 

  else:
    print()
    print("Login successful.")
    print()
    main_menu(account_id)


def create_profile_menu(id):

  print()  
  print("Create your profile")
  print()

  first_name = get_string("First name: ", 0, MAX_NAME_LENGTH)
  last_name = get_string("Last name: ", 0, MAX_NAME_LENGTH)
  dob = get_date("Date of birth: ")
  current_weight = get_weight()
  height = get_height()
  sex = get_sex()
  activity_rating = get_activity_rating()
  
  return create_profile(id, first_name, last_name, dob, current_weight, height, sex, activity_rating)


def create_account_menu():
  
  print()
  print("Create your account.")
  print()

  username = get_string("Username: ", 0, MAX_NAME_LENGTH)
  password = get_string("Password: ", MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH)
  salt, hash = get_hash_and_salt(password)

  account_id = create_account(username, salt, hash)

  if type(account_id) != int:
    print()
    print("There was an error when creating your account. Do you want to:")
    print()
    print("1. Try again")
    print("2. Exit")
    print()

    choice = get_menu_choice(2)

    if choice == 1:
      create_account_menu()
    else:
      return 

  else:
    create_profile_menu(account_id)
    

def main():
  
  while True:

    print()
    print("Welcome to FitByte, a personal informatics system for nutrition management")
    print()
    print("Main menu:")
    print("1. Create account")
    print("2. Login into existing account")
    print("3. Exit")
    print()

    choice = get_menu_choice(3)

    if choice == 1:
      create_account_menu()
    if choice == 2:
      login_menu()
    if choice == 3:
      return


if __name__ == "__main__":
  main()