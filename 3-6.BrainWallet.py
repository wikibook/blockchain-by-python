# 파이썬 실습 파일: 3-6.BrainWallet.py
# pybitcointools (https://github.com/vbuterin/pybitcointools)
# pybitcointools를 설치하지 않고 배포용 실습 코드의 bitcoin 폴더가 있는 곳에서 실행한다.
import bitcoin.main as btc

# 특정 문자열로 256-bit 개인키를 생성한다 (long brain wallet passphrase).
passphrase = 'Brain Wallet 시험용 개인키입니다. 잊어버리지 마세요.'
privKey = btc.sha256(passphrase)
dPrivKey = btc.decode_privkey(privKey, 'hex')   # 16진수 문자열을 10진수 숫자로 변환한다
if dPrivKey < btc.N:                            # secp256k1 의 N 보다 작으면 OK
    # 개인키로 공개키를 생성한다.
    pubKey = btc.privkey_to_pubkey(privKey)
    
    # 공개키로 지갑 주소를 생성한다. (mainnet 용)
    address = btc.pubkey_to_address(pubKey, 0)
        
    # 결과 확인
    print("\n\nPassphrase :", passphrase)
    print("\n개인키 :", privKey)
    print("개인키 --> 공개키 :", pubKey)
    print("\n공개키 --> 지갑주소 :", address)
else:
    print("요청하신 Passphrase로 개인키를 만들었으나, 유효하지 않습니다.")
    print("다른 Passphrase로 다시 시도해 주세요.")

