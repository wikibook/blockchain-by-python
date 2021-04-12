# 파이썬 실습 파일: 5-4.Mining.py
import binascii
import hashlib
import time
from datetime import datetime

# big-endian <--> little-endian으로 변환한다
# 단, x는 hexa-string을 입력한다.
def reverse(x):
    return ''.join(reversed([x[i:i+2] for i in range(0, len(x), 2)]))

# 더블 SHA-256 해시를 계산한다
def doubleSha256(header):
    return hashlib.sha256(hashlib.sha256(header).digest()).digest()

# 블록 헤더를 조립한다
def makeHeader(version, prevHash, merkle, timeStamp, nBits):
    s = reverse(version) + reverse(prevHash) + reverse(merkle) + reverse(timeStamp) + reverse(nBits)
    return s

# 압축형 타겟을 일반형으로 변환한다.
def Uncompact(bits):
    # bit의 왼쪽 1바이트 (exponents)를 추출한다.
    exponents = bits >> 24
    
    # bits의 오른쪽 3바이트 (coefficient)를 추출한다.
    coefficient = bits & 0x007fffff
    
    # target value를 계산한다
    target = coefficient << 8 * (exponents - 3)
    return target

# header 정보
prevHs = '00000000000000000028a9837a638d6ab0b0aa51cd97c87cefd7ca0b5ca55201'
merkle = '5299b7778e8409227af85b00ca4f006717a5d7e90470012779441deea32b67ce'
target = 0x1745fb53
version = '20000000'              # 4 bytes
prevHash = prevHs                 # 32 bytes
merkleRoot = merkle               # 32 bytes
timeStamp = '5ae7502d'            # 4 bytes
nBits = f"{target:#0{10}x}"[2:]   # 4 bytes

# nonce를 제외한 header를 조립한다.
hdr = makeHeader(version, prevHash, merkleRoot, timeStamp, nBits)

# nonce 값을 0 부터 1씩 증가시켜 가면서 header의 Hash 값을 계산한다.
# Hash 값이 nBits 보다 작은 nonce 값을 찾는 것이 목적임.
targetValue = Uncompact(target)

# nonce (=3647874098) 값을 알고 있으므로, 이 주변으로 시험해 본다.
for nonce in range(3647874000, 0xffffffff):
    # nonce 값을 포함한 header를 생성한다
    nS = f"{nonce:#0{10}x}"[2:]
    header = hdr + reverse(nS)

    # Header의 Hash 값을 계산한다
    h = hashlib.sha256(hashlib.sha256(binascii.unhexlify(header)).digest()).digest()
    print(nonce, reverse(h.hex()))
    
    # Hash 값이 nBits 보다 작은지 확인한다
    rh = int(reverse(h.hex()), 16)
    if rh < targetValue:
        # nonce 값을 찾았음.
        break
    
    nonce += 1

print("\n   Version =", version)
print("  prevHash =", prevHash)
print("merkleRoot =", merkleRoot)
print("time stamp = %s [%s]" % (timeStamp, datetime.utcfromtimestamp(int(timeStamp,16)).strftime('%Y-%m-%d %H:%M:%S')))
print("     nBits =", nBits)
print('     nonce = %d <-- Found' % nonce)
print('Header =', header)
print('\nHash =', reverse(h.hex()))

# 10 만번 돌려보고 Hash power를 측정해 본다
startTime = time.time()
for nonce in range(0, 1000000):
    # nonce 값을 포함한 header를 생성한다
    nS = f"{nonce:#0{10}x}"[2:]
    header = hdr + reverse(nS)

    # Header의 Hash 값을 계산한다
    h = hashlib.sha256(hashlib.sha256(binascii.unhexlify(header)).digest()).digest()
    
    # Hash 값이 nBits 보다 작은 지 확인한다
    rh = int(reverse(h.hex()), 16)
    if rh < targetValue:
        # nonce 값을 찾았음.
        break
    nonce += 1

endTime = time.time()
elapsed = endTime - startTime
print('\n\nHash power 측정 :')
print('Elapsed time (100 만회) = %.2f (sec)' % elapsed)
print('Hash power (Python & CPU & i7 processor) = %.2f (hash/sec)' % (nonce / elapsed))
