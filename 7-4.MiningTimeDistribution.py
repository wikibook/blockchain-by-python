# 파이썬 실습 파일: 7-4.MiningTimeDistribution.py
# RPC 패키지 : https://github.com/petertodd/python-bitcoinlib
from bitcoin.rpc import RawProxy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Bitcoin Core에 접속한다.
p = RawProxy()

# 블록체인의 블록 개수을 읽어온다
n = p.getblockcount()

# 최근 1000개 블록의 헤더를 읽어서 생성 시간을 조회한다.
header = []
for i in range(n - 999, n+1):
    bHash = p.getblockhash(i)
    hdr = p.getblockheader(bHash)
    height = hdr['height']
    btime = hdr['time']
    bhash = hdr['hash']
    header.append([height, btime, bhash])
    
df = pd.DataFrame(header, columns=['Height', 'Time', 'Hash'])
sdf = df.sort_values('Time')
sdf = sdf.reset_index()
print(df.to_string())
print('총 %d 개 블록 헤더를 읽어왔습니다.' % len(df))

# 블록 생성 소요 시간 분포 관찰
mtime = sdf['Time'].diff().values
mtime = mtime[np.logical_not(np.isnan(mtime))]
print("평균 Mining 시간 = %d (초)" % np.mean(mtime))
print("표준편차 = %d (초)" % np.std(mtime))

plt.figure(figsize=(8,4))
n, bins, patches = plt.hist(mtime, 30, facecolor='red', edgecolor='black', linewidth=0.5, alpha=0.5)
plt.title("Mining Time Distribution")
plt.show()

# 10분 이내에 내 거래가 Mining될 확률
s = 60 * 10
p = 1 - np.exp(-s / np.mean(mtime))
print("10분 이내에 내 거래가 Mining될 확률 = %.2f (%s)" % (p * 100, '%'))