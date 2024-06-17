import socket
import pickle
import hashlib
import rsa
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import struct

def generate_rsa_key():
    return rsa.newkeys(1024)

def generate_aes_key():
    key = get_random_bytes(16)
    iv = get_random_bytes(16)
    return key,iv

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


class sock_server(object):
    '''
    generate rsa and aes key in server
    '''
    def __init__(self, client: socket.socket) -> None:
        self.client = client
        self.rsa_key = generate_rsa_key()
        self.aes_key = generate_aes_key()

        self.send_rsa_key()
    '''
    send public key to client
    '''
    def send_rsa_key(self):
        rsa_public_key_byte = pickle.dumps(self.rsa_key[0])
        rsa_public_key_length = len(rsa_public_key_byte)
        self.client.sendall(pack_number(rsa_public_key_length))
        self.client.send(rsa_public_key_byte)
    
class sock_client(object):
    def __init__(self, client: socket.socket) -> None:
        self.client = client
        self.rsa_public_key = self.recv_public_key()
    
    '''
    recv rsa public key from server
    '''
    def recv_public_key(self):
        rsa_public_key_length = unpack_number(self.client.recv(4, socket.MSG_WAITALL))
        return pickle.loads(self.client.recv(rsa_public_key_length, socket.MSG_WAITALL))
    