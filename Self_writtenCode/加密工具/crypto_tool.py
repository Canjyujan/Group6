import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import argparse
import sys

# AES 密钥长度 16/24/32 字节
AES_KEY = b'ThisIsASecretKey'

def base64_encode(data):
    """Base64编码"""
    encoded = base64.b64encode(data.encode('utf-8'))
    return encoded.decode('utf-8')

def base64_decode(data):
    """Base64解码"""
    try:
        decoded = base64.b64decode(data.encode('utf-8'))
        return decoded.decode('utf-8')
    except Exception as e:
        return f'解码失败: {e}'

def md5_hash(data):
    """MD5哈希"""
    md5 = hashlib.md5()
    md5.update(data.encode('utf-8'))
    return md5.hexdigest()

def aes_encrypt(data):
    """AES加密（ECB模式）"""
    try:
        cipher = AES.new(AES_KEY, AES.MODE_ECB)
        ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
        return base64.b64encode(ct_bytes).decode('utf-8')
    except Exception as e:
        return f'加密失败: {e}'

def aes_decrypt(data):
    """AES解密（ECB模式）"""
    try:
        cipher = AES.new(AES_KEY, AES.MODE_ECB)
        ct_bytes = base64.b64decode(data)
        pt = unpad(cipher.decrypt(ct_bytes), AES.block_size)
        return pt.decode('utf-8')
    except Exception as e:
        return f'解密失败: {e}'

def menu():
    """功能菜单"""
    print("\n请选择简易加密解密工具")
    print("1. Base64 编码")
    print("2. Base64 解码")
    print("3. MD5 哈希")
    print("4. AES 加密")
    print("5. AES 解密")
    print("0. 退出")

def main():
    """程序主入口"""
    while True:
        menu()
        choice = input("请选择功能 (0-5)：")
        if choice == '0':
            print("程序已退出。")
            sys.exit()
        elif choice in ['1', '2', '3', '4', '5']:
            text = input("请输入内容：")
            if choice == '1':
                print("Base64 编码结果：", base64_encode(text))
            elif choice == '2':
                print("Base64 解码结果：", base64_decode(text))
            elif choice == '3':
                print("MD5 哈希结果：", md5_hash(text))
            elif choice == '4':
                print("AES 加密结果：", aes_encrypt(text))
            elif choice == '5':
                print("AES 解密结果：", aes_decrypt(text))
        else:
            print("输入有误，请重新选择！")

def parse_args():
    """命令行参数支持"""
    parser = argparse.ArgumentParser(description='简易加密解密工具')
    parser.add_argument('-m', '--mode', type=str, help='模式: base64-encode, base64-decode, md5, aes-encrypt, aes-decrypt')
    parser.add_argument('-t', '--text', type=str, help='要处理的文本')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    if args.mode and args.text:
        mode = args.mode.lower()
        text = args.text
        if mode == 'base64-encode':
            print(base64_encode(text))
        elif mode == 'base64-decode':
            print(base64_decode(text))
        elif mode == 'md5':
            print(md5_hash(text))
        elif mode == 'aes-encrypt':
            print(aes_encrypt(text))
        elif mode == 'aes-decrypt':
            print(aes_decrypt(text))
        else:
            print("不支持的模式")
    else:
        # 进入交互菜单模式
        main()
