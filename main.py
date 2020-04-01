# Modules
import bcrypt
import datetime
import mysql.connector

# Constants
DB_HOST_NAME = "localhost"
DB_USER_NAME = "root"
DB_PASSWORD = ""
DB_DATABASE = "fitbyte"

MAX_NAME_LENGTH = 35

POUNDS_TO_KILO_RATIO = 1/2.205
CM_TO_INCHES_RATIO = 1/2.54
KCAL_TO_KJ_RATIO = 1/4.184

"""
 Represents the account stored in the database.
"""
class Account:

  MAX_USERNAME_LENGTH = 32
  MAX_PASSWORD_LENGTH = 72
  MIN_PASSWORD_LENGTH = 6

  def __init__(self):
    self.__username = self.__get_username()
    self.__password = self.__get_password()
  
  def __get_username(self):
    while True:
      username = str(input("Username: "))
      if len(username) > 0:
        if len(username) < Account.MAX_USERNAME_LENGTH:
          return username
        else:
          print()
          print("Username is too long")
      else:
        print()
        print("Username cannot be empty")

  def __get_password(self):
    while True:
      password1 = str(input("Password: "))
      password2 = str(input("Repeat password: "))
      if password1 == password2:
        if len(password1) > Account.MIN_PASSWORD_LENGTH:
          if len(password1) < Account.MAX_PASSWORD_LENGTH:
            return password1
          else:
            print()
            print("Password is too long. Passwords must be shorter than %s characters." % Account.MAX_PASSWORD_LENGTH)
        else:
          print()
          print("Password must be longer than %s characters." % Account.MIN_PASSWORD_LENGTH)
      else:
        print()
        print("Passwords do not match.")

  def get_id(self):
    return self.__id
  
  def get_username(self):
    return self.__username

  def get_password(self):
    return self.__password


"""
  Connects to the database.

  @return The database connection.
"""
def mysqli():
  return mysql.connector.connect(host=DB_HOST_NAME, user=DB_USER_NAME, passwd=DB_PASSWORD, database=DB_DATABASE)
 
"""
  Creates a profile associated to a particular account. This
  contains all the static information about a user.

  @param id - The account id
  @param first_name - The user's first name
  @param last_name - The user's last name
  @param dob - The user's date of birth
  @param weight - The user's current weight
  @param height - The user's height
  @param height - The user's sex
  @param activity_rating - The user's acitivity rating

  @return - Whether the action was successful
"""
def create_profile(id, first_name, last_name, dob, weight, height, sex, activity_rating):

    db = mysqli()
    cursor = db.cursor()

    sql = """
      INSERT INTO profiles (account_id, first_name, last_name, DOB, current_weight, height, sex, activity_rating) 
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (id, first_name, last_name, dob, weight, height, sex, activity_rating)

    cursor.execute(sql, values)
    db.commit()
    db.close()

    return True


"""
  Creates an account for a particular user.

  @param username - The display username of the user
  @param password - The account password

  @return - The account id (for identification)
"""
def create_account(account):

    db = mysqli()
    cursor = db.cursor()

    salt = bcrypt.gensalt()
    password = account.get_password().encode("utf-8")
    hash = bcrypt.hashpw(password, salt)

    salt = salt.decode("utf-8")
    hash = hash.decode("utf-8")

    print(salt)

    sql = """
      INSERT INTO accounts (username, password_salt, password_hash, date_created) 
      VALUES (%s, %s, %s, CURDATE())
    """

    values = (account.get_username(), salt, hash)

    cursor.execute(sql, values)

    db.commit()
    db.close()

    return cursor.lastrowid


"""
  Changes the username and password of the account.

  @param id - The id of the user
  @param username - The new username associated wih the account
  @param password - The new password associated wih the account

  @return - Whether change was successful
"""
def change_account_details(id, username, password):
  
    db = mysqli()
    cursor = db.cursor()

    salt = bcrypt.gensalt()
    password = password.encode("utf-8")
    hash = bcrypt.hashpw(password, salt)

    salt = salt.decode("utf-8")
    hash = hash.decode("utf-8")

    sql = """
      UPDATE accounts
      SET username = %s, password_salt = %s, password_hash = %s
      WHERE accounts.account_id = %s;
    """

    values = (username, salt, hash, id)

    cursor.execute(sql, values)

    db.commit()
    db.close()

    return True


"""
  Authenticates user credentials.

  @param username - The username to be authenticated
  @param password - The password to be authenticated

  @return - Whether account id if the credentials are valid, None
  if authentication failed.
