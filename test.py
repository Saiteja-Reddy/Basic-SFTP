import MR
from random import randrange

# print(MR.generate_prime_number())

A_q, A_alpha = MR.get_Prime_PR() # public
print("A: generate_prime_number " + str(A_q))
Xa = randrange(2, A_q - 2)
print("A: select Xa " + str(Xa))
print("A: alpha " + str(A_alpha))

Ya = pow(A_alpha, Xa, A_q) # public
print("A: Ya " + str(Ya))

print("B:")
B_q = A_q
Yb = Ya
B_alpha = A_alpha
Xb = randrange(2, B_q - 2)
print("B: select Xb " + str(Xb))

Yb = pow(B_alpha, Xb, B_q) # public
print("B: Yb " + str(Yb))

K_a = pow(Yb, Xa ,A_q)
print("A: key is " + str(K_a))

K_b = pow(Ya, Xb ,B_q)
print("B: key is " + str(K_b))

print("Sucess - Diffie Hellman Key Exchange!!")





