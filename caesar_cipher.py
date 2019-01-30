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


# string = "Hello .World!"
# key = 112

# enc = encrypt(string, key)
# print("encrypted: ", enc)

# print(decrypt(enc, key))

