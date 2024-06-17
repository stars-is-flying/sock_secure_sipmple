from sock import *


class MySockClient(sock_client):
    def run(self):
        print(self.recv())
        self.client.close()

if __name__ == '__main__':
    server_address = ('localhost', 8888)
    client = MySockClient(server_address)
    client.run()