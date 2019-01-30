import socket
import MR
from random import randrange
from struct import *
from DH import *
from message import *
from caesar_cipher import *
from constants import *


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

prime, alpha = MR.get_Prime_PR() # public
Xa = randrange(2, prime - 2)
Ya = pow(alpha, Xa, prime) # public

DH_share_pack = create_DH_share_pack(Ya, prime, alpha)

s.sendall(DH_share_pack)
DH_reshare_pack = s.recv(calcsize('i'))
DH_data = unpack_DH_reshare_pack(DH_reshare_pack)

key = pow(DH_data['Yb'], Xa , prime)
print("key is " + str(key))
print("prime is " + str(prime))
print("Done Diffie-Hellmann!!")

logged_user = ""

while True:
	if logged_user == "":
		action = input('> ')
	else:
		action = input(logged_user + '> ')

	if action == "newlogin":
		user = input('Enter ID of user: ')
		password = input('Enter password of user: ')
		user = encrypt(user, key)
		password = encrypt(password, key)
		msg = create_message(opcode = LOGINCREAT, ID=user, password = password)
		if(msg == "Err"):
			continue
		print("Sent LOGINCREAT Message", unpack_message(msg))
		s.sendall(msg)
		msg = s.recv(calcsize('iii10s10si10si80si'))
		msg = unpack_message(msg)        
		print("Received LOGINREPLY from Server")
		if msg['status'] == 0:
			print('Already in use login - ' + str(decrypt(user, key)))
			print('Choose a different username.')
		else:
			print('Created new user login - ' + str(decrypt(user, key)))
			print('You can now login with this username.')

	elif action == "login":
		if logged_user != "":
			print("Log out first before new login!!")
			continue
		user = input('Enter ID of user: ')
		password = input('Enter password of user: ')
		user = encrypt(user, key)
		password = encrypt(password, key)
		msg = create_message(opcode = AUTHREQUEST, ID=user, password = password)
		if(msg == "Err"):
			continue
		print("Sent AUTHREQUEST Message", unpack_message(msg))
		s.sendall(msg)
		msg = s.recv(calcsize('iii10s10si10si80si'))
		msg = unpack_message(msg) 						
		print("Received AUTHREPLY from Server")
		if msg['status'] == 0:
			print('No such user found - ' + str(decrypt(user, key)))
			print('Create a new login.')
		elif msg['status'] == -1:
			print('Wrong password entered for user - ' + str(decrypt(user, key)))			
		else:
			print('Successfully Logged in as - ' + str(decrypt(user, key)))
			logged_user = decrypt(user, key)

	elif action == "getfile":
		if logged_user == "":
			print("Log in first before getfile!!")
			continue
		filename = input('Enter file path on server: ')
		user = encrypt(logged_user, key)
		msg = create_message(opcode = SERVICEREQUEST, ID=user, file = filename)
		if(msg == "Err"):
			continue
		print("Sent SERVICEREQUEST Message", unpack_message(msg))
		s.sendall(msg)
		msg = s.recv(calcsize('iii10s10si10si80si'))
		msg = unpack_message(msg)
		print(msg)						
		if(msg['status'] == -1):
			print("File doesn't exist on server!!")
			continue
		else:
			f = open(msg['file'], 'w')
			f.write(msg['buf'])
			while msg['status'] == 0:
				msg = s.recv(calcsize('iii10s10si10si80si'))
				msg = unpack_message(msg)
				f.write(msg['buf'])
				print(msg)
			f.close()
			print("Done Transferring File from server!!!")


	elif action == "quit" or action == "exit":
		exit()

	elif action == "logout":
		logged_user = ""
		print('User is now logged out.')

	else:
		print("No such action!!")
		print("Choose one among the below actions:")
		print("""1. login\n2. newlogin\n3. getfile\n4. logout\n5. quit/exit""")
