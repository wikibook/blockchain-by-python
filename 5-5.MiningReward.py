# 파이썬 실습 파일: 5-5.MiningReward.py
import matplotlib.pyplot as plt

block4Year = 210000     # 4년간 생성될 블록 수 (근사치 : 365 * 24 * 6)
Reward = [50]           # 초기 Reward = 50 BTC
Year = [2009]           # Mining 초기 연도
blockHeight = [0]       # 초기 블록 번호
Bitcoin = [50]          # 초기 발행량

# 4년씩 지나가면서 blockHeight, Reward, 비트코인 발행량을 측정함.
while True:
    blockHeight.append(blockHeight[-1] + block4Year)
    Bitcoin.append(Bitcoin[-1] + Reward[-1] * block4Year)
    Reward.append(Reward[-1] / 2)
    Year.append(Year[-1] + 4)
    
    if Reward[-1] < 1e-8:    # 1 Satoshi
        break

print("\n\n* Total Bitcoin = %.2f until %d year" % (Bitcoin[-1], Year[-1]))
print("* Block Height =", blockHeight[-1])

fig = plt.figure(figsize=(10, 7))
p1 = fig.add_subplot(2,2,1)
p2 = fig.add_subplot(2,2,2)
p3 = fig.add_subplot(2,2,3)
p4 = fig.add_subplot(2,2,4)

p1.plot(Year, Reward, color='red', linewidth=1.0)
p1.set_title("Reward")

p2.plot(Year, Bitcoin, color='blue', linewidth=1.0)
p2.set_title("Bitcoin Amount")

p3.plot(Year[0:10], Reward[0:10], color='red', linewidth=1.0)
p3.set_title("Reward")

p4.plot(Year[0:10], Bitcoin[0:10], color='blue', linewidth=1.0)
p4.set_title("Bitcoin Amount")