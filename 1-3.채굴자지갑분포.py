# 파이썬 실습 파일: 1-3.채굴자지갑분포.py
import requests
import time
import pandas as pd
import matplotlib.pyplot as plt

# 마지막 block 번호를 조회한다
resp = requests.get(url='https://blockchain.info/latestblock')
data = resp.json()
nHeight = data['height']

# 마지막부터 몇 개 블록을 읽어서 coinbase transaction의 지갑 주소를 수집한다
mining = []

for n in range(nHeight, nHeight-100, -1):
    url = 'https://blockchain.info/block-height/' + str(n) + '?format=json'
    resp = requests.get(url=url)
    data = resp.json()
    block = data['blocks'][0]
    
    stime = block['time']
    addr = block['tx'][0]['out'][0]['addr']
    value = block['tx'][0]['out'][0]['value']
    
    ts = time.gmtime(stime)
    date = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    
    # 결과를 list에 저장한다
    mining.append([date, addr, value])
    
    # 중간 결과를 표시한다
    print("#%d : %s\t%s\t%f" % (n, date, addr, value*1e-8))

# 결과를 dataframe에 저장한다
df = pd.DataFrame(mining, columns=['Date', 'Address', 'Reward'])

# 같은 지갑끼리 묶어본다
grp = df.groupby('Address').Address.count()
print() 
print(grp)

# Histogram
plt.figure(figsize=(6,3))
plt.title("Miner's Address")
x = list(range(1, len(grp.values)+1))
plt.bar(x, grp.values, width=1, color="red", edgecolor='black', linewidth=0.5, alpha=0.5)
plt.show()
