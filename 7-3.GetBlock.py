# 파이썬 실습 파일: 7-3.GetBlock.py
# RPC 패키지 : https://github.com/petertodd/python-bitcoinlib
from bitcoin.rpc import RawProxy
import pprint
pp = pprint.PrettyPrinter(indent=1)

# Bitcoin Core에 접속한다.
p = RawProxy()

# 블록체인 tip (끝 부분)의 hash, height를 읽어온다
tip = p.getchaintips()

# 블록 height 및 hash 값을 가져온다
height = tip[0]['height']
bHash = tip[0]['hash']

# 블록 데이터를 읽어온다
block = p.getblock(bHash)
pp.pprint(block)
