#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import math
import random
import secrets


def is_prime(n):  
    # Base check
    
    prime_list = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    
    for prime in prime_list:
        if n % prime == 0:
            return False
    
    # Miller-Rabin primality test
    
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    
    for _ in range(128):
        a = random.randrange(2, n - 1)
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


def generate_prime_number(length=1024):
    found_prime = False
    
    while not found_prime:
        p = secrets.randbits(length)
        p |= (1 << length - 1) | 1
        
        found_prime = is_prime(p)
    
    return p


def generate_rsa_public_key(e=17, length=2048):
    prime_length = length // 2
    
    found_modulo = False
    
    while not found_modulo:
        p = generate_prime_number(prime_length)
        q = generate_prime_number(prime_length)
    
        n = p * q
        phi = (p - 1) * (q - 1)
        
        found_modulo = math.gcd(e, phi) == 1
    
    return (n, e)
    
    
def message_to_int(message):
    if isinstance(message, str):
        message = message.encode()
    if isinstance(message, bytes):
        message = int(codecs.encode(message, "hex"), 16)
    message = int(message)
    
    return message


def encrypt(message, n, e):
    c = message_to_int(message)
    
    if c >= n:
        return None
    
    return pow(c, e, n)


if __name__ == "__main__":
    print('''Hello!

Do you want to get my secrets? Yes, I know. 
But I'll encrypt them before giving to you.

Generating key for you...''', end="\r", flush=True)

    n, e = generate_rsa_public_key()

    print(f'''[+] Your personal public key:
    n = {n}
    e = {e}
''', flush=True)

    with open("flag") as flag_file:
        flag = flag_file.read()
        
    encrypted_flag = encrypt(flag, n, e)

    print(f'''[+] Encrypted secret:
    {encrypted_flag}

Thank you for using my service!''', flush=True)
