# 파이썬 실습 파일: 7-2.GetBlockChainInfo.py
# RPC 패키지 : https://github.com/petertodd/python-bitcoinlib
from bitcoin.rpc import RawProxy
import pprint
pp = pprint.PrettyPrinter(indent=1)

# Bitcoin Core에 접속한다.
p = RawProxy()

# Blockchain 정보를 읽어온다
info = p.getblockchaininfo()

# 결과를 출력한다
print("\nBlockchain Info :")
pp.pprint(info)
