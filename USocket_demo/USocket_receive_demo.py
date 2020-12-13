import USocket

'''
The demo run correctly.
How to use the demo?
    1. Run  USocket_receive_demo.py
    2. Run  network.py
    3. Run  USocket_send_demo.py
'''
if __name__ == '__main__':
    receive_socket = USocket.UnreliableSocket(None)
    receive_addr = ('127.0.0.1', 33333)
    receive_socket.bind(receive_addr)
    while True:
        tmp = receive_socket.recvfrom(2048)
        print(tmp)