"""
def authenticate(username, password):

    # Create a database connection
    db = mysqli()
    cursor = db.cursor()

    sql = """
      SELECT password_hash 
      FROM accounts
      WHERE username = "%s"
    """ % (username)

    cursor.execute(sql)
    results = cursor.fetchone()

    db.close()

    # Only check results if they exist
    if results != None:
      if len(results) > 0:
        hashed = results[0]

        if bcrypt.checkpw(password.encode("utf8"), hashed.encode("utf8")):
          return results

    return None


"""
  Deletes the account of a particular user, and all 
  information associated with that account.

  @param id - The password to be authenticated

  @return - Whether the operation was successful
"""
def delete_account(id):

  # Create a database connection
  db = mysqli()
  cursor = db.cursor()
  
  queries = [
    "DELETE FROM accounts WHERE account_id = %s;" % id,
    "DELETE FROM achieved_badges WHERE account_id = %s;" % id,
    "DELETE FROM current_goals WHERE account_id = %s;" % id,
    "DELETE FROM energy_intake WHERE account_id = %s;" % id,
    "DELETE FROM fat_intake WHERE account_id = %s;" % id,
    "DELETE FROM fibre_intake WHERE account_id = %s;" % id,
    "DELETE FROM profiles WHERE account_id = %s;" % id,
    "DELETE FROM protein_intake WHERE account_id = %s;" % id,
    "DELETE FROM salt_intake WHERE account_id = %s;" % id,
    "DELETE FROM sugar_intake WHERE account_id = %s;" % id,
    "DELETE FROM weight WHERE account_id = %s;" % id,
  ]

  for query in queries:
    cursor.execute(query)
    db.commit()

  return True


"""
  This procedure prompts the user to enter an integer from 1 to
  the maximum number of choices, returning the integer they selected.

  @param choices - The maximum number of menu options

  @return - The menu choice, or -1 if the choice was invalid
"""
def get_menu_choice(choices):

  choice = -1

  try:
    choice = int(input(":"))
  except ValueError:
    print("Invalid choice")
    print()
  finally:
    return choice


"""
  Validates whether an integer is an input within a given range.
"""
def get_float(prompt, min, max):
  
  choice = None

  try:
    choice = float(input(prompt))
  except ValueError:
    print("Input must be a decimal number")
    print()
  else:
    if choice < min:
      print("Input must be greater than %d", min)
      print()
    if choice > max:
      print("Input must be less than %d", max)
      print()
  finally:
    return choice


"""
  Prompts user to enter a date in the standard format (yyyy:mm:dd)
"""
def get_date(prompt):
  
  print(prompt)

  correct = False
  now = datetime.datetime.now()

  while not correct:

    year = str(input("Year: "))
    month = str(input("Month (1-12): "))
    day = str(input("Day (1-31): "))

    entered_date = ("%s-%s-%s" % (year, month, day))

    try:
      datetime.datetime.strptime(entered_date, "%Y-%m-%d")
    except ValueError:
      print("Date in incorrect format")
      print()
      continue 
    else:
      return entered_date


"""
  Displays all the achievable badges (list compiled from
  the database).

  @param id - The unique identifier for the user
"""
def display_all_badges():
  
  print()
  print("All achievable badges")

  # Create a database connection
  db = mysqli()
  cursor = db.cursor()

  query = "SELECT description FROM badges"

  cursor.execute(query)
  results = cursor.fetchall()
  db.close()

  if len(results) > 0:
    for result in results:
      print(result)
  else:
    print("ERROR - Could not find badges")
    print()


"""
  Displays all badges achieved by the specified user.

  @param id - The unique identifier for the user
"""
def display_user_badges(id):
  
  print()
  print("Your badges")


"""
  Displays all goals set by the user which are currently
  active. All goals which which have been achieved by the
  user or have expired are shown in a progress summary. These
  are then removed from the database.

  @param id - The unique identifier for the user
"""
def display_user_goals(id):
  
  print()
  print("Your goals")


"""
  Displays a leadboard of all users in descending order of
  how much of a percentage of their goals they've met.

  @param id - The unique identifier for the user
