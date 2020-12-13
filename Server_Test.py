import logging

from rdt import RDTSocket

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    server_address = ('127.0.0.1', 33333)
    server = RDTSocket(rate=None)
    server.bind(server_address)
    while True:
        conn, client = server.accept()
