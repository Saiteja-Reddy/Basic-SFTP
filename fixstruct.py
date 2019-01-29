from struct import *


a = pack('14sh', "helloworld!".encode("ascii"), 212)
b = pack('14sh', "hello".encode("ascii"), 12)

# packet = pack('hh10s10si', 3,12, "hello".encode("ascii"), "password".encode("ascii", 6))
# print(len(packet))


def convertIpToInt(ip):
	return sum([int(ipField) << 8*index for index, ipField in enumerate(reversed(ip.split('.')))])

def convertIntToIp(ipInt):
	return '.'.join([str(int(ipHexField, 16)) for ipHexField in (map(''.join, zip(*[iter(str(hex(ipInt))[2:].zfill(8))]*2)))])


# print(len(a), len(b))

def unpack_message(packet):
	opcode, s_addr, d_addr, buf, ID, q, password, status, file, dummy = unpack('iii10s10si10si10si', packet)
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

	if len(file) > 10:
		print("Choose smaller file!! (<= 10 chars)")
		return "Err";		

	
	packet = pack('iii10s10si10si10si', opcode, s_addr, d_addr, buf.encode("ascii")
		, ID.encode("ascii"), q, password.encode("ascii"), status, file.encode("ascii"), dummy)

	return packet



msg = create_message(file="teja.txt", dummy = 2, opcode = 12, buf = "buf", ID="mysself", q = 12, password = "asdasdasQ", status = 1)
print(msg)
print("\n", unpack_message(msg))
	
