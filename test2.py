import rsa

# 生成密钥对
(public_key, private_key) = rsa.newkeys(512)
print(rsa.newkeys(512))

# # 要加密的数据
# data = b"Hello, this is a secret message!"

# # 使用公钥加密数据
# ciphertext = rsa.encrypt(data, public_key)

# print("加密后的数据:", ciphertext)

# # 使用私钥解密数据
# plaintext = rsa.decrypt(ciphertext, private_key)

# print("解密后的数据:", plaintext)