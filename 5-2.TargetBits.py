# 파이썬 실습 파일: 5-2.TargetBits.py
# 타겟 값을 일반형으로 변환하고 난이도를 측정한다.
def targetValue(bits):
    # bit의 왼쪽 1바이트 (exponents)를 추출한다.
    exponents = bits >> 24
    
    # bits의 오른쪽 3바이트 (coefficient)를 추출한다.
    coefficient = bits & 0x007fffff
    
    # target value를 계산한다
    target = coefficient << 8 * (exponents - 3)
    
    # difficulty를 계산한다
    genesisTargetValue = 0x00000000FFFF0000000000000000000000000000000000000000000000000000
    difficulty = genesisTargetValue / target
    
    return target, difficulty

# 블록 #559834의 target bits의 target value와 difficulty를 계산한다
targetBits = 0x172fd633
target, difficulty = targetValue(targetBits)

print("\n\n Target Bits =", hex(targetBits))
print("Target Value =", hex(target))
print("  Difficulty =", difficulty)

# 블록 #559834의 block hash는 아래와 같고, 이 값은 위의 target 보다 작다. (valid)
blockHash = 0x0000000000000000001aa4184c12376e3da18b742c1739a205fe2ea2405cd8e7
print("\nBlock Hash = ",  hex(blockHash))

if blockHash <= target:
    print("Block hash is less than target value. --> valid.")
else:
    print("Block hash is invalid.")
    