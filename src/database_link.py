"""Module for connecting to the database, viewing, and inserting information."""
import mysql.connector

def db_local_users():
    return {
        "user": "root",
        "password": "root",
        "host": "localhost",
        "database": "users"}

def db_local_data():
    return {
        "user": "root",
        "password": "root",
        "host": "localhost",
        "database": "data"}

def df_remote_data():
    return {
    "user": "root",
    "password": "5sQ-Hsd-ekt-bzS",
    "host": "bhs-pe-inventory.ci3pushvdxiu.us-west-2.rds.amazonaws.com:",
    "database": "test"
    }

class InventoryDatabase(object):

    def __init__(self, config):
        """Defines (and connects to) the Database class.
        Data Attributes:    'db' is the database connection object
                            'cursor' is the database cursor object
        """
        try:
            self.db = mysql.connector.connect(**config)
        except mysql.connector.Error as e:
            print(e)
            #Basic Error Management
            # error_popup = ErrorGUI(e)                                                        #Be sure to change this to an GUI error code eventually
        else:
            self.cursor = self.db.cursor(buffered=True)

    def return_execution(self, query):
        """Returns the value of a SQL query"""
        self.cursor.execute(query)
        return self.cursor

    def add_item(self, name, quantity):
        query = "INSERT INTO `inventory` (`Name`, `Quantity`) VALUES ('{}', '{}')".format(name, quantity)
        try:
            self.cursor.execute(query)
            self.db.commit()
        except Exception as e:
            #error_popup = ErrorGUI(e)
            print(e)

class UserDatabase(object):

    def __init__(self, config):
        """Defines (and connects to) the Database class.
        Data Attributes:    'db' is the database connection object
                            'cursor' is the database cursor object
        """
        try:
            self.db = mysql.connector.connect(**config)
        except mysql.connector.Error as e:
            print(e)
        else:
            self.cursor = self.db.cursor(buffered=True)

    def get_user(self, username):
        query = 'SELECT * FROM `Users` WHERE username = "' + username + '"'
        users_raw = self.cursor.execute(query)
        user = self.cursor.fetchone()
        if user != None:
            return user
        else:
            return None

    def add_user(self, name, username, password, permission):
        #add new users to username, salt, hash, perm, name
        pass

    def delete_user(self, username):
        #delete user from username field
        pass




#Testing weather the database connections and can execute a basic query
if __name__ == '__none__':

        #Database configuration and connection
        inv_db = InventoryDatabase(db_local_data())
        user_db = UserDatabase(db_local_users())                                #Inniltalise the Database object

        query = "SELECT * FROM `inventory`"                                     # Example query
        response = inv_db.return_execution(query)

        text_table = ''
        for (ItemID, Name, Quantity) in response:                               #Print the returned information
            text_table += "{} {} {} \n".format(ItemID, Name, Quantity)
        print(text_table)

if __name__ == "__main__":
    user_db = UserDatabase(db_local_users())
    print(user_db.get_user("admin"))
