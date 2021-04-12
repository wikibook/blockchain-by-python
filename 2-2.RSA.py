# 파이썬 실습 파일: 2-2.RSA.py
from Crypto.PublicKey import RSA

# Private key와 Public key 쌍을 생성한다.
# Private key는 소유자가 보관하고, Public key는 공개한다. 
keyPair = RSA.generate(2048)
privKey = keyPair.exportKey()   # 키 소유자 보관용
pubKey = keyPair.publickey()    # 외부 공개용

# keyPair의 p,q,e,d를 확인해 본다
keyObj = RSA.importKey(privKey)
print("p = ", keyObj.p)
print("q = ", keyObj.q)
print("e = ", keyObj.e)
print("d = ", keyObj.d)

# 암호화할 원문
plainText = 'This is Plain text. It will be encrypted using RSA.'
print()
print("원문 :")
print(plainText)

# 공개키로 원문을 암호화한다.
cipherText = pubKey.encrypt(plainText.encode(), 10)
print("\n")
print("암호문 :")
print(cipherText[0].hex())

# Private key를 소유한 수신자는 자신의 Private key로 암호문을 해독한다.
# pubKey와 쌍을 이루는 privKey 만이 이 암호문을 해독할 수 있다.
key = RSA.importKey(privKey)
plainText2 = key.decrypt(cipherText) 
plainText2 = plainText2.decode()
print("\n")
print("해독문 :")
print(plainText2)


