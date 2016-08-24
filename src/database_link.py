# utf-8
# Python 3.5.1, mysql
# Software developed by Oscar Russo
# http://github.com/odrusso/bhs-pe-inventory

# Provides functions and objects for the use of database in the bhs-pe-inventory project

import mysql.connector # Imports the connection functions from the mysql library
from db_configs import * # Imports the database connection configurations

class InventoryDatabase(object):
    def __init__(self):
        """Object instanced to connect, query, and modify the Inventory datatable of a MySQL database
        Main Data Attributes:       'db' is the database connection object
                                    'cursor' is the database cursor object
        """
        try:
            config = db_local_data() # Currently uses the local inventory database
            self.db = mysql.connector.connect(**config) # Attempts to connect to the database
            self.cursor = self.db.cursor(buffered=True) # Defines the cursor object of the database
        except Exception as e:
            print(e)

    def return_execution(self, query):
        """Returns the value of a SQL query"""
        self.cursor.execute(query) # Takes the query prarameter and attempts to execute it on the database
        return self.cursor # Returns the value of the MySQL cursor

    def add_item(self, id, name, quantity, location_id):
        """Adds an item into the inventory datatable"""
        query = "INSERT INTO `inventory` (`ItemID`,`Name`, `Quantity`, `LocationID`) VALUES ({}, '{}', {}, {})".format(id, name, quantity, location_id) # Defines the query
        self.cursor.execute(query) # Executes the query on the database
        self.db.commit() # Commits the query to the database (aka saves the database)

    def return_all_list(self):
        """Returns a list of all relevant data in the inventory datatable"""
        query = """SELECT n.ItemID, n.Name, n.Quantity, s.Issued, l.StorageLocation, r.Room
                FROM Inventory n
                LEFT JOIN Issues s ON n.ItemID=s.ItemID
                LEFT JOIN Locations l on n.LocationID=l.LocationID
                LEFT JOIN Rooms r on l.RoomID=r.RoomID"""

        inventory_raw = self.return_execution(query) # Executes the query on the database
        new_data = [] # Defines empty list for the non-cursor object data
        for (id, name, quantity, issued, storagelocation, room) in inventory_raw:
            new_data.append([id, name, quantity, issued, storagelocation, room]) # Appends the clean data to the new_data list
        return new_data # Retrusn the new_data list

    def return_room_list(self):
        """Returns a list of all of the defined rooms in the datatable"""
        query = "SELECT `Room` FROM Rooms"
        raw_return = self.return_execution(query)
        room_list = []
        for room in raw_return:
            room_list.append(room[0])
        return room_list

    def return_location_dictionary(self):
        """Returns a dictionary of rooms and their locations as a dictionary"""
        rooms = self.return_room_list()
        location_dict = {}
        for (id, room) in enumerate(rooms):
            query = "SELECT `StorageLocation` FROM Locations WHERE `RoomID` = " + str(id)
            raw_return = self.return_execution(query)
            new_locations = []
            for location in raw_return:
                new_locations.append(location[0])
            location_dict[room] = new_locations

        return location_dict

class UserDatabase(object):
    def __init__(self):
        """Object instanced to connect, query, and modify the Users datatable of a MySQL database
        Main Data Attributes:       'db' is the database connection object
                                    'cursor' is the database cursor object
        """
        try:
            config = db_local_users() # Currently uses the local user database
            self.db = mysql.connector.connect(**config) # Attempts to connect to the database
            self.cursor = self.db.cursor(buffered=True) # Defines the cursor object of the database
        except Exception as e:
            print(e)

    def get_user(self, username):
        """Returns a list of user attrubtes from a username prarameter"""
        query = 'SELECT * FROM `Users` WHERE username = "' + username + '"' # Defines the query
        users_raw = self.cursor.execute(query) # Executes the query on the database
        user = self.cursor.fetchone() # Gets the value if just 1 users
        if user != None: # Checks for a valid user
            return user
        else:
            return None

    def add_user(self, name, username, password, permission):
        """Adds a new user to the user datatable"""
        #add new users to username, salt, hash, perm, name
        pass

    def delete_user(self, username):
        """Deletes a user from the user datatable"""
        #delete user from username field
        pass

#Testing weather the database connects and can execute a basic query
if __name__ == '__main__':
    print("This program is not designed to run standalone")

    #Database configuration and connection
    inv_db = InventoryDatabase()
    user_db = UserDatabase()

    values = inv_db.return_all_list() # Gets all of the relevant inventory data

    print(len(values))
    for i in values:
        print(i)

    print(inv_db.return_location_dictionary())