"""
def display_leadboard(id):
  
  print()
  print("Leaderboard")
  print()


"""
  Adds a user goal. 

  @param id - The unique identifier for the user
"""
def add_user_goal(id):
  
  print()
  print("Add a new goal")
  print()

  metric = ""
  valid_metric = False

  while not valid_metric:
    
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
    print("8. None of the above (return to menu)")
    print()

    choice = get_menu_choice(8)

    if choice > 0:
      valid_metric = True
      if choice == 1:
        metric = "energy_intake"
        continue
      if choice == 2:
        metric = "fat_intake"
        continue
      if choice == 3:
        metric = "fibre_intake"
        continue
      if choice == 4:
        metric = "protein_intake"
        continue
      if choice == 5:
        metric = "salt_intake"
        continue
      if choice == 6:
        metric = "sugar_intake"
        continue
      if choice == 7:
        metric = "weight"
        continue
      if choice == 8:
        return
    

"""
  Allows a user to modify a current goal.

  @param id - The unique identifier for the user
"""
def edit_user_goal(id):
  
  print()
  print("Edit a goal")
  print()

  display_user_goals(id)


"""
  Allows a user to cancel a goal. 

  @param id - The unique identifier for the user
"""
def cancel_user_goal(id):
  
  print()
  print("Cancel a goal")
  print()

  display_user_goals(id)


"""
  Displays the menu for editing the account details. From this
  menu the user can change their username or password or delete
  their account with all its associated information.

  @param id - The unique identifier for the user
"""
def edit_account_menu(id):
  
  print()
  print("Edit account information")

  complete = False

  while not complete:

    # Prompt user to select which field they wish to update
    print()
    print("1. Edit username")
    print("2. Edit password")
    print("3. Return")

    choice = get_menu_choice(3)

    if choice > 0:
      if choice == 1:
        pass
      if choice == 2:
        pass
      if choice == 3:
        return


"""
  Displays the menu for editing the profile details. From this
  menu the user can change the values stored about them in 
  their profile. 

  @param id - The unique identifier for the user
"""
def edit_profile_menu(id):
  
  print()
  print("Edit profile information")
  print("Press enter to keep the same")

  complete = False

  while not complete:
    
    print()

    # Prompt user to enter their name
    first_name = str(input("First name: "))
    last_name = str(input("Last name: "))

    # Ensure first name and last name are not empty
    if len(first_name) <= 0 or len(last_name) <= 0:
      print("Names cannot be empty")
      continue

    # Ensure names are not over database limit of 35 characters
    if len(first_name) > MAX_NAME_LENGTH or len(last_name) > MAX_NAME_LENGTH:
      print("Names must not be longer than %d", MAX_NAME_LENGTH)
      continue

    # Prompt user to enter their DOB (so we can calculate age)
    dob = get_date("Date of birth: ")

    # Prompt user to enter their current weight
    current_weight_units = str(input("Current weight units (kg, lb): "))

    # Ensure only valid units are accepted (so we can convert to standard units)
    if current_weight_units.lower() == "kg" or current_weight_units.lower() == "lb":
      current_weight_magnitude = get_float("Current weight (magnitude): ", 0, 1000)
      if current_weight_magnitude != None:
        # Convert pounds to kilograms
        if current_weight_units.lower() == "lb":
          current_weight_magnitude *= POUNDS_TO_KILO_RATIO 
      else:
        continue
    else:
      print("Weight units must be either kg or lb")
      continue

    # Prompt user for their height (stored in cm)#
    height_units = str(input("Height units (cm, inches)"))

    # Ensure entered units are valid
    if height_units.lower() == "cm" or height_units.lower() == "inches":
      height = get_float("Height (magnitude): ", 0, 1000)
      if height != None:
        # Convert feet to cm
        if height_units.lower() == "inches":
          height *= CM_TO_INCHES_RATIO
      else:
        continue
    else:
      print("Height units must be either cm or ft")
      continue

    # Prompt user for their sex (this is used for calculating BMI)
    sex = str(input("Sex (M/F): "))

    # Ensure entered sex is valid
    if not(sex.lower() == "m" or sex.lower() == "f"):
      print("Sex must be either m or f")
      continue

    # Prompt user for their activity rating (1-5)
    print("Describe your activity: ")
    print("1. Extremely inactive")
    print("2. Sedentary (no excercise)")
    print("3. Moderately active (some excercise)")
    print("4. Vigorously active (lots of excersie)")
    print("5. Extremely active (i.e. an athelete)")
    print()

    activity_rating = get_menu_choice(5)

    # Ensure valid menu option has been selected
    if not(activity_rating > 0):
      print("Enter a menu choice between 1 and 5")
      continue


"""
  Displays the user's data in table format. For large datasets
  this information is displayed in multi-page format. The user
  can choose which page they want displayed.

  @param id - The unique identifier for the user
