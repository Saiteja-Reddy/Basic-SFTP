import socket
import threading 
import time
  
# thread fuction 
def threaded(conn): 
    while True:
        data = conn.recv(1024)
        # time.sleep(5)
        if not data:
            break
        conn.sendall(data)
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