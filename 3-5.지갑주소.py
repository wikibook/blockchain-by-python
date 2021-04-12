# 파이썬 실습 파일: 3-5.지갑주소.py
# pybitcointools를 설치하지 않고 배포용 실습 코드의 bitcoin 폴더가 있는 곳에서 실행한다.
import bitcoin.main as btc

# 개인키를 생성한다
while (1):
    privKey = btc.random_key()                      # 256 bit Random number를 생성한다
    dPrivKey = btc.decode_privkey(privKey, 'hex')   # 16진수 문자열을 10진수 숫자로 변환한다
    if dPrivKey < btc.N:                            # secp256k1 의 N 보다 작으면 OK
        break

# 개인키로 공개키를 생성한다.
pubKey = btc.privkey_to_pubkey(privKey)

# 공개키로 지갑 주소를 생성한다. (mainnet 용)
address1 = btc.pubkey_to_address(pubKey, 0)

# 공개키로 160-bit public key hash를 생성한다
pubHash160 = btc.hash160(btc.encode_pubkey(pubKey, 'bin'))

# 160-bit public key hash로 지갑 주소를 생성한다. (위의 address와 동일하다)
address2 = btc.hex_to_b58check(pubHash160, 0)

# 지갑 주소를 160-bit public key hash로 변환한다. (위의 pubHash160과 동일하다)
pubHash1601 = btc.b58check_to_hex(address2)

# 공개키로 testnet용 지갑 주소를 생성한다
address3 = btc.pubkey_to_address(pubKey, 0x6f)

# 결과 확인
print("\n\n개인키 : ", privKey)
print("개인키 --> 공개키 : ", pubKey)
print("\n공개키 --> 지갑주소 (1. mainet 용) : ", address1)
print("공개키 --> 공개키 해시 : ", pubHash160)
print("\n공개키 해시 --> 지갑주소 (2. mainet 용) : ", address2)
print("지갑주소 --> 공개키 해시 : ", pubHash1601)
print("지갑주소 (Testnet 용) :", address3)