"""
def view_all_data_menu(id):
  pass


"""
  Displays the user's bmr using 3 different equations.

  @param id - The unique identifier for the user
"""
def view_my_bmr(id):
  pass


"""
  Display a menu which allows the user to generate a graph of 
  their data. These graphs can be produced for each measured 
  catergory (e.g. weight, calories, salt intake... ), and can 
  display this information in four different time scales: 
  weekly, bi-weekly, monthly and yearly.

  @param metric - The table from which data is to be collected.
  @param timescale - Specifies how data is grouped (e.g. Weekly)
"""
def create_graph(metric, timescale):
  pass


"""
  Display a menu which allows the user to generate a graph of 
  their data. These graphs can be produced for each measured 
  catergory (e.g. weight, calories, salt intake... ), and can 
  display this information in four different time scales: 
  weekly, bi-weekly, monthly and yearly.

  @param id - The unique identifier for the user
"""
def view_my_graphs_menu(id):
  
  print()
  print("View my data as graphs")

  metric = ""
  valid_metric = False

  while not valid_metric:
    
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
    print("8. None of the above (return to menu)")
    print()

    choice = get_menu_choice(8)

    if choice > 0:
      valid_metric = True
      if choice == 1:
        metric = "energy_intake"
        continue
      if choice == 2:
        metric = "fat_intake"
        continue
      if choice == 3:
        metric = "fibre_intake"
        continue
      if choice == 4:
        metric = "protein_intake"
        continue
      if choice == 5:
        metric = "salt_intake"
        continue
      if choice == 6:
        metric = "sugar_intake"
        continue
      if choice == 7:
        metric = "weight"
        continue
      if choice == 8:
        return

  timescale = ""
  valid_timescale = False

  while not valid_timescale:
    
    print()
    print("Display graph with a")
    print()
    print("1. Weekly breakdown")
    print("2. Bi-weekly breakdown")
    print("3. Monthly breakdown")
    print("4. Yearly breakdown")

    choice = get_menu_choice(4)

    if choice > 0:
      valid_timescale = True
      create_graph(metric, choice)


"""
  Allows the user add data from their own tracking.

  @param id - The unique identifier for the user
"""
def add_informatics_data(id):
  
  print()
  print("Add informatics data")

  valid_entry = False

  while not valid_entry:
    
    print()
    print("1. Add calorie information")
    print("2. Add fat information")
    print("3. Add fibre information")
    print("4. Add protein information")
    print("5. Add salt information")
    print("6. Add sugar information")
    print("7. Add weight information")
    print("8. Return")

    choice = get_menu_choice(8)

    if choice > 0:

      # Attempt to get the amount of calories intaken
      if choice == 1:
        table = "enery_intake"
        print("How many calories did you intake?")
        units = str(input("Units (kcal or kJ"))
        if units.lower() == "kcal" or units.lower() == "kJ":
          value = get_float("Value: ", 0, 10000)
          if value != None:
            if units.lower() == "kcal":
              value *= KCAL_TO_KJ_RATIO
          else:
            continue
        else:
          print("Invalid units")
          continue

      # Attempt to get the amount of fat intaken
      if choice == 2:
        table = "fat_intake"
        print("How many grams of fat did you intake?")
        value = get_float("Value: ", 0, 10000)
        if value == None:
          continue

      # Attempt to get the amount of fibre intaken
      if choice == 3:
        table = "fibre_intake"
        print("How many grams of fibre did you intake?")
        value = get_float("Value: ", 0, 10000)
        if value == None:
          continue

      # Attempt to get the amount of protein intaken
      if choice == 4:
        table = "protein_intake"
        print("How many grams of protein did you intake?")
        value = get_float("Value: ", 0, 10000)
        if value == None:
          continue

      # Attempt to get the amount of salt intake
      if choice == 5:
        table = "salt_intake"
        print("How many grams of salt did you intake?")
        value = get_float("Value: ", 0, 10000)
        if value == None:
          continue

      # Attempt to get the amount of sugar intake
      if choice == 6:
        table = "sugar_intake"
        print("How many grams of sugar did you intake?")
        value = get_float("Value: ", 0, 10000)
        if value == None:
          continue

      if choice == 7:
        table = "weight_intake"
        print()
        print("What was your measured weight?")
        units = str(input("Units (kg or lb): "))
        if units.lower() == "kg" or units.lower() == "lb":
          value = get_float("Value: ", 0, 1000)
          if value != None:
            if units.lower() == "lb":
              value *= POUNDS_TO_KILO_RATIO
        else:
          print("Invalid units")
          continue          
      
      print()
      date = get_date("When did you make this measurement?")
      break
  
  db = mysqli()
  cursor = db.cursor()

  sql = """
    INSERT INTO %s (account_id, date, value) 
    VALUES (%s, %s, %s)
  """

  values = (table, id, date, value)

  cursor.execute(sql, values)
  db.commit()
  db.close()


"""
  Displays the menu for viewing and editing personal informatics
  data. From this menu the user can view a summary of their data,
  change a historic record, add a new record and view a comparison
  of their data against other users.

  @param id - The unique identifier for the user
