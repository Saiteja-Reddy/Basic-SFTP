from struct import *

def convertIpToInt(ip):
	return sum([int(ipField) << 8*index for index, ipField in enumerate(reversed(ip.split('.')))])

def convertIntToIp(ipInt):
	return '.'.join([str(int(ipHexField, 16)) for ipHexField in (map(''.join, zip(*[iter(str(hex(ipInt))[2:].zfill(8))]*2)))])

def unpack_message(packet):
	opcode, s_addr, d_addr, buf, ID, q, password, status, file, dummy = unpack('iii10s10si10si80si', packet)
	out = {}
	out['opcode'] = opcode
	out['s_addr'] = s_addr
	out['d_addr'] = d_addr
	out['buf'] = buf.decode("ascii").rstrip('\x00')
	out['ID'] = ID.decode("ascii").rstrip('\x00')
	out['q'] = q
	out['password'] = password.decode("ascii").rstrip('\x00')
	out['status'] = status
	out['file'] = file.decode("ascii").rstrip('\x00')
	out['dummy'] = dummy
	return out

def create_message(opcode = 10,
		s_addr = convertIpToInt("127.0.0.1"),
		d_addr = convertIpToInt("127.0.0.1"),
		buf = "",
		ID = "",
		q = -1,
		password = "",
		status = 0,
		file = "",
		dummy = -1
	):

	if len(buf) > 10:
		print("Choose smaller message!! (<= 10 chars)")
		return "Err";
	
	if len(ID) > 10:
		print("Choose smaller ID!! (<= 10 chars)")
		return "Err";	

	if len(password) > 10:
		print("Choose smaller password!! (<= 10 chars)")
		return "Err";	

	if len(file) > 80:
		print("Choose smaller file path!! (<= 10 chars)")
		return "Err";		

	
	packet = pack('iii10s10si10si80si', opcode, s_addr, d_addr, buf.encode("ascii")
		, ID.encode("ascii"), q, password.encode("ascii"), status, file.encode("ascii"), dummy)

	return packet

def get_encoding():
	dict = {}
	r_dict = {}

	dict[' '] = 00
	r_dict[0] = ' '


	for i in range(65, 65 + 26):
		dict[chr(i)] =  i-64
		r_dict[i-64] =  chr(i)

	dict[','] = 27
	dict['.'] = 28
	dict['?'] = 29
	r_dict[27] = ','
	r_dict[28] = '.'
	r_dict[29] = '?'

	for i in range(48, 48 + 10):
		dict[chr(i)] =  i-18
		r_dict[i-18] =  chr(i)

	for i in range(97, 97 + 26):
		dict[chr(i)] =  i-57
		r_dict[i-57] =  chr(i)


	dict['!'] = 66
	r_dict[66] = '!'
	# print(dict)
	# print(r_dict)
	return (dict, r_dict)

def encrypt(string, key):
	dict, r_dict = get_encoding()
	keys = list(dict.keys())
	# print(keys)
	out = ""
	for char in string:
		if char not in keys:
			# print("Err: Invalid character")
			return -1
		else:
			now = dict[char]
			fin = ((now + key) % 67)
			# print(fin)
			out += r_dict[fin]
	return out

def decrypt(string, key):
	dict, r_dict = get_encoding()
	keys = list(dict.keys())
	# print(keys)
	out = ""
	for char in string:
		if char not in keys:
			# print("Err: Invalid character")
			return -1
		else:
			now = dict[char]
			fin = ((now - key) % 67)
			out += r_dict[fin%67]
	return out

# msg = create_message(file="teja.txt", dummy = 2, opcode = 12, buf = "buf", ID="mysself", q = 12, password = "asdasdasQ", status = 1)
# print(msg)
# print("\n", unpack_message(msg))