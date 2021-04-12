# 파이썬 실습 파일: 2-3.ECC(Group).py
import math
import numpy as np
import matplotlib.pyplot as plt

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
    
# y^2 = x^3 + 2 * x + 2 mod 127
a = 2
b = 2
m = 127   # Prime number 이어야 함.
P = (5,1)
Q = P

allPoints = [P]
while(1):
    # R이 P의 inverse인지 확인한다. inverse이면 infinity 지점임
    # A = (x1, y1), B = (x2, y2) 일 때 x1 = x2 이고 y1 과 y2가 
    # (mod m)에 대해 additive inverse 이면 infinity
    if (Q[0] == P[0]) & (abs(Q[1] - m) == P[1]):
        # 다음부터 cyclic 되므로 여기서 멈춤.
        break
    else:
        R = addOperation(a, b, P, Q, m)
        allPoints.append(R)
        Q = R

x, y = np.array(allPoints).T
plt.figure(figsize=(8,6))
plt.scatter(x, y, marker='o', color='green', alpha=0.5, s=150)
plt.show()
print(allPoints)