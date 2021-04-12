# 파이썬 실습 파일: 4-5.Bech32Address.py
# https://github.com/sipa/bech32/blob/master/ref/python/segwit_addr.py
# 배포용 실습 코드의 bitcoin 폴더가 있는 곳에서 실행한다.
import binascii
import bitcoin.main as btc
import bitcoin.segwit_addr as bech32

# 개인키를 생성한다
while (1):
    privKey = btc.random_key()                      # 256 bit Random number를 생성한다
    dPrivKey = btc.decode_privkey(privKey, 'hex')   # 16진수 문자열을 10진수 숫자로 변환한다
    if dPrivKey < btc.N:                            # secp256k1 의 N 보다 작으면 OK
        break
privKey='860ef116221744a5299c99a0ed726c15a2148a21a341fe522399c84a59771cfe01'
# 개인키로 공개키를 생성한다. Compressed format.
pubKey = btc.privkey_to_pubkey(privKey)
cPubKey = btc.compress(pubKey)

# 공개키로 160-bit public key hash를 생성한다
witprog = btc.bin_hash160(binascii.unhexlify(cPubKey))

# BIP-173 주소를 생성한다. (Base32 address format for native v0-16 witness outputs)
# P2WPKH
mainnetAddr = bech32.encode('bc', 0, witprog)
testnetAddr = bech32.encode('tb', 0, witprog)

# 결과
print("\n\n공개키 :", cPubKey)
print("Bech32 주소 (Mainnet P2WPKH) :", mainnetAddr)
print("Bech32 주소 (Testnet P2WPKH) :", testnetAddr)

print("\n\nBIP-173 문서의 Example 확인")
print("==========================")
cPubKey = '0279BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798'

# 공개키로 160-bit public key hash를 생성한다
witprog = btc.bin_hash160(binascii.unhexlify(cPubKey))

# BIP-173 주소를 생성한다. (Base32 address format for native v0-16 witness outputs)
mainnetAddr = bech32.encode('bc', 0, witprog)
testnetAddr = bech32.encode('tb', 0, witprog)
print("\n공개키 :", cPubKey)
print("Bech32 주소 (Mainnet P2WPKH) :", mainnetAddr)
print("Bech32 주소 (Testnet P2WPKH) :", testnetAddr)

