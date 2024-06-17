from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# 密钥和初始化向量（IV）
key = get_random_bytes(16)  # 16字节（128位）的密钥
iv = get_random_bytes(16)   # 16字节的初始化向量

# 要加密的数据
data = b"Hello, this is a secret message!"

# 创建AES加密器
cipher = AES.new(key, AES.MODE_CBC, iv)

# 加密数据
ciphertext = cipher.encrypt(pad(data, AES.block_size))

print("加密后的数据:", ciphertext)

# 创建AES解密器
decipher = AES.new(key, AES.MODE_CBC, iv)

# 解密数据
plaintext = unpad(decipher.decrypt(ciphertext), AES.block_size)

print("解密后的数据:", plaintext)