import hashlib
from random import getrandbits

string = "GeeksforGeeks"
salt = getrandbits(6)
prime = 761
string = string + str(salt) + str(prime)
print(string)
result = hashlib.sha1(string.encode()) 
print(result.hexdigest())