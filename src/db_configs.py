# utf-8
# Python 3.5.1
# Software developed by Oscar Russo
# http://github.com/odrusso/bhs-pe-inventory

# Simple program to store the different database configurations

def db_local_users():
    """Returns the config information for the users table of a local database"""
    config =  {
        "user": "root",
        "password": "root",
        "host": "localhost",
        "database": "users"
        }
    return config

def db_local_data():
    """Returns the config information for the inventory table of a local database"""
    config = {
        "user": "root",
        "password": "root",
        "host": "localhost",
        "database": "data"
        }
    return config

def db_remote_data():
    """Returns the config information for the users table of a remote database"""
    config = {
    "user": "root",
    "password": "5sQ-Hsd-ekt-bzS",
    "host": "bhs-pe-inventory.ci3pushvdxiu.us-west-2.rds.amazonaws.com:",
    "database": "test"
    }
    return config

def db_remote_users():
    """Returns the config information for the users table of a remote database"""
    config = {
    "user": "root",
    "password": "5sQ-Hsd-ekt-bzS",
    "host": "bhs-pe-inventory.ci3pushvdxiu.us-west-2.rds.amazonaws.com:",
    "database": "users"
    }
    return config
