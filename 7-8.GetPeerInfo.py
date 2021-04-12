# 파이썬 실습 파일: 7-8.GetPeerInfo.py
# RPC 패키지 : https://github.com/petertodd/python-bitcoinlib
from bitcoin.rpc import RawProxy
import pprint
pp = pprint.PrettyPrinter(indent=1)

# Bitcoin Core에 접속한다.
p = RawProxy()

# 통신 중인 Peer 노드들의 정보를 확인한다.
peer = p.getpeerinfo()
print("\n\nNumber of Nodes :", len(peer))
print("\n")
pp.pprint(peer)