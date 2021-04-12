# 파이썬 실습 파일: 3-1.개인키(생성).py
import os
import random
import time
import hashlib

# secp256k1의 Domain parameter (order of G)
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# CSPRNG 방식, os.urandom()와 random()를 적당히 섞어서 hash256으로 256bit 난수를 생성한다.
def random_key():
    r = str(os.urandom(32)) \
        + str(random.randrange(2**256)) \
        + str(int(time.time() * 1000000))
    r = bytes(r, 'utf-8')
    h = hashlib.sha256(r).digest()
    key = ''.join('{:02x}'.format(y) for y in h)
    return key

# secp256k1의 n값보다 작으면 된다.
while (1):
    privKey = random_key()
    if int(privKey, 16) < N:
        break

print("PrivKey (Hex) : ", privKey)
print("PrivKey (Dec) : ", int(privKey, 16))

