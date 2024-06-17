import socket
import pickle
import hashlib
import rsa
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import struct
import threading
from abc import ABC, abstractmethod

def generate_rsa_key():
    return rsa.newkeys(1024)

def generate_aes_key():
    key = get_random_bytes(16)
    iv = get_random_bytes(16)
    return key,iv

'''
aes encrypt
'''
def aes_encrypt(key, data: bytes):
    cipher = AES.new(key[0], AES.MODE_CBC, key[1])
    return cipher.encrypt(data)

'''
aes decrypt
'''
def aes_decrypt(key, data):
    decipher = AES.new(key[0], AES.MODE_CBC, key[1])
    return decipher.decrypt(data)

'''
rsa encrypt
'''
def rsa_encrypt(public_key, data):
    return rsa.encrypt(data, public_key)

'''
rsa decrypt
'''
def rsa_decrypt(private_key, data):
    return rsa.decrypt(data, private_key)

'''
pack int number to 4 bytes length bytesarray data
'''
def pack_number(num) -> bytes:
    return struct.pack('i', num)

'''
unpack 4 bytes length bytesarray data to int number
'''
def unpack_number(data: bytes):
    return struct.unpack('i', data)[0]

class SockServerInterface(ABC):
    @abstractmethod
    def run(self, client: socket.socket):
        pass

class sock_server(SockServerInterface):
    '''
    generate rsa and aes key in server
    '''
    def __init__(self, addr) -> None:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(addr)
        server.listen()
        self.server = server
        print(f'server listen on {addr[0]}:{addr[1]}...')

        while True:
            client, addr = server.accept()
            self.client = client
            self.rsa_key = generate_rsa_key()
            self.send_rsa_key()
            self.recv_aes_key()
            th = threading.Thread(target=self.run, args=(client,))
            th.start()


    '''
    This method should be overridden by the user
    '''
    def run(self, client: socket.socket):
        pass

    '''
    send public key to client
    '''
    def send_rsa_key(self):
        rsa_public_key_byte = pickle.dumps(self.rsa_key[0])
        rsa_public_key_length = len(rsa_public_key_byte)
        self.client.send(pack_number(rsa_public_key_length))
        self.client.send(rsa_public_key_byte)

    '''
    recv aes key from client
    '''
    def recv_aes_key(self):
        head_len = unpack_number(self.client.recv(4, socket.MSG_WAITALL))

        encrypted_aes_key = self.client.recv(head_len, socket.MSG_WAITALL)

        decrypted_aes_key = rsa.decrypt(pickle.loads(encrypted_aes_key), self.rsa_key[1])

        self.aes_key = pickle.loads(decrypted_aes_key)
    
    def send(self,client: socket.socket, data: dict):
        data_bytes = pickle.dumps(data)
        en_data = aes_encrypt(self.aes_key, data_bytes)
        self.

class sock_client(object):
    def __init__(self, addr) -> None:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(addr)
        self.client = client
        self.rsa_public_key = self.recv_public_key()
        self.aes_key = generate_aes_key()
        self.send_aes_key()
    '''
    recv rsa public key from server
    '''
    def recv_public_key(self):
        rsa_public_key_length = unpack_number(self.client.recv(4, socket.MSG_WAITALL))
        return pickle.loads(self.client.recv(rsa_public_key_length, socket.MSG_WAITALL))

    '''
    send aes key to server
    '''
    def send_aes_key(self):
        encrypted_aes_key = rsa_encrypt(self.rsa_public_key, pickle.dumps(self.aes_key))
        self.client.send(pack_number(len(encrypted_aes_key)))
        self.client.send(encrypted_aes_key)