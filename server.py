import socket
import threading 
import time
import MR
from random import *
from DH import *
from struct import *
from message import *
from caesar_cipher import *
from constants import *
import hashlib


pass_file = {}
  
def check_creds(id, password):
    global pass_file
    password = password + str(pass_file[id]['salt']) + str(pass_file[id]['prime'])
    password = hashlib.sha1(password.encode()).hexdigest()
    if pass_file[id]['password'] == password:
        return 1;
    return -1;

# thread fuction 
def threaded(conn): 
    DH_share_pack = conn.recv(calcsize('iii'))
    DH_data = unpack_DH_share_pack(DH_share_pack)
    Xb = randrange(2, DH_data['prime'] - 2)
    
    Yb = pow(DH_data['alpha'], Xb, DH_data['prime']) # public to A

    DH_reshare_pack = create_DH_reshare_pack(Yb)
    conn.sendall(DH_reshare_pack)

    prime = DH_data['prime']
    key = pow(DH_data['Ya'], Xb , prime)

    print("key is " + str(key))
    print("prime is " + str(prime))
    print("Done Diffie-Hellmann!!\n")

    while True:
        msg = conn.recv(calcsize('iii10s10si10si10si'))
        msg = unpack_message(msg)
        print("Received from client: ", msg)

        if msg['opcode'] == LOGINCREAT:
            ID = decrypt(msg['ID'], key)
            password = decrypt(msg['password'], key)
            print(ID, password)
            # add to table
            salt = abs(getrandbits(6))
            password = password + str(salt) + str(prime)
            password = hashlib.sha1(password.encode()).hexdigest()

            if ID in pass_file.keys():
                msg = create_message(opcode = LOGINREPLY, status = 0)
                print("Sent LOGINREPLY Message", unpack_message(msg))
                conn.sendall(msg)
            else:
                pass_file[ID] = {'password' : password, 'prime' : prime, 'salt' : salt}
                print(pass_file)
                msg = create_message(opcode = LOGINREPLY, status = 1)
                print("Sent LOGINREPLY Message", unpack_message(msg))
                conn.sendall(msg) 

        elif msg['opcode'] == AUTHREQUEST:            
            ID = decrypt(msg['ID'], key)
            password = decrypt(msg['password'], key)
            print(ID, password)
            #check in table
            if ID not in pass_file.keys():
                msg = create_message(opcode = AUTHREPLY, status = 0)
                print("Sent AUTHREPLY Message", unpack_message(msg))
                conn.sendall(msg) 
            else:
                status = check_creds(ID, password)
                msg = create_message(opcode = AUTHREPLY, status = status)
                print("Sent AUTHREPLY Message", unpack_message(msg))
                conn.sendall(msg) 


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