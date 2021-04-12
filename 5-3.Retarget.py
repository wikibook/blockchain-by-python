# 파이썬 실습 파일: 5-3.ReTarget.py
from datetime import datetime

# 압축형 타겟을 일반형으로 변환한다.
def Uncompact(bits):
    # bit의 왼쪽 1바이트 (exponents)를 추출한다.
    exponents = bits >> 24
    
    # bits의 오른쪽 3바이트 (coefficient)를 추출한다.
    coefficient = bits & 0x007fffff
    
    # target value를 계산한다
    target = coefficient << 8 * (exponents - 3)
    return target

# 일반형 타겟을 압축형으로 변환한다.
def Compact(target):
    # target의 길이
    nLen = target.bit_length()

    # Compact Format으로 변환한다
    nLen = ((nLen + 7) & ~0x7)
    exponents = (int(nLen/8) & 0xff)
    coefficient = (target >> (nLen - 24)) & 0xffffff

    if coefficient & 0x800000:
        coefficient >>= 8
        exponents += 1

    return (exponents << 24) | coefficient

nPowTargetTimespan = 14 * 24 * 60 * 60   # 2 weeks (초)
powLimit = '00000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffff'

# 블록 520128의 target value를 결정한다. (Retarget)
# 이전 블록 (520127)과 2016 이전 블록을 참조하여 계산한다
if 520128 % 2016 == 0:
    # 블록 520127의 target value와 timeStamp를 읽는다
    oldTarget = 0x1749500d
    oldTarget = Uncompact(oldTarget)
    currTimeStamp = 0x5ae305b6
    
    # 2016 이전 블록 (520127 - 2016 + 1 = 518112)의 timeStamp를 읽는다
    prevTimeStamp = 0x5ad16764
    
    # 2016블록이 생성된 시간을 측정한다 (초 단위)
    nActualTimespan = currTimeStamp - prevTimeStamp
    
    # 크게 변동하는 것을 방지하기 위해, 
    # 0.5 weeks 보다 작으면 0.5 weeks로, 8 weeks 보다 크면 8 weeks로 조정한다.
    if nActualTimespan < nPowTargetTimespan / 4:
        nActualTimespan = nPowTargetTimespan / 4
    if nActualTimespan > nPowTargetTimespan * 4:
        nActualTimespan = nPowTargetTimespan * 4
        
    # Retarget Value를 계산한다
    newTarget = oldTarget * (nActualTimespan / nPowTargetTimespan)
    
    # 난이도 상한선 조정
    if newTarget > int(powLimit, 16):
        newTarget = int(powLimit, 16)
        
    newTarget = round(newTarget)
    newTarget = Compact(newTarget)
    
    # 결과 출력
    print("\n블록 518112 생성 시각 =", datetime.utcfromtimestamp(prevTimeStamp).strftime('%Y-%m-%d %H:%M:%S'))
    print("블록 520127 생성 시각 =", datetime.utcfromtimestamp(currTimeStamp).strftime('%Y-%m-%d %H:%M:%S'))
    print("2016 블록 생성에 걸린 시간 = %.2f (분)" % (nActualTimespan / 60))
    print("1 블록 생성에 걸린 평균 시간 = %.2f (분)" % (nActualTimespan / 60 / 2016))
    print("현재 Target bits =", hex(Compact(oldTarget)))
    print("블록 520128에 적용할 새로운 Target bits =", hex(newTarget))
else:
    # 아직 target을 바꿀 때가 아님. 520127의 target을 유지한다.
    newTarget = 0x1749500d



