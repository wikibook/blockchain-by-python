# 파이썬 실습 파일: 7-7.MemPool.py
# RPC 패키지 : https://github.com/petertodd/python-bitcoinlib
from bitcoin.rpc import RawProxy
import pprint
pp = pprint.PrettyPrinter(indent=1)

# Bitcoin Core에 접속한다.
p = RawProxy()

# MemPool에 있는 Tx 개수를 확인한다
mem = p.getmempoolinfo()
print("\n\nNumber of Tx :", mem['size'])

# MemPool에 있는Txid를 조회한다.
memTxid = p.getrawmempool()

# MemPool에 있는 Tx 데이터 10개 만 상세 데이터를 조회한다.
i = 0
for tx in memTxid:
    # MemPool에 있는 Txid의 상세 데이터를 읽어온다.
    memTx = p.getmempoolentry(tx)
    rawTx = p.getrawtransaction(tx)
    print("\nTXID :", tx)
    pp.pprint(memTx)
    print("\nRaw TX :")
    print(rawTx)
    i += 1
    if i > 10:
        break

# rawTx 데이터를 decode 한다
dTx = p.decoderawtransaction(rawTx)
print("\n\n")
pp.pprint(dTx)