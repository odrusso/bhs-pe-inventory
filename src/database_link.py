# utf-8
# Python 3.5.1, MySQL
# Software developed by Oscar Russo
# http://github.com/odrusso/bhs-pe-inventory

# Provides functions and objects for the use of database in the bhs-pe-inventory project

import mysql.connector # Imports the connection functions from the mysql library
import sqlite3 # Imports the connection functions from the sqline3 library
from db_configs import * # Imports the database connection configurations
import security # Imports the securty program
import threading # Imports the threading library
from time import sleep # Imports the sleep function from the time library
from pickle import loads, dumps # Imports the loads and dumps pickles from the pickle library

class InventoryDatabase(object):
    def __init__(self, handler):
        """Object instanced to connect, query, and modify the Inventory datatable of a MySQL database
        Main Data Attributes:       'db' is the database connection object
                                    'cursor' is the database cursor object
        """
        self.handler = handler
        remote_config = db_local_data() # Currently uses the local inventory database
        local_config = "./data/inv_local.db"
        try:
            #self.db = mysql.connector.connect(**remote_config) # Attempts to connect to the database
            self.db = sqlite3.connect(local_config)
            cursor = self.db.cursor()
            #cursor.execute("SELECT VERSION()")
            #results = cursor.fetchone()
        except Exception as e:
            print("Offline Mode or Config Error")
            print(e)

    def cursor_execute(self, query):
        """Simply executes an SQL query, keeps clean cursor object"""
        self.cursor = self.db.cursor() # Defines the cursor object of the database
        if type(query) == type(""):
            self.cursor.execute(query) # Executes the query on the database
            self.handler.add_query(query, "inv")
        elif type(query) == type(("example", "example")):
            self.cursor.execute(query[0], query[1]) # Uses the pramaterization insertion
            self.handler.add_param(query[0], query[1], "inv")
        self.db.commit() # Commits the data to the database
        self.cursor.close() # Closes the cursor

    def return_execution(self, query):
        """Returns the value of a SQL query"""
        self.cursor = self.db.cursor() # Defines the cursor object of the database
        self.cursor.execute(query) # Takes the query prarameter and attempts to execute it on the database
        cursor_raw = list(self.cursor) # Assigns the value of the MySQL cursor
        self.cursor.close() # Closes the cursor to keep program clean
        return cursor_raw # Returns the value of the cursor

    def add_item(self, id, name, quantity, location_id):
        """Adds an item into the inventory datatable"""
        query = 'INSERT INTO `inventory` (`ItemID`, `Name`, `Quantity`, `LocationID`) VALUES ({}, "{}", {}, {})'.format(id, name, quantity, location_id) # Defines the query
        self.cursor_execute(query) # Executes the query on the database
        self.db.commit() # Commits the query to the database (aka saves the database)

    def remove_item(self, id):
        """Removes an item from the database"""
        query = 'DELETE FROM `Inventory` WHERE `ItemID` IN ("{}")'.format(id) # Defines the query
        self.cursor_execute(query) # Executes the query on the database

    def modify_item(self, id, field, new_data):
        """Takes information and updates an item in the database"""
        query = 'UPDATE `Inventory` SET {} = "{}" WHERE `ItemID` = {}'.format(field, new_data, id) # Defines the query
        self.cursor_execute(query) # Executes the query on the database

    def issue_item(self, id):
        """Takes item ID and sets it to Issued"""
        query = "UPDATE `Inventory` SET Issued = 1 WHERE `ItemID` = {}".format(id)
        self.cursor_execute(query)

    def return_item(self, id):
        """Takes item ID and sets it to Issued"""
        query = "UPDATE `Inventory` SET Issued = 0 WHERE `ItemID` = {}".format(id)
        self.cursor_execute(query)

    def return_all_list(self):
        """Returns a list of all relevant data in the inventory datatable"""
        query = """SELECT n.ItemID, n.Name, n.Quantity, s.Issued, l.StorageLocation, r.Room, n.Issued
                FROM Inventory n
                LEFT JOIN Issues s ON n.ItemID=s.ItemID
                LEFT JOIN Locations l on n.LocationID=l.LocationID
                LEFT JOIN Rooms r on l.RoomID=r.RoomID"""

        inventory_raw = self.return_execution(query) # Executes the query on the database
        new_data = [] # Defines empty list for the non-cursor object data
        for (id, name, quantity, issued, storagelocation, room, issued) in inventory_raw:
            new_data.append([id, name, quantity, issued, storagelocation, room, issued]) # Appends the clean data to the new_data list
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
        query = 'INSERT INTO `Rooms` (`RoomID`, `Room`) VALUES ({}, "{}")'.format(room_id, room_name) # Defines the query
        self.cursor_execute(query) # Executes the query on the database
        self.db.commit() # Commits the changes to the database

    def add_location(self, location_name, room_name):
        """Adds a new location to the inventory database"""
        location_id = len(self.return_location_list()) + 1 # Gets the value for the location_id
        query = 'SELECT `RoomID` FROM `Rooms` WHERE `Room` = "' + str(room_name) + '"' # Defines the query
        room_id = self.return_execution(query)[0][0] # Gets the value of the room_id
        query = 'INSERT INTO `Locations` (`LocationID`, `RoomID`, `StorageLocation`) VALUES ({}, {}, "{}")'.format(location_id, room_id, location_name) # Defines the query
        self.cursor_execute(query) # Executes the query on the database

