from sock import *

class MySockServer(sock_server):
    def run(self, client: socket.socket):
        self.send(client, {"name": "abu"})
        client.close()

if __name__ == '__main__':
    server_address = ('localhost', 8888)
    server = MySockServer(server_address)




