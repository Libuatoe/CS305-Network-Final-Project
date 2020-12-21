import logging
import threading

from USocket import UnreliableSocket
from packet import *

#########################################################
#           日志模块，不需要动。 -- Cheng                    #
#########################################################
logging.basicConfig(
    level=logging.DEBUG,  # 定义输出到文件的log级别，
    format='%(asctime)s in %(filename)s: %(message)s',  # 定义输出log的格式
    datefmt='%Y-%m-%d %A %H:%M:%S')  # 时间


class RDTSocket(UnreliableSocket):
    """
    The functions with which you are to build your RDT.
    -   recvfrom(bufsize)->bytes, addr
    -   sendto(bytes, address)
    -   bind(address)

    You can set the mode of the socket.
    -   settimeout(timeout)
    -   setblocking(flag)
    By default, a socket is created in the blocking mode. 
    https://docs.python.org/3/library/socket.html#socket-timeouts

    """

    def __init__(self, rate=None, debug=True):
        super().__init__(rate=rate)
        self._rate = rate
        self._send_to = None
        self._recv_from = None
        self.debug = debug
        # TODO: ADD YOUR NECESSARY ATTRIBUTES HERE

        self.remote_address = None
        self.last_time = None
        self.timeout = 2
        self.state = 'CLOSED'

    def bind(self, address: (str, int)):
        super().bind(address=address)

    def accept(self) -> ('RDTSocket', (str, int)):

        """
        Accept a connection. The socket must be bound to an address and listening for 
        connections. The return value is a pair (conn, address) where conn is a new 
        socket object usable to send and receive data on the connection, and address 
        is the address bound to the socket on the other end of the connection.

        This function should be blocking.
        """

        temp_state = 'LISTEN'
        addr = None

        while True:
            if temp_state == 'LISTEN':
                handshake_0 = super().recvfrom(2048)
                addr = handshake_0[1]
                if Packet.check_handshake(0, handshake_0[0]):
                    self.sendto(Packet.handshake(1).encode(), addr)
                    logging.debug("Server receives handshake 0")
                    logging.debug("Server sends handshake 1")
                    temp_state = 'SYN-SENT'
                else:
                    temp_state = 'CLOSED'
            if temp_state == 'SYN-SENT':
                expire_thread = TimerThread(func=self.recvfrom_USocket, args=(2048,))
                expire_thread.start()
                expire_thread.join(timeout=3)
                handshake1 = expire_thread.get_result()
                addr = handshake1[1]
                if Packet.check_handshake(1, handshake1[0]):
                    self.sendto(Packet.handshake(2).encode(), addr)
                    logging.debug("Server receives handshake 2")
                    temp_state = 'ESTABLISHED'
                else:
                    temp_state = 'CLOSED'
            if temp_state == 'ESTABLISHED':
                logging.debug("Server connection established.")
                break
            if temp_state == 'CLOSED':
                temp_state = 'LISTEN'

        conn = RDTSocket()
        return conn, addr

    def connect(self, address: (str, int)):
        """
        Connect to a remote socket at address.
        Corresponds to the process of establishing a connection on the client side.
        send syn, receive syn, ack; send ack
        """

        # send syn
        self.sendto(Packet.handshake(0).encode(), address)
        logging.debug("Client sent handshake 0")

        handshake_1 = self.receive_handshake(1, 3)
        while handshake_1[1] != address:
            handshake_1 = self.receive_handshake(1, 3)
        logging.debug("Client received handshake 1")

        self.sendto(Packet.handshake(2).encode(), address)
        logging.debug("Client sent handshake 2")

        # raise NotImplementedError()

    def receive_handshake(self, number: int, max_retry: int) -> bytes:
        tmp_timeout = self.timeout
        i = 0
        while True:
            logging.debug(
                "Trying to receive handshake " + str(number) + " , " + str(i + 1) + (" time." if i == 0 else " times."))
            expire_thread = TimerThread(func=self.recvfrom_USocket, args=(2048,))
            expire_thread.start()
            expire_thread.join(timeout=tmp_timeout)
            handshake = expire_thread.get_result()
            i = i + 1
            tmp_timeout *= 2
            if i == max_retry:
                raise ConnectionError
            if handshake is not None and Packet.check_handshake(number, handshake[0]):
                break

        return handshake

    def recvfrom_USocket(self, buff_size: int) -> tuple:
        return super().recvfrom(buff_size)

    def recv(self, bufsize: int) -> bytes:
        """
        Receive data from the socket. 
        The return value is a bytes object representing the data received. 
        The maximum amount of data to be received at once is specified by bufsize. 
        
        Note that ONLY data send by the peer should be accepted.
        In other words, if someone else sends data to you from another address,
        it MUST NOT affect the data returned by this function.
        """
        data = None

        # assert self._recv_from, "Connection not established yet. Use recvfrom instead."
        #############################################################################
        # TODO: YOUR CODE HERE                                                      #
        #############################################################################
        data = super().recvfrom(bufsize)
        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################
        return data

    def send(self, bytes: bytes):
        """
        Send data to the socket. 
        The socket must be connected to a remote socket, i.e. self._send_to must not be none.
        """
        assert self._send_to, "Connection not established yet. Use sendto instead."
        #############################################################################
        # TODO: YOUR CODE HERE                                                      #
        #############################################################################
        raise NotImplementedError()
        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################

    def close(self):
        """
        Finish the connection and release resources. For simplicity, assume that
        after a socket is closed, neither futher sends nor receives are allowed.
        """
        #############################################################################
        # TODO: YOUR CODE HERE                                                      #
        #############################################################################

        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################
        super().close()

    def set_send_to(self, send_to):
        self._send_to = send_to

    def set_recv_from(self, recv_from):
        self._recv_from = recv_from


"""
You can define additional functions and classes to do thing such as packing/unpacking packets, or threading.

"""


class TimerThread(threading.Thread):

    def __init__(self, func, args=()):
        super(TimerThread, self).__init__()
        self.func = func
        self.args = args
        self.result = None

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
