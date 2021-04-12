# 파이썬 실습 파일: 5-1.BlockHeader.py
import binascii
import hashlib
from datetime import datetime

# big-endian <--> little-endian으로 변환한다
# x는 hexa-string을 입력한다.
def reverse(x):
    return ''.join(reversed([x[i:i+2] for i in range(0, len(x), 2)]))

def doubleSha256(header):
    return hashlib.sha256(hashlib.sha256(header).digest()).digest()

def makeHeader(version, prevHash, merkle, timeStamp, nBits, nonce):
    h = str(hex(nonce))[2:]
    s = reverse(version) + reverse(prevHash) + reverse(merkle) + reverse(timeStamp) + reverse(nBits) + reverse(h)
    return s
#blockchain.info/rawblock/00000000000000000017b762584c2e48a8f80855d8f954d90584d9bb4e7320ef?format=hex 
# 최근 생성된 블록의 헤더 데이터를 아래와 같이 hex format으로 조회한다.
# 블록헤더의 해시 = 00000000000000000017b762584c2e48a8f80855d8f954d90584d9bb4e7320ef 
# blockchain.info/rawblock/블록헤더의 해시?format=hex
# 조회한 데이터의 앞 부분 80 byte만 사용한다.
#header = '0000402064445f7643fb2720c36e6b9e1d5255cd30146e128dd617000000000000000000278f00317a2b7c174a613f2706c6b8d9c4f71ffda1098b489b7d645ed90a16c8156a485c33d62f17345e0812'
header = '00000020cfbf17b954f7baae49bff3a19fba1bef2032ff73384c1f0000000000000000007d4ced56ee79b139ab53ff4fd5be2ac022aaaff9ed5ca168a55547725acb935d233c485c33d62f17ff7b256a'

# Header hash를 계산하고 blockchain.info의 결과와 비교해 본다
h = doubleSha256(binascii.unhexlify(header))
print("Header Hash = ", reverse(h.hex()))

# header를 decode한다.
version = reverse(header[0:0 + 4 * 2])        # 4 bytes
prevHash = reverse(header[8: 8 + 32 * 2])     # 32 bytes
merkleRoot = reverse(header[72: 72 + 32 * 2]) # 32 bytes
timeStamp = reverse(header[136: 136 + 4 * 2]) # 4 bytes
nBits = reverse(header[144: 144 + 4 * 2])     # 4 bytes
nonce = reverse(header[152: 152 + 4 * 2])     # 4 bytes

print("\n\nHeader =", header)
print("\n\n   Version =", version)
print("  prevHash =", prevHash)
print("  currHash =", reverse(h.hex()))
print("merkleRoot =", merkleRoot)
print("time stamp = %s [%s]" % (timeStamp, datetime.utcfromtimestamp(int(timeStamp,16)).strftime('%Y-%m-%d %H:%M:%S')))
print("     nBits =", nBits)
print("     nonce =", int(nonce, 16))

# 다시 header로 조립한다
hdr = makeHeader(version, prevHash, merkleRoot, timeStamp, nBits, int(nonce, 16))
print("\n\nHeader =", hdr)
