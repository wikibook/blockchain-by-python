# 파이썬 실습 파일: 3-4.공개키(Format).py
# 개인키와 공개키는 파이썬 실습 3.2 공개키 생성에서 생성한 결과를 이용한다.
privKey = '3ba54c096fbb082b2af8efdfd92f886350a36c806296199234d338e8d81b456d'
pubKey = ('484ec026a5a371a4e99cd2258760be98f9662c95b94a49706735e62a1a128855',
          'c7f3b6a8e049d54ab99414b2245fd45bbf5d916a97e56bdd87f7110c95f7bde8')

# secp256k1에 정의된 domain parameter p
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

# 공개키를 Uncompressed format으로 표시한다.
uPubKey = '04' + pubKey[0] + pubKey[1]

# 공개키를 Compressed format으로 표시한다.
if int(pubKey[1], 16) % 2 == 0:
    cPubKey = '02' + pubKey[0]
else:
    cPubKey = '03' + pubKey[0]

# Compressed Format을 (x, y) Format으로 변환한다.
# p % 4 = 3 mod 4 이므로 아래 공식을 적용할 수 있음.
x = int(cPubKey[2:], 16)
a = (pow(x, 3, p) + 7) % p  # y^2
y = pow(a, (p+1)//4, p)     # y

prefix = int(cPubKey[:2], 16)
if (prefix == 2 and y & 1) or (prefix == 3 and not y & 1):
    y = (-y) % p

# 공개키 출력
print("\n Public Key : (%s,\n               %s)" % (pubKey[0], pubKey[1]))

# Uncompressed format 출력
print("\nUncompressed (size = %d):\n%s" % (len(uPubKey)*4, uPubKey))

# Compressed format 출력
print("\nCompressed (size = %d):\n%s" % (len(cPubKey)*4, cPubKey))

print("\nCompressed format --> Public key :")
print("\n Public Key : (%s,\n               %s)" % (hex(x)[2:], hex(y)[2:]))


