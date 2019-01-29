import socket
import threading 
import time
import MR
from random import randrange
from DH import *
from struct import *
  
# thread fuction 
def threaded(conn): 
    DH_share_pack = conn.recv(calcsize('iii'))
    DH_data = unpack_DH_share_pack(DH_share_pack)
    print(DH_data)
    Xb = randrange(2, DH_data['prime'] - 2)
    print("Selected Private Xb as " + str(Xb))
    
    Yb = pow(DH_data['alpha'], Xb, DH_data['prime']) # public to A
    print("Yb is " + str(Yb)) 

    DH_reshare_pack = create_DH_reshare_pack(Yb)
    print("Sending to Server", unpack_DH_reshare_pack(DH_reshare_pack))
    conn.sendall(DH_reshare_pack)

    prime = DH_data['prime']
    key = pow(DH_data['Ya'], Xb , prime)

    print("key is " + str(key))
    print("Done Diffie-Hellmann!!\n")


    conn.close() 

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
while True: 
    conn, addr = s.accept()
    print('Connected by', addr)
    t = threading.Thread(target=threaded, args=(conn,))
    t.start() 
s.close() 