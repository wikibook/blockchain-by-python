# 파이썬 실습 파일: 5-6.FeePerBytes.py
import requests
import matplotlib.pyplot as plt

# 마지막 블록의 해시 값을 읽어온다
url = 'https://blockchain.info/latestblock?format=json'
resp = requests.get(url=url)
data = resp.json()

# 마지막 블록을 읽어온다
url = 'https://blockchain.info/block/' + data['hash'] + '?format=json'
resp = requests.get(url=url)
data = resp.json()

# Transaction (Tx) 부분을 분석한다
tx = data['tx']
nTx = len(tx)

# Tx를 순차적으로 읽어가면서 fee / bytes를 계산한다
txFee = []
byteFee = []
accByteFee = []
for i in range(1, nTx):
    txIn = tx[i]['inputs']
    txOut = tx[i]['out']
    
    inValue = 0
    outValue = 0
    
    # Input value를 계산한다
    for k in range(len(txIn)):
        inValue += txIn[k]['prev_out']['value']
        
    # Output value를 계산한다
    for k in range(len(txOut)):
        outValue += txOut[k]['value']
    
    # Fee를 계산한다
    fee = inValue - outValue
    txFee.append(fee)
    byteFee.append(fee / tx[i]['size'])
    
    # 바이트 당 Fee를 누적한다
    if i == 1:
        accByteFee.append(byteFee[-1])
    else:
        accByteFee.append(accByteFee[-1] + byteFee[-1])

print("\n\nBlock Height =", data['height'])
print("Number of Transactions =", nTx)
print("Total Fee = %f BTC" % (data['fee'] * 1e-8 ))
fig = plt.figure(figsize=(9, 4))
p1 = fig.add_subplot(1,2,1)
p2 = fig.add_subplot(1,2,2)
p1.plot(byteFee[0:300], color='red', linewidth=1)
p1.set_title("Transaction Fee per bytes")
p1.set_xlabel("Tx number")
p1.set_ylabel("Fee (satoshi)")
p2.plot(accByteFee[0:300], color='blue', linewidth=1)
p2.set_title("Accumulated Transaction Fee per bytes")
p2.set_xlabel("Block size")
p2.set_ylabel("Accumulated Fee (satoshi)")
plt.show()