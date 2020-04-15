import bcrypt
import mysql.connector

from account import *
from profile import *
from goal import *
from data_visualisation import *

DB_HOST_NAME = "localhost"
DB_USER_NAME = "root"
DB_PASSWORD = ""
DB_DATABASE = "fitbyte"

"""
  Creates a connection to the database.
"""
def connect():
  try:
    connection = mysql.connector.connect(
      host = DB_HOST_NAME, 
      user = DB_USER_NAME, 
      passwd = DB_PASSWORD, 
      database = DB_DATABASE
    )
  except Exception:
    print()
    print("Could not connect to database.")
    exit()
  else:
    return connection


"""
  Creates a profile associated to a particular account. This
  contains all the static information about a user.
"""
def create_profile(id, first_name, last_name, dob, weight, height, sex, activity_rating):

    sql = """
      INSERT INTO profiles (account_id, first_name, last_name, DOB, current_weight, height, sex, activity_rating) 
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (str(id), str(first_name), str(last_name), str(dob), str(weight), str(height), str(sex), str(activity_rating))

    db = connect()
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    db.close()

    return True

"""
  Creates an account for a particular user.
"""
def create_account(username, salt, hash):

    sql = """
      INSERT INTO accounts (username, password_salt, password_hash, date_created) 
      VALUES (%s, %s, %s, CURDATE())
    """

    values = (str(username), str(salt), str(hash))

    db = connect()
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    db.close()

    return cursor.lastrowid


"""
  Inserts personal informatics data into its
  respective table.
"""
def create_personal_informatics_entry(id, date, value, table):

  sql = """
    INSERT INTO """ + table + """ (account_id, date, value) 
    VALUES (%s, %s, %s)
  """

  values = (str(id), str(date), str(value))

  db = connect()
  cursor = db.cursor()
  cursor.execute(sql, values)
  db.commit()
  db.close()


def change_account_details(id, username, salt, hash):

    sql = """
      UPDATE accounts
      SET username = %s, password_salt = %s, password_hash = %s
      WHERE accounts.account_id = %s;
    """

    values = (str(username), str(salt), str(hash), str(id))

    db = connect()
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    db.close()

    return True


def change_profile_details(id, first_name, last_name, dob, current_weight, height, sex, activity_rating):

    sql = """
      UPDATE profiles
      SET first_name = %s, last_name = %s, dob = %s, current_weight = %s, height = %s, sex = %s, activity_rating = %s
      WHERE profiles.account_id = %s;
    """

    values = (str(first_name), str(last_name), str(dob), str(current_weight), str(height), str(sex), str(activity_rating), str(id))

    db = connect()
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    db.close()

    return True


"""
  Validates users and returns their unique identifier for
  further queries.
"""
def authenticate(username, password):

    sql = """
      SELECT account_id, password_hash 
      FROM accounts
      WHERE username = "%s"
    """ % (username)

    db = connect()
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchone()
    db.close()

    if results != None:
      if len(results) > 1:
        hashed = results[1]
        if bcrypt.checkpw(password.encode("utf8"), hashed.encode("utf8")):
          return results[0]


"""
  Returns an instance of an account when provided with a 
  particular id. 
"""
def get_account(id):

  sql = "SELECT * FROM accounts WHERE account_id = %s" % id

  db = connect()
  cursor = db.cursor()
  cursor.execute(sql)
  results = cursor.fetchone()
  db.close()

  return Account(results)


"""
  Returns the information associated with a particular profile
"""
def get_profile(id):

  sql = "SELECT * FROM profiles WHERE account_id = %s" % id

  db = connect()
  cursor = db.cursor()
  cursor.execute(sql)
  results = cursor.fetchone()
  db.close()

  return Profile(results)


"""
  Deletes all information associated with a particular account.
"""
def delete_account(id):
  
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

  db = connect()
  cursor = db.cursor()

  for query in queries:
    cursor.execute(query)
    db.commit()

  return True


"""
  Displays all badges available for a user to get.
"""
def display_all_badges():
  
  print()
  print("All achievable badges")
  print()

  query = "SELECT description FROM badges"

  db = connect()
  cursor = db.cursor()
  cursor.execute(query)
  results = cursor.fetchall()
  db.close()

  print_badges(results)


"""
  Displays all badges achieved by a particular user.
"""
def display_user_badges(id):
  
  print()
  print("Your badges")
  print()

  query = """
    SELECT badges.description 
    FROM badges, (
      SELECT achieved_badges.badge_id, achieved_badges.account_id
      FROM achieved_badges
    ) AS user_badges
    WHERE badges.badge_id = user_badges.badge_id
    AND user_badges.account_id = %s
  """ % id

  db = connect()
  cursor = db.cursor()
  cursor.execute(query)
  results = cursor.fetchall()
  db.close()

  print_badges(results)


def get_user_goal_data(id):
  
  print()
  print("Your goals")
  print()

  query = """
    SELECT * FROM current_goals
    WHERE account_id = %s
  """ % id

  db = connect()
  cursor = db.cursor()
  cursor.execute(query)
  results = cursor.fetchall()
  db.close()

  return results


"""
  Displays a leadboard of all current 
"""
def display_leadboard(id):
  
  print()
  print("Leaderboard")
  print()


"""
  Creates a user goal.
"""
def create_user_goal(target, metric, start_date, end_date, interval, id):
  
  sql = """
    INSERT INTO current_goals (target, metric, start_date, end_date, set_interval, account_id)
    VALUES (%s, %s, %s, %s, %s, %s)
  """

  values = (str(target), str(metric), str(start_date), str(end_date), str(interval), str(id))

  db = connect()
  cursor = db.cursor()
  cursor.execute(sql, values)
  db.commit()
  db.close()


"""
  Creates a user goal.
"""
def award_badge(id, badge_id):
  
  sql = """
    INSERT INTO achieved_badges (account_id, badge_id)
    VALUES (%s, %s)
  """

  values = (str(id), str(badge_id))

  db = connect()
  cursor = db.cursor()
  cursor.execute(sql, values)
  db.commit()
  db.close()


"""
  Retrieves all data pertaining to a
  particular account. 
"""
def get_all_data(id, table):
  
  sql = """
    SELECT date, value
    FROM """ + table + """
    WHERE account_id = %s
  """ % id
  
  db = connect()
  cursor = db.cursor()
  cursor.execute(sql)
  results = cursor.fetchall()
  db.close()

  return table, results

