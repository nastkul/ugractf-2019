#!/usr/bin/env python3

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"
FLAG_ENC = "BwnJ_aREnPhT_YJkd_iJNYan"
FLAG_PREFIX = "ugra"

def l2n(c):
    # letter → number [0..52]
    return ALPHABET.index(c)

def n2l(n):
    # number [0..52] → letter
    return ALPHABET[n]

def encrypt(n, a, b, c, d):
    return (a * n ** 3 + b * n ** 2 + c * n + d) % len(ALPHABET)

def brute():
    for a in range(len(ALPHABET)):
        for b in range(len(ALPHABET)):
            for c in range(len(ALPHABET)):
                for d in range(len(ALPHABET)):
                    for p, e in zip(FLAG_PREFIX, FLAG_ENC):
                        if n2l(encrypt(l2n(p), a, b, c, d)) != e:
                            break
                    else:
                        return a, b, c, d

a, b, c, d = brute()
print("Found coefficients:", a, b, c, d, flush=True)

mapping_back = {}
print("\nReplacement rules:")
for p in ALPHABET:
    e = n2l(encrypt(l2n(p), a, b, c, d))
    print(f"    {p} → {e}")
    mapping_back[e] = p
print(flush=True)

flag = ''.join(map(mapping_back.get, FLAG_ENC))
print("Flag:", flag)
