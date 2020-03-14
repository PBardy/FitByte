# Modules
import bcrypt
import mysql.connector

# Constants
DB_HOST_NAME = "localhost"
DB_USER_NAME = "root"
DB_PASSWORD = ""
DB_DATABASE = "fitbyte"

"""
  Connects to the database.

  @return The database connection.
"""
def mysqli():
  return mysql.connector.connect(host=DB_HOST_NAME, user=DB_USER_NAME, passwd=DB_PASSWORD, database=DB_DATABASE)
 
"""
  Creates a profile associated to a particular account. This
  contains all the static information about a user.

  @param id         - The account id
  @param first_name - The user's first name
  @param last_name  - The user's last name
  @param dob        - The user's date of birth
  @param weight     - The user's current weight
  @param height     - The user's height
  @param height     - The user's sex
  @param ar         - The user's acitivity rating

  @return           - Whether the action was successful
"""
def create_profile(id, first_name, last_name, dob, weight, height, sex, ar):

    db = mysqli()
    cursor = db.cursor()

    sql = """
      INSERT INTO profiles (account_id, first_name, last_name, DOB, current_weight, height, sex, activity_rating) 
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (id, first_name, last_name, dob, weight, height, sex, ar)

    cursor.execute(sql, values)
    db.commit()
    db.close()

    return True


"""
  Creates an account for a particular user.

  @param username   - The display username of the user
  @param password   - The account password

  @return           - The account id (for identification)
"""
def create_account(username, password):

    db = mysqli()
    cursor = db.cursor()

    salt = bcrypt.gensalt()
    password = password.encode("utf-8")
    hash = bcrypt.hashpw(password, salt)

    salt = salt.decode("utf-8")
    hash = hash.decode("utf-8")

    sql = """
      INSERT INTO accounts (username, password_salt, password_hash, date_created) 
      VALUES (%s, %s, %s, CURDATE())
    """

    values = (username, salt, hash)

    cursor.execute(sql, values)

    db.commit()
    db.close()

    return cursor.lastrowid


"""
  Changes the username and password of the account.

  @param id         - The id of the user
  @param username   - The new username associated wih the account
  @param password   - The new password associated wih the account

  @return           - Whether change was successful
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

  @param username   - The username to be authenticated
  @param password   - The password to be authenticated

  @return           - Whether the user credentials are valid
"""
def authenticate(username, password):

    db = mysqli()
    cursor = db.cursor()

    sql = """
      SELECT password_hash 
      FROM accounts
      WHERE username = "%s"
    """ % (username)

    cursor.execute(sql)
    results = cursor.fetchone()
    hashed = results[0]

    db.close()

    return bcrypt.checkpw(password.encode("utf8"), hashed.encode("utf8"))


"""
  Deletes the account of a particular user, and all 
  information associated with that account.

  @param id        - The password to be authenticated

  @return          - Whether the operation was successful
"""
def delete_account(id):

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
  The main entry point of the program. From here the user 
  inputs commands to retrieve data from, or put data into the 
  database.
"""
def main():
  pass


if __name__ == "__main__":
  main()
