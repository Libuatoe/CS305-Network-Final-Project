class Packet:
    SYN_FIN_ACK_dict = {'000': b'\x00', '001': b'\x20', '010': b'\x40', '011': b'\x60',
                        '100': b'\x70', '101': b'\x90', '110': b'\xC0', '111': b'\xE0'}

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
        tmp_str = str(self.SYN) + str(self.FIN) + str(self.ACK)
        return Packet.SYN_FIN_ACK_dict[tmp_str]

    # ! TODO: write a decode function here. Receive a packet and decode it in Packet object.

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
    def parse(raw: bytes) -> 'Packet':
        """
        This function parse the bytes of Packet object.
        :param raw: The bytes.
        :return: A Packet Object.
        """
        new_dict = {v: k for k, v in Packet.SYN_FIN_ACK_dict.items()}
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
        str0 = 'SYN: ' + str(self.SYN) + '\n'
        str1 = 'FIN: ' + str(self.FIN) + '\n'
        str2 = 'ACK: ' + str(self.ACK) + '\n'
        str3 = 'SEQ: ' + str(self.SEQ) + '\n'
        str4 = 'SEQACK: ' + str(self.SEQACK) + '\n'
        str5 = 'LEN: ' + str(self.LEN) + '\n'
        str6 = 'CHECKSUM: ' + str(self.CHECKSUM) + '\n'
        str7 = 'payload: ' + str(self.payload) + '\n'

        print(str0 + str1 + str2 + str3 + str4 + str5 + str6 + str7)

    @staticmethod
    def check_handshake(number: int, raw: bytes) -> bool:
        return raw == Packet.handshake(number).encode()
