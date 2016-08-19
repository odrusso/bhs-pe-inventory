"""Module for handling the encryption and decryption of the usernames and passwords used in BHS PE Inventory"""
import scrypt
import os
from database_link import *

def gen_password(password):
    salt = str(os.urandom(16))
    hash = str(scrypt.hash(password, salt))
    return (salt, hash)

def verify_password(salt, hash, password):
    new_hash = str(scrypt.hash(password, salt))
    if str(new_hash) == str(hash):
        return True
    else:
        return False




#ns, nh = gen_password("admin")
#print(ns)
#print(nh)
