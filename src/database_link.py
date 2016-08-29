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
        except Exception as e:
            print(e)

    def return_execution(self, query):
        """Returns the value of a SQL query"""
        self.cursor = self.db.cursor(buffered=True) # Defines the cursor object of the database
        self.cursor.execute(query) # Takes the query prarameter and attempts to execute it on the database
        cursor_raw = list(self.cursor) # Assigns the value of the MySQL cursor
        self.cursor.close() # Closes the cursor to keep program clean
        return cursor_raw # Returns the value of the cursor

    def cursor_execute(self, query):
        """Simply executes an SQL query, keeps clean cursor object"""
        self.cursor = self.db.cursor(buffered=True) # Defines the cursor object of the database
        self.cursor.execute(query) # Executes the query
        self.db.commit() # Commits the value to the database
        self.cursor.close() # Closes the cursor

    def add_item(self, id, name, quantity, location_id):
        """Adds an item into the inventory datatable"""
        query = "INSERT INTO `inventory` (`ItemID`,`Name`, `Quantity`, `LocationID`) VALUES ({}, '{}', {}, {})".format(id, name, quantity, location_id) # Defines the query
        self.cursor_execute(query) # Executes the query on the database
        self.db.commit() # Commits the query to the database (aka saves the database)

    def remove_item(self, id):
        """Removes an item from the database"""
        query = "DELETE FROM `Inventory` WHERE `ItemID` IN ('{}')".format(id) # Defines the query
        self.cursor_execute(query) # Executes the query on the database

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
        query = "SELECT `Room` FROM Rooms" # Defines the query
        raw_return = self.return_execution(query) # Gets the raw value of the query
        room_list = [] # Defines room_list to be an empty list
        for room in raw_return:
            room_list.append(room[0]) # Adds the room name to the room list
        return room_list # Returns the room list

    def return_location_list(self):
        """Returns a list of all locations"""
        query = "SELECT `StorageLocation` FROM `Locations`" # Defines the query
        raw_return = self.return_execution(query) # Gets the raw value of the query
        location_list = [] # Defines location list to be an empty list
        for i in raw_return:
            location_list.append(i[0]) # Adds the location name to the location list
        return location_list # Returns the list of locations

    def return_location_dictionary(self):
        """Returns a dictionary of rooms and their locations as a dictionary"""
        rooms = self.return_room_list() # Gets the list of roms
        location_dict = {} # Defines empty location dict dictionary
        for (id, room) in enumerate(rooms):
            id += 1
            query = "SELECT `StorageLocation` FROM Locations WHERE `RoomID` = " + str(id) # Defines the query
            raw_return = self.return_execution(query) # Gets the raw value of the query
            new_locations = [] # Defines new_locations as an empty list
            for location in raw_return:
                new_locations.append(location[0]) # Append the location to the new_locations list
            location_dict[room] = new_locations # Adds the new location list to the reletive room in the dictionary
        return location_dict # Returns the dictionary

    def add_room(self, room_name):
        """Adds a room to the inventory database"""
        room_id = len(self.return_room_list()) + 1 # Gets the next value for the room ID
        query = "INSERT INTO `Rooms` (`RoomID`, `Room`) VALUES ({}, '{}')".format(room_id, room_name) # Defines the query
        self.cursor_execute(query) # Executes the query on the database
        self.db.commit() # Commits the changes to the database
        print(self.return_room_list)

    def add_location(self, location_name, room_name):
        """Adds a new location to the inventory database"""
        location_id = len(self.return_location_list()) + 1 # Gets the value for the location_id
        query = 'SELECT `RoomID` FROM `Rooms` WHERE `Room` = "' + str(room_name) + '"' # Defines the query
        room_id = self.return_execution(query)[0][0] # Gets the value of the room_id
        query = "INSERT INTO `Locations` (`LocationID`, `RoomID`, `StorageLocation`) VALUES ({}, {}, '{}')".format(location_id, room_id, location_name) # Defines the query
        self.cursor_execute(query) # Executes the query on the database

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

    def cursor_execute(self, query):
        """Simply executes an SQL query, keeps clean cursor object"""
        self.cursor = self.db.cursor(buffered=True) # Defines the cursor object of the database
        self.cursor.execute(query) # Executes the query on the database
        self.db.commit() # Commits the data to the database
        self.cursor.close() # Closes the cursor

    def return_execution(self, query):
        """Returns the value of a SQL query"""
        self.cursor = self.db.cursor(buffered=True) # Defines the cursor object of the database
        self.cursor.execute(query) # Takes the query prarameter and attempts to execute it on the database
        cursor_raw = list(self.cursor) # Assigns the value of the MySQL cursor
        self.cursor.close() # Closes the cursor to keep program clean
        return cursor_raw # Returns the value of the cursor

    def get_user(self, username):
        """Returns a list of user attrubtes from a username prarameter"""
        query = 'SELECT * FROM `Users` WHERE username = "' + username + '"' # Defines the query
        user = self.return_execution(query) # Executes the query on the database
        if user != None: # Checks for a valid user
            return user[0]
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

    inv_db.add_location("Random Box", "PE Office")
