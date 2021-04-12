# 파이썬 실습 파일: 7-9.TxFee.py
# RPC 패키지 : https://github.com/petertodd/python-bitcoinlib
from bitcoin.rpc import RawProxy
import matplotlib.pyplot as plt

# Bitcoin Core에 접속한다.
p = RawProxy()

def getUtxo(x, n):
    tt = p.getrawtransaction(x, True)
    return tt['vout'][n]['value']

# 블록체인 tip (끝 부분)의 hash, height를 읽어온다
tip = p.getchaintips()

# 마지막 블록을 읽어온다
height = tip[0]['height']
bHash = tip[0]['hash']
block = p.getblock(bHash)

# 마지막 블록의 Tx를 읽는다.
nTx = len(block['tx'])
    
# Tx를 차례대로 읽어가면서 Fee를 계산한다. (Coinbase Tx는 제외)
txFee = []
byteFee = []
accByteFee = []
cnt = 0
for i in range(1, nTx):
    txid = block['tx'][i]
    tx = p.getrawtransaction(txid, True)
    
    # total Input value를 계산한다
    nIn = len(tx['vin'])
    inValue = 0
    for j in range(0, nIn):
        inValue += getUtxo(tx['vin'][j]['txid'], tx['vin'][j]['vout'])
        
    # total output value를 계산한다
    nOut = len(tx['vout'])
    outValue = 0
    for k in range (0, nOut):
        outValue += tx['vout'][k]['value']
    
    # Fee를 계산한다
    fee = (inValue - outValue) * 100000000
    txFee.append(fee)
    byteFee.append(fee / tx['size'])
    
    # 바이트 당 Fee를 누적한다
    if i == 1:
        accByteFee.append(byteFee[-1])
    else:
        accByteFee.append(accByteFee[-1] + byteFee[-1])
    
    # 300개 까지만 확인한다
    cnt += 1
    if cnt > 300:
        break
    
print("\n\nBlock Height =", height)
print("Number of Transactions =", nTx)
fig = plt.figure(figsize=(11, 4))
p1 = fig.add_subplot(1,2,1)
p2 = fig.add_subplot(1,2,2)

#p1.plot(byteFee[0:300], color='red', linewidth=1)
x = list(range(1, cnt+1))
p1.bar(x, byteFee[0:cnt], width=1, color="red", edgecolor='red', linewidth=0.5, alpha=0.5)
p1.set_title("Transaction Fee per bytes")
p1.set_xlabel("Tx number")
p1.set_ylabel("Fee (satoshi)")

p2.plot(accByteFee[0:cnt], color='blue', linewidth=1)
p2.set_title("Accumulated Transaction Fee per bytes")
p2.set_xlabel("Block size")
p2.set_ylabel("Accumulated Fee (satoshi)")
plt.show()
