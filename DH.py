from struct import *

#functions to create fixed size packed for Diffie Hellman Key Exchange

def create_DH_share_pack(Ya, prime, alpha):
	packet = pack('iii', Ya, prime, alpha)
	return packet

def unpack_DH_share_pack(packet):
	Ya, prime, alpha = unpack('iii', packet)
	out = {}
	out['prime'] = prime
	out['Ya'] = Ya
	out['alpha'] = alpha
	return out

def create_DH_reshare_pack(Yb):
	packet = pack('i', Yb)
	return packet

def unpack_DH_reshare_pack(packet):
	Yb = unpack('i', packet)[0]
	out = {}
	out['Yb'] = Yb
	return out
