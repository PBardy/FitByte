import bcrypt

class Account:
    
  def __init__(self, entry):
    self.__id = entry[0]
    self.__username = entry[1]
    self.__salt = entry[2]
    self.__hash = entry[3]
    self.__date = entry[4]

  def get_username(self):
    return self.__username

  def get_salt(self):
    return self.__salt

  def get_hash(self):
    return self.__hash


def get_hash_and_salt(password):

    salt = bcrypt.gensalt()
    password = password.encode("utf-8")
    hash = bcrypt.hashpw(password, salt)
    salt = salt.decode("utf-8")
    hash = hash.decode("utf-8")

    return salt, hash
