# 파이썬 실습 파일: 2-4.ECC(PublicKey).py
import math

# Additive Operation
def addOperation(a, b, p, q, m):
    if q == (math.inf, math.inf):
        return p
    
    x1 = p[0]
    y1 = p[1]
    x2 = q[0]
    y2 = q[1]
    
    if p == q:
        # Doubling
        # slope (s) = (3 * x1 ^ 2 + a) / (2 * y1) mod m
        # 분모의 역원부터 계산한다 (by Fermat's Little Theorem)
        # pow() 함수가 내부적으로 Square-and-Multiply 알고리즘을 수행한다.
        r = 2 * y1
        rInv = pow(r, m-2, m)   # Fermat's Little Theorem
        s = (rInv * (3 * (x1 ** 2) + a)) % m
    else:
        r = x2 - x1
        rInv = pow(r, m-2, m)   # Fermat's Little Theorem
        s = (rInv * (y2 - y1)) % m
    x3 = (s ** 2 - x1 - x2) % m
    y3 = (s * (x1 - x3) - y1) % m
    return x3, y3

# Domain parameter를 정의한다.
# y^2 = x^3 + 2 * x + 2 mod 231559
a = 2
b = 2
p = 32416189381   # Prime number 이어야 함.
G = (5,1)

# 개인키를 선택한다. P보다 작은 임의의 숫자를 선택한다.
# 실제는 순환군 범위내에서 선택한다. 이 부분은 지갑 (Wallet)편에서 다룬다.
d = 1234567    # Private Key

# Double-and-Add 알고리즘으로 공개키를 생성한다
bits = bin(d)
bits = bits[2:len(bits)]

# initialize. bits[0] = 1 (always)
K = G

# 두 번째 비트부터 Double-and-Add
bits = bits[1:len(bits)]
for bit in bits:
    # Double
    K = addOperation(a, b, K, K, p)
    
    # Multiply
    if bit == '1':
        K = addOperation(a, b, K, G, p)
            
privKey = d
pubKey = K

print("\nDomain parameters : (P, a, b, G)")
print("P = %d" % p)
print("a = %d" % a)
print("b = %d" % b)
print("G = (%d, %d)" % (G[0], G[1]))
print("EC : y^2 = x^3 + %d * x + %d mod %d" % (a, b, p))
print("\nKeys :")
print("Private Key = ", privKey)
print("Public Key = %d * (%d, %d) = (%d, %d)" % (d, G[0], G[1], pubKey[0], pubKey[1]))

