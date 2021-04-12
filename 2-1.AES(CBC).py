# 파이썬 실습 파일: 2-1.AES(CBC).py
from Crypto.Cipher import AES
from Crypto import Random
import numpy as np

# 대칭키를 만든다. 대칭키는 128-bit, 192-bit, 256-bit를 사용할 수 있다.
secretKey128 = b'0123456701234567'
secretKey192 = b'012345670123456701234567'
secretKey256 = b'01234567012345670123456701234567'

# 128-bit key를 사용한다.
secretKey = secretKey128
plainText = 'This is Plain text. It will be encrypted using AES with CBC mode.'
print("\n\n")
print("원문 :")
print(plainText)

# CBC 모드에서는 plain text가 128-bit (16 byte)의 배수가 되어야 하므로, padding이 필요함.
# padding으로 NULL 문자를 삽입함. 수신자는 별도로 padding을 제거할 필요없음.
n = len(plainText)
if (n % 16) != 0:
    n = n + 16 - (n % 16)
    plainText = plainText.ljust(n, '\0')
    
# initialization vector. iv도 수신자에게 보내야 한다.
iv = Random.new().read(AES.block_size)
ivcopy = np.copy(iv) # 수신자에게 보낼 복사본

# 송신자는 secretKey와 iv로 plainText를 암호문으로 변환한다.
iv = Random.new().read(AES.block_size)
ivcopy = np.copy(iv)
aes = AES.new(secretKey, AES.MODE_CBC, iv)
cipherText = aes.encrypt(plainText)
print("\n\n\n")
print("암호문 :")
print(cipherText.hex())

# 암호문, secretKey, ivcopy를 수신자에게 보내면, 수신자는 암호문을 해독할 수 있다.
aes = AES.new(secretKey, AES.MODE_CBC, ivcopy)
plainText2 = aes.decrypt(cipherText)
plainText2 = plainText2.decode()
print("\n\n\n")
print("해독문 :")
print(plainText2)