"""
def my_personal_data_menu(id):
  
  print()
  print("My personal informatics data")

  complete = False

  while not complete:
    
    print()
    print("1. View all data (as table)")
    print("2. View my BMR")
    print("3. View my graphs")
    print("4. Add data")
    print("5. Return")
    print()

    choice = get_menu_choice(5)

    if choice > 0:
      if choice == 1:
        view_all_data_menu(id)
        continue
      if choice == 2:
        view_my_bmr(id)
        continue
      if choice == 3:
        view_my_graphs_menu(id)
        continue
      if choice == 4:
        add_informatics_data(id)
        continue
      if choice == 5:
        return


"""
  Displays the menu for viewing and editing goals. From this 
  menu the user can view the progress of their current goals,
  see what badges they have achieved, add new goals, cancel 
  goals and view a comparison of their progression against 
  other users.

  @param id - The unique identifier for the user
"""
def my_goals_menu(id):
  
  print()
  print("My goals")

  complete = False

  while not complete:
    
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

    if choice > 0:
      if choice == 1:
        display_user_goals(id)
        continue
      if choice == 2:
        display_user_badges(id)
        continue
      if choice == 3:
        display_all_badges()
        continue
      if choice == 4:
        edit_user_goal(id)
        continue
      if choice == 5:
        add_user_goal(id)
        continue
      if choice == 6:
        cancel_user_goal(id)
        continue
      if choice == 7:
        display_leadboard(id)
      if choice == 8:
        return
      

"""
  Displays the main menu, for authenticated users. From here 
  the user can edit their account details, edit their profile
  details, view their and edit their personal informatics data
  and view and edit their goals.

  @param id - The unique identifier for the user
"""
def main_menu(id):
  
  print()
  print("Main menu")

  session_active = True

  while session_active:
    print()
    print("1. Edit account details")
    print("2. Edit profile details")
    print("3. My personal informatics data")
    print("4. My goals")
    print("5. Exit")
    print()

    choice = get_menu_choice(2)

    if choice > 0:
      if choice == 1: 
        edit_account_menu(id)
        continue
      if choice == 2: 
        edit_profile_menu(id)
        continue
      if choice == 3:
        my_personal_data_menu(id)
        continue
      if choice == 4:
        my_goals_menu(id)
        continue
      if choice == 5:
        session_active = False


"""
  Displays the login menu. This prompts the user for a 
  username and password, then attempts to verify the user.
"""
def login_menu():
  
  print()
  print("Login")

  authenticated = False

  while not authenticated:
    
    # Prompt user to input their username and password
    username = str(input("Username: "))
    password = str(input("Password: "))

    # Authentication returns the account id so we can reference the user
    account_id = authenticate(username, password)

    if account_id == None:
      print("Authentication failed.")
      print("Your username or password was incorrect")
      print()
      print("1. Retry")
      print("2. Return to home")
      print()

      choice = get_menu_choice(2)

      if choice == 2:
        return 

    else:
      print("Login successful.")
      print()
      main_menu(account_id)


"""
  Displays the menu for creating a profile. This prompts the 
  user to enter personal details to be associated with their 
  account.

  @param id - The unique identifier for the user.
