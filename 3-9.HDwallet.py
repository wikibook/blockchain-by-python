# 파이썬 실습 파일: 3-9.HDWallet.py
# pybitcointools (https://github.com/vbuterin/pybitcointools)
# pybitcointools를 설치하지 않고 배포용 실습 코드의 bitcoin 폴더가 있는 곳에서 실행한다.
import bitcoin.main as btc
import bitcoin.deterministic as det

# seed 값인 단어 목록 (Mnemonic words)를 임의로 설정하고
# Master private key와 master public key를 생성한다.
seed = b'ksLee hlpark shcho previous andante apple solee clk learn'
mPrv = det.bip32_master_key(seed)  # master private key
mPub = det.bip32_privtopub(mPrv)   # master public key

# 계층-1의 extended private key와 public key를 생성한다.
# Depth-1 (m=0, m/1)
xPrv01 = det.bip32_ckd(mPrv, 1)     # 마스터 개인키로 Depth-1의 개인키를 생성한다
xPub01 = det.bip32_ckd(mPub, 1)     # 마스터 공개키로 Depth-1의 공개키를 생성한다

# 계층-2의 extended private key와 public key를 생성한다.
# Depth-2 (m/1/0)
xPrv010 = det.bip32_ckd(xPrv01, 0)  # Depth-1의 개인키로 Depth-2의 개인키를 생성한다
xPub010 = det.bip32_ckd(xPub01, 0)  # Depth-1의 공개키로 Depth-2의 공개키를 생성한다

# 계층-3의 extended private key와 public key를 생성한다.
# Depth-3 (m/1/0/0)
xPrv0100 = det.bip32_ckd(xPrv010, 0) # Depth-2의 개인키로 Depth-3의 개인키를 생성한다
xPub0100 = det.bip32_ckd(xPub010, 0) # Depth-2의 공개키로 Depth-3의 공개키를 생성한다

# Address (m/1/0/0)
prv0100 = det.bip32_extract_key(xPrv0100)
pub0100 = det.bip32_extract_key(xPub0100)
adr0100 = btc.pubkey_to_address(pub0100, 0x00) # Depth-3의 공개키로 주소를 생성한다

# 결과 출력
print("\nDepth-3 (m/1/0/0) :")
print("\nxPrivate Key =", xPrv0100)
print("\nxPublic Key =", xPub0100)
print("\nPrivate Key =", prv0100)
print("Public Key =", pub0100)
print("Address =", adr0100)

# Depth-3의 공개키는 Private key로 생성한 것이 아님. Depth-2의 공개키로 생성한 것임.
# 그럼에도 불구하고 아래 관계가 성립해야함.
# prv0100 --> pub0100 관계를 확인한다.
pubKey = btc.privkey_to_pubkey(prv0100)
if pubKey == pub0100:
    print("\nPrivate Key --> Public Key 관계가 잘 성립함.")
else:
    print("\nPrivate Key --> Public Key 관계가 성립하지 않음.")

# Depth-3 (m/1/0/1~5)
print("\nDepth-3의 지갑 주소는 개인키 없이도 무수히 만들어 낼 수 있음.")
for i in range(1, 8):
    xPub_i = det.bip32_ckd(xPub010, i)
    pubKey_i = det.bip32_extract_key(xPub_i)
    adr_i = btc.pubkey_to_address(pubKey_i, 0x00)
    print("m/1/0/%d : %s" % (i, adr_i))
    