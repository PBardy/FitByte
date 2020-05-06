from database import *
from input_validation import *
from calculations import *
from account import *
from profile import *
from goal import *

MAX_NAME_LENGTH = 35
MAX_USERNAME_LENGTH = 32
MAX_PASSWORD_LENGTH = 72
MIN_PASSWORD_LENGTH = 6


"""
  Determines whether a goal has been completed.
"""
def get_completed_goals(id, goals):

  completed = []

  for goal in goals:
    obj = make_goal(goal)
    table, tracked = get_all_data(id, obj.get_metric())
    if len(tracked) >= obj.get_interval():
      for datapoint in tracked:
        if datapoint[0] > obj.get_start_date() and datapoint[0] < obj.get_end_date():
          if datapoint[1] <= obj.get_target():
            completed.append(obj)
            break

  return completed


"""
  Displays user goals, including whether they
  have been achieved. 
"""
def display_user_goals(id):

  goals = get_user_goal_data(id)
  
  entries = []
  goal_objs = []
  now = datetime.datetime.now()

  for goal in goals:
    goal_obj = make_goal(goal)
    goal_objs.append(goal_obj)
    metric = goal_obj.get_metric()
    start = goal_obj.get_start_date()
    end = goal_obj.get_end_date()
    target = goal_obj.get_target()
    interval = goal_obj.get_interval()
    table, tracked = get_all_data(id, metric)
    relevant = [val for val in tracked if val[0] > start and val[0] < end]
    data_completion = (len(relevant) / interval) * 100
    achieved = len([val for val in tracked if val[1] <= target]) > 0 and data_completion >= 100
    goal_obj.set_completion(data_completion)
    goal_obj.set_achieved(achieved)
    entries.append(goal_obj.get_properties())

  display_goals(entries)

  return goal_objs


"""
  Displays the leaderboard option selection menu.
"""
def display_leaderboard_menu(id):
  print(get_leaderboard_data())


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

      # Get date strings
      sta = get_date("Track from  (start date): ")
      end = get_date("Track until (end date):   ")

      # For comparison, convert to datetime objects
      date_a = datetime.datetime.strptime(sta, "%Y-%m-%d")
      date_b = datetime.datetime.strptime(end, "%Y-%m-%d")

      if date_a < date_b:
        now = datetime.datetime.now()
        if date_a > now and date_b > now:
          valid = True
        else:
          print()
          print("Dates must be in the future")
          print()
      else:
        print()
        print("Start date must be before end date")
        print()
    
    interval = get_float("Check progress how many times? ", 1, 10)

    create_user_goal(target, metric, sta, end, interval, id)


"""
  Allows a user to change the parameters of a goal.
"""
def edit_user_goal(id):
  
  print()
  print("Edit a goal")
  print()

  all_goals = display_user_goals(id)

  if len(all_goals) > 0:
    print()
    print("Index to edit")
    print()
    index = get_menu_choice(len(all_goals) - 1, min_choice = 0)
    goal = all_goals[index]
    updated = update_goal(goal)   
    update_goal_entry(updated) 

  else:
    print()
    print("There are no goals to edit")
    print()


"""
  Allows the user to cancel a goal.
"""
def cancel_user_goal(id):
  
  print()
  print("Cancel a goal")
  print()

  all_goals = display_user_goals(id)

  if len(all_goals) > 0:
    print()
    print("Index to cancel")
    print()
    index = get_menu_choice(len(all_goals) - 1, min_choice = 0)
    goal = all_goals[index]
    delete_goal_entry(goal)    

  else:
    print()
    print("There are no goals to cancel")
    print()


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


"""
  Retrieves and displays all personal informatics
  data pertaining to a particular account. 
"""
def view_all_data_menu(id):
  
  print()
  print("Displaying all data")
  print()

  print_all_data(get_all_data(id, "energy_intake"))
  print_all_data(get_all_data(id, "fat_intake"))
  print_all_data(get_all_data(id, "fibre_intake"))
  print_all_data(get_all_data(id, "protein_intake"))
  print_all_data(get_all_data(id, "salt_intake"))
  print_all_data(get_all_data(id, "sugar_intake"))
  print_all_data(get_all_data(id, "weight"))


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
  cpd = calories_for_activity_level(msj, activity_level)

  print()
  print("Your BMR")
  print()
  print("Mifflin-St Jeor Equation: %f Calories/day" % msj)
  print("Revised Harris-Benedict Equation: %f Calories/day" %rhb)
  print()

  print("Based on your activity level you need %s Calories/day" %cpd)


