import USocket

if __name__ == '__main__':
    send_socket = USocket.UnreliableSocket(None)
    receive_addr = ('127.0.0.1', 33333)
    # print(packet.handshake_0().encode())
    print(receive_addr)
    # content = packet.handshake_0().encode()
    content = 'hello'.encode()
    print(content)
    send_socket.sendto(content, receive_addr)
