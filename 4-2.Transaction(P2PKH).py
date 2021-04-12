# 파이썬 실습 파일: 4-2.Transaction(P2PKH).py
# pybitcointools (https://pypi.python.org/pypi/bitcoin)
# pybitcointools를 설치하지 않고 배포용 실습 코드의 bitcoin 폴더가 있는 곳에서 실행한다.
from bitcoin.bci import history
from bitcoin.transaction import mktx, sign
from urllib.request import urlopen
from urllib.parse import urlencode

url = "https://testnet.blockchain.info/"
A = 0   # Alice
B = 1   # Bob
address = ['mhJH61ScRnWJrhJm6283BbmACr27FjzT4Y', 'mg5urjMQZpALgga9GmwZaiiKKyBftxe7Mt']
privKey = ['7c06fcd8b6d7ef34182dd86882f5f1f1834381c132653b4f6937065167062b10', '8126b6e1b33432198cbf9139174b470285b085fd4a0ccb6cc439f31cdbf3d298']

# 써드파티 API 서버에게 UTXO를 요청한다
def getUtxo(n=A):
    if n == A or n == B:
        h = history(address[n])
        return list(filter(lambda txo: 'spend' not in txo, h))
    else:
        print("address error.")

# Transaction data packet을 생성한다
# input, output을 생성한다.
def makeTx(utxo, n1=A, n2=B, value=0.01, fee=0.0001):
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
    outputs = [{'value': int(value * 1e8), 'address': address[n2]}, {'value': chgSatoshi, 'address': address[n1]}]
    tx = mktx(inputs, outputs)
    return tx, len(inputs)

# 송금자의 private key로 서명한다. ScriptSig를 생성한다.
def signTx(utxo, tx, nInput=1, nPriv=A):
    for i in range(nInput):
        tx = sign(tx, i, privKey[nPriv])
    return tx

# 써드파티 API 서버에게 TX 전송을 요청한다.
def sendTx(tx):
    params = {'tx': tx}
    payload = urlencode(params).encode('UTF-8')
    response = urlopen(url + 'pushtx', payload).read()
    print(response.decode('utf-8'))


