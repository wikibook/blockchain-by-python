# 파이썬 실습 파일: 4-4.AnyoneCanSpend.py
# 배포용 실습 코드의 bitcoin 폴더가 있는 곳에서 실행한다.
# txid = c586389e5e4b3acb9d6c8be1c19ae8ab2795397633176f5a6442a261bbdefc3a
# 사례를 통해 Anyone-Can-Spend 결과를 확인한다.
import binascii
import bitcoin.main as btc

# P2WPKH nested in P2SH
# scriptSig: <0x0014{20-byte-key-hash}>, 0x0014는 20 바이트의 길이임.
scriptSig = '0014a4b4ca48de0b3fffc15404a1acdc8dbaae226955'

# utxo = 42f7d0545ef45bd3b9cfee6b170cf6314a3bd8b3f09b610eeb436d92993ad440 : 1
# script hash는 위 utxo의 두 번째 출력부에 기록돼 있음.
# OP_HASH160 <script hash> OP_EQUAL
scriptHash = '2928f43af18d2d60e8a843540d8086b305341339'

# combined script
print ('\n\n사례 : txid = c586389e5e4b3acb9d6c8be1c19ae8ab2795397633176f5a6442a261bbdefc3a')
print("\nCombined Script (without Witness) :")
print("\n<%s> OP_HASH160 <%s> OP_EQUAL" % (scriptSig, scriptHash))

# Validity check : OP_HASH160
check = btc.bin_hash160(binascii.unhexlify(scriptSig))

# OP_EQUAL
if check.hex() == scriptHash:
    print("\n==> Valid Script")
else:
    print("\n==> Invalid Script")
