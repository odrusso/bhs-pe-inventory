"""Module for connecting to the database, viewing, and inserting information."""
import mysql.connector
from sql_viewer import ErrorGUI, LoadingGUI

class Database(object):

    def __init__(self, config):
        """Defines (and connects to) the Database class.
        Data Attributes:    'db' is the database connection object
                            'cursor' is the database cursor object
        """
        try:
            print("Connecting to Server...")
            self.db = mysql.connector.connect(**config)
        except mysql.connector.Error as e:
            #Basic Error Management
            error_popup = ErrorGUI(e)                                                        #Be sure to change this to an GUI error code eventually
        else:
            self.cursor = self.db.cursor()
            print("Connected")

    def return_execution(self, query):
        """Returns the value of a SQL query"""
        self.cursor.execute(query)
        return self.cursor

    def add_person(self, id, first_name, last_name):
        query = "INSERT INTO `people` (`PersonID`, `FirstName`, `LastName`) VALUES ('{}', '{}', '{}')".format(id, first_name, last_name)
        try:
            self.cursor.execute(query)
            self.db.commit()
        except Exception as e:
            error_popup = ErrorGUI(e)

#Testing weather the database connections and can execute a basic query
if __name__ == '__main__':

        #Database configuration and connection
        database_config = {
        "user": "root",
        "password": "5sQ-Hsd-ekt-bzS",
        "host": "bhs-pe-inventory.ci3pushvdxiu.us-west-2.rds.amazonaws.com",
        "database": "test"
        }
        # 5sQ-Hsd-ekt-bzS

        ExampleDB = Database(database_config)                                   #Inniltalise the Database object

        query = "SELECT * FROM `people`"                                        # Example query
        response = ExampleDB.return_execution(query)

        for (PersonID, FirstName, LastName) in response:                        #Print the returned information
            print("{} {} {}".format(PersonID, FirstName, LastName))