class UserDatabase(object):
    def __init__(self, handler):
        """Object instanced to connect, query, and modify the Users datatable of a MySQL database
        Main Data Attributes:       'db' is the database connection object
                                    'cursor' is the database cursor object
        """
        self.handler = handler
        remote_config = db_local_data() # Currently uses the local inventory database
        local_config = "./data/usr_local.db"
        try:
            #self.db = mysql.connector.connect(**remote_config) # Attempts to connect to the database
            self.db = sqlite3.connect(local_config)
            cursor = self.db.cursor()
            #cursor.execute("SELECT VERSION()")
            #results = cursor.fetchone()
        except Exception as e:
            print("Local DB Config Error")

    def cursor_execute(self, query):
        """Simply executes an SQL query, keeps clean cursor object"""
        self.cursor = self.db.cursor() # Defines the cursor object of the database
        if type(query) == type(""):
            self.cursor.execute(query) # Executes the query on the database
            self.handler.add_query(query, "usr")
        elif type(query) == type(("example", "example")):
            self.cursor.execute(query[0], query[1]) # Uses the pramaterization insertion
            self.handler.add_param(query[0], query[1], "")
        self.db.commit() # Commits the data to the database
        self.cursor.close() # Closes the cursor

    def return_execution(self, query):
        """Returns the value of a SQL query"""
        self.cursor = self.db.cursor() # Defines the cursor object of the database
        self.cursor.execute(query) # Takes the query prarameter and attempts to execute it on the database
        cursor_raw = list(self.cursor) # Assigns the value of the MySQL cursor
        self.cursor.close() # Closes the cursor to keep program clean
        return cursor_raw # Returns the value of the cursor

    def get_user(self, username):
        """Returns a list of user attrubtes from a username prarameter"""
        value = None
        query = "SELECT * FROM `Users` WHERE username = 'admin'" # Defines the query
        local_user_db = self.return_execution("SELECT `username` FROM `Users`")
        local_users = []
        for username in local_user_db:
            local_users.append(username[0])
        try:
            user_config = db_local_users() # Defines the database config
            usr_db = mysql.connector.connect(**user_config) # Connects to the database
        except:
            print("There was an error connecting to the user database")
            user = self.return_execution(query)
            if user != []: # Checks for a valid user
                value = user[0]
            else:
                value = None
        else:
            usr_cursor = usr_db.cursor(buffered=True) # Defines the query
            raw = usr_cursor.execute(query) # Executes the query
            user = usr_cursor.fetchone() # Converts the query to a list
            if user != None: # Checks for a valid user
                value = user
            else:
                value = None
        finally:
            value = list(value)
            if type(value[1]) == type(b'example'):
                value[1] = value[1].decode()
            if value[1] in local_users:
                return value
            else:
                self.add_local_user(value)
                return value

    def add_local_user(self, args):
        new_args = (args[1].decode(), args[2], args[3], args[4], args[5])
        query = 'INSERT INTO `Users` (`username`, `salt`, `hash`, `perm`, `name`) VALUES (?, ?, ?, ?, ?)'
        self.cursor_execute((query, new_args))

    def add_user(self, name, username, password, permission):
        """Adds a new user to the user datatable"""
        #add new users to username, salt, hash, perm, name
        salt, hash = security.gen_password(password)
        query = ('INSERT INTO `Users` (`username`, `salt`, `hash`, `perm`, `name`) VALUES (?, ?, ?, ?, ?)', (username, salt, hash, permission, name))
        self.cursor_execute(query)
        online_query = 'INSERT INTO `Users` (`username`, `salt`, `hash`, `perm`, `name`) VALUES (%s, %s, %s, %s, %s)'
        self.handler.add_param(online_query, query[1], "usr")

    def delete_user(self, username):
        """Deletes a user from the user datatable"""
        #delete user from username field
        pass

