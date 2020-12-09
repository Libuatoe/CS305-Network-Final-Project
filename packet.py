

class Packet:
    # The constructor of Packet
    def __init__(self):
        # merge SYN FIN ACK to a byte
        # SYN FIN ACK 0 0 0 0 0
        # total 8 bits, that is 1 bytes
        self.SYN = 0
        self.FIN = 0
        self.ACK = 0

        # max SEQ is 2^32 = 4,294,967,295
        # 4 bytes
        self.SEQ = 0

        # max SEQACK is 2^32 = 4,294,967,295
        # 4 bytes
        self.SEQACK = 0

        # 4 bytes
        self.LEN = 0

        # 2 bytes
        self.CHECKSUM = 0
        self.payload = ''

    def encode(self) -> bytes:
        return self.SYN_FIN_ACK_to_byte() + self.SEQ.to_bytes(length=4, byteorder="big") + \
               self.SEQACK.to_bytes(length=4, byteorder="big") + \
               self.LEN.to_bytes(length=4, byteorder="big") + \
               self.CHECKSUM.to_bytes(length=2, byteorder="big") + self.payload_to_byte()

    def payload_to_byte(self) -> bytes:
        return str.encode(self.payload)

    def SYN_FIN_ACK_to_byte(self) -> bytes:
        """
        Convert SYN, FIN, ACK 3 bits to 1 bytes
        :return: A bytes.
        """

        tmp_dict = {'000': b'\x00', '001': b'\x20', '010': b'\x40', '011': b'\x60',
                    '100': b'\x70', '101': b'\x90', '110': b'\xC0', '111': b'\xE0'}
        tmp_str = str(self.SYN) + str(self.FIN) + str(self.ACK)

        print(type(tmp_dict[tmp_str]))
        return tmp_dict[tmp_str]

    # ! TODO: write a decode function here. Receive a packet and decode it in Packet object.

    def set_LEN(self) -> None:
        # Set the LEN property.
        self.LEN = len(bytes(self.payload))

    # ! TODO: Maybe we should write a new checksum rather than the demonstration one in pdf.
    def calculate_CHECKSUM(self) -> int:
        checksum = 0
        for byte in self.payload_to_byte():
            checksum += byte
        checksum = -(checksum % 256)
        return checksum & 0XFF

    def set_CHECKSUM(self) -> None:
        self.CHECKSUM = self.calculate_CHECKSUM()


def handshake_0() -> Packet:
    """
    :return: A Packet object that used for first handshake.
    """
    packet = Packet()
    packet.SYN = 1
    packet.SEQ = 0
    packet.payload = ''
    packet.set_LEN()
    packet.set_CHECKSUM()
    return packet
