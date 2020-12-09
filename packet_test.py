from packet import Packet

if __name__ == '__main__':
    packet1 = Packet()
    packet2 = Packet()
    packet2.FIN = 1
    packet2.SYN = 1

    print(packet2.encode())


