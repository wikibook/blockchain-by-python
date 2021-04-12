# 파이썬 실습 파일: 6-2.BloomFilter.py
from bitarray import bitarray
import math
import random
import mmh3     # pip install mmh3 : Murmur3 hash function

# Bloom filter의 최적 파라메터를 결정한다
# n = number of elements
# prob = Desired False positive probability
def optParameter(n, prob):
    m = -n * math.log(prob) / (math.log(2) ** 2)
    k = math.ceil(m * math.log(2) / n)
    return k, math.ceil(m)

# element를 Bloom filter에 등록한다
def add(BloomFilter, element, k, m):
    for i in range(k):
        index = mmh3.hash(element, i) % m
        BloomFilter[index] = 1

# element가 Bloom filter에 있는지 확인한다
def contain(BloomFilter, element, k, m):
    for i in range(k):
        index = mmh3.hash(element, i) % m
        if BloomFilter[index] == 0:
            # 한 비트라도 0 (False)이면 "없음"
            return 0
        
    # 모두 1 이면 "있을 가능성이 있음"
    return 1

# 임의의 10,000개 숫자를 블룸필터에 등록한 후 특정 숫자가 블룸필터에 등록돼 있는지
# 찾아본다. 그리고 실제는 등록되지 않았는데 등록됐다고 잘못 판단한 경우가 얼마나
# 되는지 측정해 본다. 총 100,000 번 수행해서 평균적으로 잘못 판단할 확률을 측정해 본다.
def bloomFilter(prob=0.1, nTry = 100000):
    # 1 ~ 10,000 사이의 난수 100개를 만들어 집합 A를 구성한다
    setA = random.sample(range(1, 10000), 100)
    
    # Bloom filter를 초기화한다. FP rate가 원하는 수준이 나오도록 k, m을 설정한다.
    k, m = optParameter(len(setA), prob=prob)
    BloomFilter = bitarray(m)
    BloomFilter[:] = 0     # 모두 0으로 초기화한다
    
    # 집합 A로 Bloom Filter를 만든다
    for element in setA:
        add(BloomFilter, str(element), k, m)
    
    predCnt = 0
    actCnt = 0
    for i in range(nTry):
        # 1 ~ 10,000 사이의 난수 1개를 만든다
        r = random.randrange(1,10000)
        
        # r이 집합 A에 있는지 확인한다
        result = contain(BloomFilter, str(r), k, m)
        if result == 1:
            # 있을 가능성이 있다는 카운터
            predCnt += 1
            
            # 실제 확인한 카운터
            for e in setA:
                if r == e:
                    actCnt += 1
                    break
                
        # result == 0 이면 확실히 없는 것임.
    
    # Desired FP rate와 Actual FP rate이 잘 일치하는지 확인한다.
    print("\nDesired FP rate = ", prob)
    print("Number of element (n) = ", len(setA))
    print("Number of hash functions (k) = ", k)
    print("Number of Bloom filter bit (m) = ", m)
    print("Actual FP rate (p) = ", (predCnt - actCnt) / nTry)

