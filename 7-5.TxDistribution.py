# 파이썬 실습 파일: 7-5.TxDistribution.py
# RPC 패키지 : https://github.com/petertodd/python-bitcoinlib
from bitcoin.rpc import RawProxy
import matplotlib.pyplot as plt
import numpy as np

# Bitcoin Core에 접속한다.
p = RawProxy()

# 블록체인의 블록 개수를 읽어온다
n = p.getblockcount()

# 최근 200개 블록을 읽어서 Transaction 개수를 확인한다
nTx = []
for i in range(n - 199, n+1):
    bHash = p.getblockhash(i)
    block = p.getblock(bHash)
    nTx.append(len(block['tx']))

print(nTx)
print("\nTransaction 평균 = %.2f" % np.mean(nTx))

# Histogram을 그려 본다
plt.figure(figsize=(8,5))
n, bins, patches = plt.hist(nTx, 30, facecolor='blue', edgecolor='black', linewidth=0.5, alpha=0.5)
plt.title("Number of Transactions")
plt.show()
