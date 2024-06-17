import socket
import sock

addr = ('127.0.0.1', 8888)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(addr)

sock_ = sock.sock_client(client)
print(sock_.rsa_public_key)
