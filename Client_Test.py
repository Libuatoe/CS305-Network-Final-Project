from rdt import RDTSocket

if __name__ == '__main__':
    server_address = ('127.0.0.1', 33333)
    client = RDTSocket(rate=None)
    client.connect(server_address)

