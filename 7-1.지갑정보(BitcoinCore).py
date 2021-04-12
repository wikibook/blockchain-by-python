# 파이썬 실습 파일: 7-1.지갑정보(BitcoinCore).py
# pybitcointools (https://github.com/vbuterin/pybitcointools)
# pybitcointools를 설치하지 않고 배포용 실습 코드의 bitcoin 폴더가 있는 곳에서 실행한다.
import base58
import binascii
import bitcoin.main as btc
import bitcoin.segwit_addr as bech32

# 비트코인 코어에서 지갑 주소로 WIF 개인키를 조회한다
# 디버그 콘솔 : dumpprivkey "지갑 주소"
# 주소의 상세 내역 조회 : validateaddress "지갑 주소"
privKeyWIF = "L1iJWxsPa6iSYuPC9mvYzL5SCjHiDhVHPhS5Gz1wJy3fLN6qPwgD"
wifDecode = base58.b58decode(privKeyWIF).hex()

# pybitcointool로 키를 변환한다
# 참조 : pybitcointools (https://pypi.python.org/pypi/bitcoin)
# WIF 개인키를 일반 개인키로 변환한다.
privKey = btc.b58check_to_hex(privKeyWIF)

# 개인키로 공개키를 생성한다.
pubKey = btc.privkey_to_pubkey(privKey)

# 공개키로 160-bit public key hash를 생성한다
pubHash160 = btc.hash160(binascii.unhexlify(pubKey))

# P2SH용 스크립트를 생성한다. script = OP_0 + length + public key hash
script = '00' + '14' + pubHash160

# 160 비트 스크립트 해시를 계산한다
scriptHash = btc.hash160(binascii.unhexlify(script))

# 스크립트 해시로 지갑 주소를 생성한다.
addr = btc.hex_to_b58check(scriptHash, 0x05)

# BIP-173 주소를 생성한다.
# 참조: https://github.com/sipa/bech32/blob/master/ref/python/segwit_addr.py
witprog = btc.bin_hash160(binascii.unhexlify(pubKey))
bech32Addr = bech32.encode('bc', 0, witprog)

# 결과를 확인한다
print("Decode WIF = ", wifDecode)
print("Private Key = ", privKey)
print("Public Key = ", pubKey)
print("Public Key Hash = ", pubHash160)
print("Script = ", script)
print("ScriptHash = ", scriptHash)
print("Address = ", addr)
print("Bech32 Address = ", bech32Addr)



