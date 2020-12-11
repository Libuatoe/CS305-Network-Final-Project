from rdt import RDTSocket

if __name__ == '__main__':
    server_address = ('127.0.0.1', '33333')
    server = RDTSocket(rate=None)

    server.bind(server_address)

