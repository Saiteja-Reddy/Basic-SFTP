from random import randrange, getrandbits
import math

def is_prime(n, k=128):
    """ Test if a number is prime
        Args:
            n -- int -- the number to test
            k -- int -- the number of tests to do
        return True if n is prime
    """
    # Test if n is not even.
    # But care, 2 is prime !
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True

def generate_prime_candidate(length):
    """ Generate an odd integer randomly
        Args:
            length -- int -- the length of the number to generate, in bits
        return a integer
    """
    # generate random bits
    p = getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p

def generate_prime_number(length=26):
    """ Generate a prime
        Args:
            length -- int -- length of the prime to generate, in          bits
        return a prime
    """
    p = 4
    # keep generating while the primality test fail
    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
    return p
# print(generate_prime_number())


def find_prime_factors(num):
    pf = set([])
    while(num % 2 == 0):
        pf.add(2)
        num //=2

    for i in range(3, int(math.sqrt(num))+1):
        while num % i == 0:
            pf.add(i)
            num //=i

    if num > 2:
        pf.add(num)

    # print(num, pf)
    return pf;

def get_Prime_PR():
    prime = generate_prime_number()
    phi = prime - 1
    pfs = find_prime_factors(phi)

    for i in range(2, phi+1):
        flag = False
        for fact in pfs:
            if pow(i, int(phi/fact), prime) == 1:
                flag = True
                break
        if flag == False:
            # print("Primitive Root is " + str(i))
            return (prime, i)
            # break
    return get_Prime_PR()




