import scrypt
import os

password = input("Enter New Password: ")

salt = str(os.urandom(16))
print("Salt: " + salt)
hash = str(scrypt.hash(password, salt))
print("Hash: " + hash)
