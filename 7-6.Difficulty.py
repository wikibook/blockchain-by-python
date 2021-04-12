# 파이썬 실습 파일: 7-6.Difficulty.py
# RPC 패키지 : https://github.com/petertodd/python-bitcoinlib
from bitcoin.rpc import RawProxy
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Bitcoin Core에 접속한다.
p = RawProxy()

# 블록체인의 블록 개수를 읽어온다
n = p.getblockcount()

# 과거 2016번째 블록 헤더를 100개 읽어서 difficulty를 측정한다
difficulty = []
i = 0
while True:
    bHash = p.getblockhash(n)
    hdr = p.getblockheader(bHash)
    
    dt = datetime.utcfromtimestamp(hdr['time'])
    st = dt.strftime('%Y-%m-%d')
    
    difficulty.append([st, hdr['difficulty']])
    
    # 약 2주 전 블록을 읽어온다. Difficulty는 2016 블록 단위로 바뀌기 때문.
    n -= 2016
    i += 1
    if i < 0 or i > 100:
        break
    print("%d) %d 블록을 읽었습니다" % (i, n))
    
print('총 %d 개 블록 헤더를 읽어왔습니다.' % len(difficulty))

# 차트로 확인해 본다
df = pd.DataFrame(difficulty, columns=['Time', 'Difficulty'])
df = df.reindex(index=df.index[::-1])
df = df.reset_index()
del df['index']
print("\n마지막 10개의 Difficulty:")
print(df.tail(10))

plt.figure(figsize=(8,4))
x = [datetime.strptime(d,'%Y-%m-%d').date() for d in df['Time']]
y = range(len(x))
plt.plot(x, df['Difficulty'], color='red', linewidth=1)

plt.title("Difficulty")
plt.grid(alpha=0.2)
plt.show()