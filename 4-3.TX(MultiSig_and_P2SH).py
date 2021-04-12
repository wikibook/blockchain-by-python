# 파이썬 실습 파일: 4-3.TX(MultiSig_and_P2SH).py
# pybitcointools (https://pypi.python.org/pypi/bitcoin)
# pybitcointools를 설치하지 않고 배포용 실습 코드의 bitcoin 폴더가 있는 곳에서 실행한다.
import bitcoin.main as btc
from bitcoin.bci import history
from bitcoin.transaction import mk_multisig_script, scriptaddr, multisign, mktx, apply_multisignatures
from urllib.request import urlopen
from urllib.parse import urlencode
url = "https://testnet.blockchain.info/"

# n-개의 개인키를 만든다
def getPrivKey(n):
    seed = "MultiSig를 시험하기 위해 만든 seed"
    key = []
    for i in range(n):
        privKey = btc.sha256(seed)
        key.append(privKey)
        seed = privKey
    return key

# 개인키 만큼 공개키를 만든다
def getPubKey(privKey):
    key = []
    n = len(privKey)
    for i in range(n):
        pubKey =  btc.privkey_to_pubkey(privKey[i])
        key.append(pubKey)
    return key

# 공개키 리스트로 리딤스크립트를 만든다
def redeemScript(pubKey, n):
    script = mk_multisig_script(pubKey, n)
    return script

# 리딤스크립트로 P2SH 지갑 주소를 만든다. 0xc4 = testnet의 P2SH address
def getAddr(script, magic=0xc4):
    addr = scriptaddr(script, magic)
    return addr

# UTXO를 조회한다
def getUtxo(addr):
    h = history(addr)
    return list(filter(lambda txo: 'spend' not in txo, h))

# Transaction data packet을 생성한다
# input, output을 생성한다.
def makeTx(utxo, aFrom, aTo, value=0.02, fee=0.0001):
    # Input을 만든다
    totValue = 0
    inputs = []
    for i in range(len(utxo)):
        totValue += utxo[i]['value'] * 1e-8
        inputs.append(utxo[i])
        
        # 송금할 금액만큼 UTXO를 선택한다. 최적화는 아니고 앞에서부터 소비한다.
        if totValue > (value + fee):
            break
        
    # 수수료를 차감한 금액을 계산한다
    # 수수료 (Fee)를 뺀 나머지는 myAddr1 으로 재송금한다. (!!! 대단히 중요함 !!!)
    # 재 송금하지 않으면 모두 fee로 간주되어 Miner가 모두 가져간다.
    outChange = totValue - value - fee
    chgSatoshi = int(outChange * 1e8)
    
    # Transaction 데이터 (TX)를 만든다.
    outputs = [{'value': int(value * 1e8), 'address': aTo}, {'value': chgSatoshi, 'address': aFrom}]
    tx = mktx(inputs, outputs)
    return tx

# testnet.blockchain.info API 서버에 TX 전송을 요청한다.
def sendTx(tx):
    params = {'tx': tx}
    payload = urlencode(params).encode('UTF-8')
    response = urlopen(url + 'pushtx', payload).read()
    print(response.decode('utf-8'))

privKey = getPrivKey(3)
pubKey = getPubKey(privKey)
redeem = redeemScript(pubKey, 2)
addr = getAddr(redeem)
print(addr)  # 2NBkVCBVoifBnVxYN3mJtdAvCJkpJNGCLRj

# Alice에게 0.2 BTC를 송금한다
Alice = 'mhJH61ScRnWJrhJm6283BbmACr27FjzT4Y'

# UTXO를 조회한다
utxo = getUtxo(addr)

# Tx 데이터를 생성한다
tx = makeTx(utxo, addr, Alice)

# Signature
sig1 = multisign(tx, 0, redeem, privKey[0])
sig2 = multisign(tx, 0, redeem, privKey[2])
tx2 = apply_multisignatures(tx, 0, redeem, sig1, sig2)

# tx2를 전송한다
#sendTx(tx2)