"""
def create_profile_menu(id):

  print()  
  print("Create your profile")

  created = False

  while not created:

    print()

    # Prompt user to enter their name
    first_name = str(input("First name: "))
    last_name = str(input("Last name: "))

    # Ensure first name and last name are not empty
    if len(first_name) <= 0 or len(last_name) <= 0:
      print("Names cannot be empty")
      continue

    # Ensure names are not over database limit of 35 characters
    if len(first_name) > MAX_NAME_LENGTH or len(last_name) > MAX_NAME_LENGTH:
      print("Names must not be longer than %d", MAX_NAME_LENGTH)
      continue

    # Prompt user to enter their DOB (so we can calculate age)
    dob = get_date("Date of birth: ")

    # Prompt user to enter their current weight
    current_weight_magnitude = get_float("Current weight (magnitude): ", 0, 1000)
    current_weight_units = str(input("Current weight units (kg, lb): "))

    # Ensure entered units are valid
    if current_weight_units.lower() == "kg" or current_weight_units.lower() == "lb":
      # Convert pounds to kilograms
      if current_weight_units.lower() == "lb":
        current_weight_magnitude *= POUNDS_TO_KILO_RATIO 
    else:
      print("Weight units must be either kg or lb")
      continue

    # Prompt user for their height (stored in cm)
    height = get_float("Height (magnitude): ", 0, 1000)
    height_units = str(input("Height units (cm, inches)"))

    # Ensure entered units are valid
    if height_units.lower() == "cm" or height_units.lower() == "inches":
      # Convert feet to cm
      if height_units.lower() == "inches":
        height *= CM_TO_INCHES_RATIO
    else:
      print("Height units must be either cm or ft")
      continue

    # Prompt user for their sex (this is used for calculating BMI)
    sex = str(input("Sex (M/F): "))

    # Ensure entered sex is valid
    if not(sex.lower() == "m" or sex.lower() == "f"):
      print("Sex must be either m or f")
      continue

    # Prompt user for their activity rating (1-5)
    print("Describe your activity: ")
    print("1. Extremely inactive")
    print("2. Sedentary (no excercise)")
    print("3. Moderately active (some excercise)")
    print("4. Vigorously active (lots of excersie)")
    print("5. Extremely active (i.e. an athelete)")
    print()

    activity_rating = get_menu_choice(5)

    # Ensure valid menu option has been selected
    if not(activity_rating > 0):
      print("Enter a menu choice between 1 and 5")
      continue

    # At this point all details are valid, so add to the database
    return create_profile(id, first_name, last_name, dob, current_weight_magnitude, height, sex, activity_rating)


"""
  Displays the menu to create the account. This prompts the 
  user to suggest a username, type a password and repeat it 
  (so they) know it is valid.
"""
def create_account_menu():
  
  print()
  print("Create your account.")

  successful = False

  while not successful:

    account = Account()

    # At this point all details should be valid for database entry
    account_id = create_account(account)

    # If not account id is returned then the entry was not created
    if type(account_id) != int:
      print()
      print("There was an error when creating your account. Do you want to:")
      print()
      print("1. Try again")
      print("2. Exit")
      print()

      choice = get_menu_choice(2)

      if choice > 0:
        if choice == 1:
          continue
        else:
          return 

    else:
      create_profile_menu(account_id)
      return
    

"""
  The main entry point of the program. From here the user 
  inputs commands to retrieve data from, or put data into the 
  database.
"""
def main():
  
  print("Welcome to FitByte, a personal informatics system for nutrition management")

  exiting = False

  while not exiting:
    print()
    print("Main menu:")
    print("1. Create account")
    print("2. Login into existing account")
    print("3. Exit")
    print()

    choice = get_menu_choice(3)

    if choice > 0:
      if choice == 1:
        create_account_menu()
        continue
      if choice == 2:
        login_menu()
        continue
      if choice == 3:
        exiting = True


if __name__ == "__main__":
  main()