from socket import *

if __name__ == '__main__':
    udp_socket = socket(AF_INET, SOCK_DGRAM)

    receive_addr = ('127.0.0.1', 33333)
    # receive_addr = ('', 33333)

    data = "Test msg\n".encode()
    print(data)

    udp_socket.sendto(data, receive_addr)
