import mysql.connector

class Database(object):

    def __init__(db, cursor):
        """Defines (and connects to) the Database class.
        Data Attributes:    'db' is the database connection object
                            'cursor' is the database cursor object
        """
        self.db = db
        self.cursor = cursor

try:
    #Database configuration and connection
    database_config = {
    "user": "root",
    "password": "root",
    "host": "127.0.0.1",
    "database": "example"
    }
    self.db = mysql.connector.connect(**database_config)
except mysql.connector.Error as err:
    #Basic Error Management
    print("There was an error connecting to the database.")
    print(err) #Be sure to change this to an GUI error code eventually
