# 파이썬 실습 파일: 3-8.DeterministicWallet.py
# pybitcointools (https://github.com/vbuterin/pybitcointools)
# pybitcointools를 설치하지 않고 배포용 실습 코드의 bitcoin 폴더가 있는 곳에서 실행한다.
import bitcoin.main as btc

# 초기 Seed 값을 정의한다.
seed = '초기 seed 값입니다.'

# n 개의 개인키를 만든다
n = 5
error = 0
for i in range(1, (n+1)):
    seed += str(i)
    privKey = btc.sha256(seed)
    dPrivKey = btc.decode_privkey(privKey, 'hex')   # 16진수 문자열을 10진수 숫자로 변환한다
    if dPrivKey < btc.N:                            # secp256k1 의 N 보다 작으면 OK
        print("Key (%d) : %s" % (i, privKey))
    else:
        error += 1

if error > 0:
    print("요청하신 seed로 개인키 %d개를 모두 만들지 못했습니다." % n)
