import socket
import sock

host = "0.0.0.0"
port = 8888

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server.bind((host, port))
print(f'server listen on {host}:{port}.....')
server.listen()

client, addr = server.accept()
sock_ = sock.sock_server(client)
client.close()
server.close()


