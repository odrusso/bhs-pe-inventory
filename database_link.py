import mysql.connector

class Database(object):

    def __init__(self, config):
        """Defines (and connects to) the Database class.
        Data Attributes:    'db' is the database connection object
                            'cursor' is the database cursor object
        """

        try:
            self.db = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            #Basic Error Management
            print("There was an error connecting to the database.")
            print(err)                                                          #Be sure to change this to an GUI error code eventually
        else:
            self.cursor = self.db.cursor()

    def return_execution(self, query):
        """Returns the value of a SQL query"""
        self.cursor.execute(query)
        return self.cursor

#Testing weather the database connections and can execute a basic query
if __name__ == '__main__':

        #Database configuration and connection
        database_config = {
        "user": "root",
        "password": "root",
        "host": "127.0.0.1",
        "database": "example"
        }

        ExampleDB = Database(database_config)                                   #Inniltalise the Database object

        query = "SELECT * FROM `people`"                                        # Example query
        response = ExampleDB.return_execution(query)

        for (PersonID, FirstName, LastName) in response:                        #Print the returned information
            print("{} {} {}".format(PersonID, FirstName, LastName))