def view_my_graphs_menu(id):

  metrics = ["Calories", "Fat", "Fibre", "Protein", "Salt", "Sugar", "Weight"]
  
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
    
    """
    print()
    print("Display graph with a")
    print()
    print("1. Weekly breakdown")
    print("2. Bi-weekly breakdown")
    print("3. Monthly breakdown")
    print("4. Yearly breakdown")

    timescale = get_menu_choice(4)
    """
    
    create_graph(get_data_points(get_all_data(id, metrics[metric - 1])))


"""
  Checks goal completion, which is then used
  to awards badges and calculate the user's position
  on the leaderboard.
"""
def update_account(id):

  goal_data = get_user_goal_data(id)
  completed = get_completed_goals(id, goal_data)
  update_goals_completed(id, len(completed))

  if len(completed) >= 100:
    award_badge(id, badge_id=11)
  if len(completed) >= 75:
    award_badge(id, badge_id=10)
  if len(completed) >= 50:
    award_badge(id, badge_id=9)
  if len(completed) >= 30:
    award_badge(id, badge_id=8)
  if len(completed) >= 25:
    award_badge(id, badge_id=7)
  if len(completed) >= 20:
    award_badge(id, badge_id=6)
  if len(completed) >= 15:
    award_badge(id, badge_id=5)
  if len(completed) >= 10:
    award_badge(id, badge_id=4)
  if len(completed) >= 5:
    award_badge(id, badge_id=3)
  if len(completed) >= 2:
    award_badge(id, badge_id=2)
  if len(completed) >= 1:
    award_badge(id, badge_id=1)


"""
  Prompts user to choose a metric to add data to,
  then prompts the user to state the data they recorded
  the data, and what the data is, before storing this.
"""
def add_informatics_data(id):
  
  while True:

    print()
    print("Add informatics data about")
    print()
    choice, table, name = get_metric()
    print()

    if choice == 8:
      return

    date = get_date("When did you record this data? ", allowFuture=False)

    if choice == 1:
      value = get_calories()
    if choice == 2:
      value = get_float("Fat (grams): ", 0, 1000)
    if choice == 3:
      value = get_float("Fibre (grams): ", 0, 1000)
    if choice == 4:
      value = get_float("Protein (grams): ", 0, 1000)
    if choice == 5:
      value = get_float("Salt (grams): ", 0, 1000)
    if choice == 6:
      value = get_float("Sugar (grams): ", 0, 1000)
    if choice == 7:
      value = get_weight()   

    create_personal_informatics_entry(id, date, value, table)
    update_account(id)


""" 
  Allows user to navigate to the view all data,
  view BMR, view graphs or add data menus. 
"""
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


"""
  Provides a menu to allow user to select
  which sub-menu they wish to progress to.
"""
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
      display_leaderboard_menu(id)
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
    print("5. Delete account")
    print("6. Exit")
    print()

    choice = get_menu_choice(6)

    if choice == 1: 
      edit_account_menu(id)
    if choice == 2: 
      edit_profile_menu(id)
    if choice == 3:
      my_personal_data_menu(id)
    if choice == 4:
      my_goals_menu(id)
    if choice == 5:
      delete_account(id)
      return
    if choice == 6:
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
  dob = get_date("Date of birth: ", allowFuture=False)
  current_weight = get_weight()
  height = get_height()
  sex = get_sex()
  activity_rating = get_activity_rating()
  
  return create_profile(id, first_name, last_name, dob, current_weight, height, sex, activity_rating)


def create_account_menu():
  
  print()
  print("Create your account.")
  print()

  username = get_string("Username: ", 0, MAX_USERNAME_LENGTH)
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