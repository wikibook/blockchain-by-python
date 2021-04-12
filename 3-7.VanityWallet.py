# 파이썬 실습 파일: 3-7.VanityWallet.py
# pybitcointools (https://github.com/vbuterin/pybitcointools)
# pybitcointools를 설치하지 않고 배포용 실습 코드의 bitcoin 폴더가 있는 곳에서 실행한다.
import bitcoin.main as btc

bFound = False
for i in range(10000):
    # 개인키를 생성한다
    while (1):
        privKey = btc.random_key()                      # 256 bit Random number를 생성한다
        dPrivKey = btc.decode_privkey(privKey, 'hex')   # 16진수 문자열을 10진수 숫자로 변환한다
        if dPrivKey < btc.N:                            # secp256k1 의 N 보다 작으면 OK
            break
    
    # 개인키로 공개키를 생성한다.
    pubKey = btc.privkey_to_pubkey(privKey)
    
    # 공개키로 지갑 주소를 생성한다. (mainnet 용)
    address = btc.pubkey_to_address(pubKey, 0)
    
    # 지갑 주소 앞 부분 원하는 문자열인지 확인한다
    if address[1:4] == 'ABC':
        bFound = True
        break

if bFound:
    # 결과 확인
    print("\n\n개인키 : ", privKey)
    print("\n개인키 --> 공개키 : ", pubKey)
    print("\n공개키 --> 지갑주소 : ", address)
else:
    print("찾지 못했습니다. 다시 시도해 주세요")


