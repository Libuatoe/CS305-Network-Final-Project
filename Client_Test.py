from rdt import RDTSocket

if __name__ == '__main__':
    client_address = ('127.0.0.1', 44444)
    client = RDTSocket(rate=None)
    client.bind(client_address)

