string = "GeeksforGeeks"

key = 1

dict = {}

for i in range(65, 65 + 26):
	dict[chr(i)] =  i-65

dict[','] = 27
dict['.'] = 28
dict['?'] = 29

for i in range(48, 48 + 10):
	dict[chr(i)] =  i-18

for i in range(97, 97 + 26):
	dict[chr(i)] =  i-57


dict['!'] = 66

print(dict)