class DatabaseSync(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        while True:
            changes = self.return_queries()
            if len(changes) != 0:
                try:
                    data_config = db_local_data()
                    self.inv_db = mysql.connector.connect(**data_config)
                    self.inv_cursor = self.inv_db.cursor()

                    user_config = db_local_users()
                    self.usr_db = mysql.connector.connect(**user_config)
                    self.usr_cursor = self.usr_db.cursor()

                    for (change_id, change_query, change_db, params) in changes:
                        if params == None:
                            if change_db == "inv":
                                self.inv_cursor.execute(change_query)
                                self.inv_db.commit()
                            elif change_db == "usr":
                                self.usr_cursor.execute(change_query)
                                self.usr_db.commit()
                        else:
                            if change_db == "inv":
                                unpick_params = loads(params)
                                self.inv_cursor.execute(change_query, unpick_params)
                                self.inv_db.commit()
                            elif change_db == "usr":
                                unpick_params = loads(params)
                                self.usr_cursor.execute(change_query, unpick_params)
                                self.usr_db.commit()
                        print("Succesfull sync with databasse")
                        self.dump_query(change_id)
                except RuntimeError as e:
                    print("There was an error syncing with the database")
                    print(e)
            sleep(1)

    def add_query(self, query, database):
        changes_db = sqlite3.connect("./data/changes_local.db")
        changes_cursor = changes_db.cursor()
        new_query = "INSERT INTO `Changes` (`Query`, `Database`) VALUES ('{}', '{}')".format(query, database) # Defines the query
        changes_cursor.execute(new_query)
        changes_db.commit()

    def add_param(self, query, params, database):
        changes_db = sqlite3.connect("./data/changes_local.db")
        changes_cursor = changes_db.cursor()
        pickle_params = dumps(params)
        new_query = 'INSERT INTO `Changes` (`Query`, `Database`, `Params`) VALUES (?, ?, ?)' # Defines the query
        changes_cursor.execute(new_query, (query, database, pickle_params))
        changes_db.commit()

    def return_queries(self):
        changes_db = sqlite3.connect("./data/changes_local.db")
        changes_cursor = changes_db.cursor()
        query = "SELECT * FROM `Changes`"
        changes_cursor.execute(query)
        dump = list(changes_cursor)
        return dump

    def dump_query(self, change_id):
        changes_db = sqlite3.connect("./data/changes_local.db")
        changes_cursor = changes_db.cursor()
        query = "DELETE FROM `Changes` WHERE `ChangeNum` = {}".format(change_id)
        changes_cursor.execute(query)
        changes_db.commit()

#Testing weather the database connects and can execute a basic query
if __name__ == '__main__':
    print("This program is not designed to run standalone")

    sync = DatabaseSync()
    sync.start()
