class Packet:
    SYN_FIN_ACK_RST_dict = {
        '0000': b'\x00', '0010': b'\x20', '0100': b'\x40', '0110': b'\x60',
        '1000': b'\x70', '1010': b'\x90', '1100': b'\xC0', '1110': b'\xE0',
        '0001': b'\x10', '0011': b'\x30', '0101': b'\x50', '0111': b'\x70',
        '1001': b'\x80', '1011': b'\xA0', '1101': b'\xD0', '1111': b'\xF0'
    }

    def __init__(self):
        # merge SYN FIN ACK to a byte
        # SYN FIN ACK RST 0 0 0 0
        # total 8 bits, that is 1 bytes
        self.SYN = 0
        self.FIN = 0
        self.ACK = 0
        self.RST = 0

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
        tmp_str = str(self.SYN) + str(self.FIN) + str(self.ACK)
        return Packet.SYN_FIN_ACK_RST_dict[tmp_str]

    def set_LEN(self) -> None:
        # Set the LEN property.
        self.LEN = len(bytes(self.payload, encoding="utf-8"))

    # ! TODO: Maybe we should write a new checksum rather than the demonstration one in pdf.
    def calculate_CHECKSUM(self) -> int:
        checksum = 0
        for byte in self.payload_to_byte():
            checksum += byte
        checksum = -(checksum % 256)
        return checksum & 0XFF

    def set_CHECKSUM(self) -> None:
        self.CHECKSUM = self.calculate_CHECKSUM()

    @staticmethod
    def handshake(number: int) -> 'Packet':
        """
        :param: number: 0 1 2. It is the sequence of handshake.
        :return: A Packet object that used for handshake.
        """
        packet = Packet()
        packet.set_payload('')
        if number == 0:
            packet.SYN = 1
        elif number == 1:
            packet.SYN = 1
            packet.ACK = 1
        else:
            packet.ACK = 1

        return packet

    def set_payload(self, string) -> None:
        self.payload = string
        self.set_LEN()
        self.set_CHECKSUM()

    @staticmethod
    def test_packet() -> 'Packet':
        """
        :return: A test packet object.
        """
        packet = Packet()
        packet.set_payload('I can eat glass, it doesn\'t hurt me.\n')
        return packet

    @staticmethod
    def RST_packet() -> 'Packet':
        packet = Packet()
        packet.RST = 1
        packet.set_payload('')
        return packet

    @staticmethod
    def parse(raw: bytes) -> 'Packet':
        """
        This function parse the bytes of Packet object.
        :param raw: The bytes.
        :return: A Packet Object.
        """
        new_dict = {v: k for k, v in Packet.SYN_FIN_ACK_RST_dict.items()}
        packet = Packet()
        tmp_str = new_dict[raw[:1]]
        packet.SYN = tmp_str[0]
        packet.FIN = tmp_str[1]
        packet.ACK = tmp_str[2]
        packet.SEQ = int.from_bytes(raw[1:5], byteorder="big", signed=False)
        packet.SEQACK = int.from_bytes(raw[5:9], byteorder="big", signed=False)
        packet.LEN = int.from_bytes(raw[9:13], byteorder="big", signed=False)
        packet.CHECKSUM = int.from_bytes(raw[13:15], byteorder="big", signed=False)
        packet.payload = raw[15:].decode('utf-8')
        return packet

    def to_string(self):
        string = 'SYN: ' + str(self.SYN) + '\n' \
                 + 'FIN: ' + str(self.FIN) + '\n' \
                 + 'ACK: ' + str(self.ACK) + '\n' \
                 + 'RST: ' + str(self.RST) + '\n' \
                 + 'SEQ: ' + str(self.SEQ) + '\n' \
                 + 'SEQACK: ' + str(self.SEQACK) + '\n' \
                 + 'LEN: ' + str(self.LEN) + '\n' \
                 + 'CHECKSUM: ' + str(self.CHECKSUM) + '\n' \
                 + 'payload: ' + str(self.payload) + '\n'

        print(string)

    @staticmethod
    def check_handshake(number: int, raw: bytes) -> bool:
        return raw == Packet.handshake(number).encode()
