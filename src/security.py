# utf-8
# Python 3.5.1, scrypt
# Software developed by Oscar Russo
# http://github.com/odrusso/bhs-pe-inventory

# Provides functions and objects for encryption and decryption of usernames and passwords in the bhs-pe-inventory project

import scrypt # Imports the scrypt library which handles the encryption and decryption of passwords
from os import urandom # Imports the urandom from the OS library which is able to generate a random hash

def gen_password(password):
    """Function to generate a salt and salted hash from a given password"""
    salt = str(urandom(16)) # Generates a random salt
    hash = str(scrypt.hash(password, salt)) # Generates a salted hash
    return (salt, hash) # Retruns the salt and hash in a tuple

def verify_password(salt, hash, password):
    """Function to verify if a password matches a given salt and salted hash"""
    new_hash = str(scrypt.hash(password, salt)) # Creates a new hash based on the input salt and password
    if str(new_hash) == str(hash): # Checks to see if the new hash is the same as the given hash
        return True
    else:
        return False

def manual_password(password):
    """Function to manually generate new passwords"""
    salt, hash = gen_password(password) # Uses the gen_password() function to generate a password
    print("Password: " + password) # Prints the inputed password
    print("Salt: " + salt) # Prints the salt
    print("Hash: " + hash) # Prints the salted hash

if __name__ == "__main__":
    print("This program is not designed to run standalone")
    manual_password("test") # An example test-cast to generate a salt and hash form the pasword 'test'
