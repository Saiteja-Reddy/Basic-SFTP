import socket
import MR
from random import randrange
from struct import *
from DH import *

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

prime, alpha = MR.get_Prime_PR() # public
print("Generated Prime Number is " + str(prime))
Xa = randrange(2, prime - 2)
print("Selected Private Xa as " + str(Xa))
print("Generator is " + str(alpha))
Ya = pow(alpha, Xa, prime) # public
print("Ya is " + str(Ya))

DH_share_pack = create_DH_share_pack(Ya, prime, alpha)
print("Sending to Server", unpack_DH_share_pack(DH_share_pack))

s.sendall(DH_share_pack)
DH_reshare_pack = s.recv(calcsize('i'))
DH_data = unpack_DH_reshare_pack(DH_reshare_pack)
print(DH_data)

key = pow(DH_data['Yb'], Xa , prime)
print("key is " + str(key))
print("Done Diffie-Hellmann!!")





# print('Received', repr(data))