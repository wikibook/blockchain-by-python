# 파이썬 실습 파일: 6-1.VersionMsg.py
import socket
import hashlib
import struct
import time
import random

magic = 0xd9b4bef9
protocolVersion = 70015
swVersion = b'/Satoshi:0.16.0/'     # 문자열 길이는 16으로 고정함
NODE_NETWORK = 1 # Node Service (bitcoin/src/protocol.h 참조)
services = NODE_NETWORK
tcpPort = 8333

# 메시지를 조립한다
def assembleMessage(command, payload):
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[0:4]
    header = struct.pack('L12sL4s', magic, command, len(payload), checksum)
    return  header + payload

# version 메시지에 IP 주소를 기록한다
def verAddr(ipaddr, port):
    nodeService = struct.pack('<Q', services)
    if len(ipaddr) < 1:
        filler = b'\x00' * 12
    else:
        filler = struct.pack('<12s', b'\x00' * 10 + b'\xff' * 2)
    nodeAddress = struct.pack('>4s', ipaddr)
    nodePort = struct.pack('>H', port)
    return (nodeService + filler + nodeAddress + nodePort)

# Version 메시지 생성
# 참조 : Wireshark analyzer & https://en.bitcoin.it/wiki/Protocol_documentation#version
def msgVersion(ip):
    timestamp = int(time.time())
    addrYou = verAddr(socket.inet_aton(ip), tcpPort)
    addrMe = verAddr(b'', 0)
    nonce = random.getrandbits(64)
    userAgent = swVersion
    blockHeight = 0

    msg = struct.pack('<LQQ26s26sQB16sLB', 
                      protocolVersion, 
                      services, 
                      timestamp, 
                      addrYou, 
                      addrMe, 
                      nonce, 
                      16, 
                      userAgent, 
                      blockHeight,
                      1)
    return assembleMessage(b'version', msg)

# Version Ack 메시지 생성
def msgVerAck():
    return assembleMessage(b'verack', b'') # payload 없음

# destIP 노드로 version 메시지를 보내고, verack 메시지를 수신한다.
def sendVersion(destIP):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect((destIP, tcpPort))
    except Exception:
        print("\n%s 에 접속할 수 없습니다." % destIP)
        return -1
    
    # Version 메시지를 송출한다
    msg = msgVersion(destIP)
    sock.send(msg)
    
    now = time.gmtime(time.time())
    print("\n[%02d:%02d:%02d] Send Version to %s" % (now.tm_hour, now.tm_min, now.tm_sec, destIP))
    
    # 상대방이 보낸 Version, VerAck를 받는다
    a = sock.recv(1024) # receive version
    b = sock.recv(1024)
    v = a + b
    
    # VerAck 메시지를 보낸다
    msg = msgVerAck()
    sock.send(msg)
    sock.close()
    
    # Receive packet을 decode 해야 하지만, 관심있는 필드만 뽑아내기로 한다
    version = v[4:11].decode("utf-8")
    
    # user agent string의 length (1 byte)
    length = int.from_bytes(v[104:105], byteorder='big')
    userAgent = v[105:(105 + length)].decode("utf-8")
    block = struct.unpack("<L", v[121:125])[0]
    verack = v[130:136].decode("utf-8")
    
    print("[%02d:%02d:%02d] Receive %s : %s, Block height = %d" % (now.tm_hour, now.tm_min, now.tm_sec, version, userAgent, block))
    print("[%02d:%02d:%02d] Receive %s" % (now.tm_hour, now.tm_min, now.tm_sec, verack))
    return 0
