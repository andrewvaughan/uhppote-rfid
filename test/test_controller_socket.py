#!/usr/bin/env python

import mock
import os
import socket
import threading
import time
import unittest

from uhppote_rfid import ControllerSocket, SocketConnectionException, SocketTransmitException


class TestControllerSocket(unittest.TestCase):
    """
    Tests UHPPOTE socket transmission by emulating the control board's server.
    """


    def setUp(self):
        """
        .. function:: setUp()

           Runs a server locally on port 60000 to listen for connections to respond accordingly.
        """
        self.server = socket.socket()
        self.server.bind(('127.0.0.1', 60000))
        self.server.listen(1)

        self.socket = ControllerSocket('127.0.0.1')


    def tearDown(self):
        """
        .. function:: tearDown()

           Cleanly shuts down the test suite's server.
        """
        self.socket.close()
        self.sockt = None

        self.server.close()
        self.server = None


    # Socket.__init__

    def test_constructor_NegativePort_Exception(self):
        with self.assertRaises(ValueError):
            ControllerSocket('127.0.0.1', -1)

    def test_constructor_ZeroPort_Exception(self):
        with self.assertRaises(ValueError):
            ControllerSocket('127.0.0.1', 0)

    def test_constructor_LargePort_Exception(self):
        with self.assertRaises(ValueError):
            ControllerSocket('127.0.0.1', 65535 + 1)

    def test_constructor_BlankPort_Exception(self):
        with self.assertRaises(ValueError):
            ControllerSocket('127.0.0.1', '')

    def test_constructor_NonIntStringPort_Exception(self):
        with self.assertRaises(ValueError):
            ControllerSocket('127.0.0.1', 'ab')

    def test_constructor_FloatPort_Exception(self):
        with self.assertRaises(ValueError):
            ControllerSocket('127.0.0.1', 1.1)

    def test_constructor_ByteArrayPort_Exception(self):
        with self.assertRaises(ValueError):
            ControllerSocket('127.0.0.1', bytearray([0, 5, 2]))

    def test_constructor_EmptyHost_Exception(self):
        with self.assertRaises(ValueError):
            ControllerSocket('')

    def test_constructor_IntegerHost_Exception(self):
        with self.assertRaises(ValueError):
            ControllerSocket(55)

    def test_constructor_ByteArrayHost_TooLongException(self):
        with self.assertRaises(ValueError):
            ControllerSocket(bytearray([127, 0, 0, 1, 5]))

    def test_constructor_ByteArrayHost_TooShortException(self):
        with self.assertRaises(ValueError):
            ControllerSocket(bytearray([127, 0, 0]))

    def test_constructor_NegativeIP01_Exception(self):
        with self.assertRaises(ValueError):
            ControllerSocket('-1.0.0.0')

    def test_constructor_NegativeIP02_Exception(self):
        with self.assertRaises(ValueError):
            ControllerSocket('0.-1.0.0')

    def test_constructor_NegativeIP03_Exception(self):
        with self.assertRaises(ValueError):
            ControllerSocket('0.0.-3.0')

    def test_constructor_NegativeIP04_Exception(self):
        with self.assertRaises(ValueError):
            ControllerSocket('0.0.0.-1')

    def test_constructor_TooLongHost_Exception(self):
        with self.assertRaises(ValueError):
            ControllerSocket('longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.longhost.long')

    def test_constructor_BadChar_Exception(self):
        with self.assertRaises(ValueError):
            ControllerSocket('Hello*World')

    def test_constructor_DefaultPort_Valid(self):
        self.assertEquals(self.socket.getPort(), 60000)

    def test_constructor_IntegerPort_Valid(self):
        socket = ControllerSocket("127.0.0.1", 59)
        self.assertEquals(socket.getPort(), 59)

    def test_constructor_StringIntegerPort_Valid(self):
        socket = ControllerSocket("127.0.0.1", '128')
        self.assertEquals(socket.getPort(), 128)

    def test_constructor_StringHost_Valid(self):
        self.assertEquals(self.socket.getHost(), "127.0.0.1")

    def test_constructor_ByteArrayHost_Valid(self):
        socket = ControllerSocket(bytearray([127, 0, 0, 1]))
        self.assertEquals(socket.getHost(), "127.0.0.1")

    def test_constructor_DotAtEndHost_Valid(self):
        socket = ControllerSocket("localhost.")
        self.assertEquals(socket.getHost(), "localhost")


    # Socket.connect

    def test_connect_ZeroAttempts_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.connect(0)

    def test_connect_NegativeAttempts_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.connect(-1)

    def test_connect_DefaultAttemptsFail_Exception(self):
        socket = ControllerSocket('badhost')
        with self.assertRaises(SocketConnectionException):
            socket.connect()

    def test_connect_ConnectLocal_Success(self):
        try:
            self.socket.connect()
        except SocketConnectionException, e:
            self.fail("Unexpected SocketConnectionException raisesd: %s" % str(e))


    # Socket.close

    def test_close_CloseInactive_Success(self):
        try:
            self.socket.close()
        except Exception, e:
            self.fail("Unexpected Exception raised: %s" % str(e))

    def test_close_CloseActive_Success(self):
        self.socket.connect()

        try:
            self.socket.close()
        except Exception, e:
            self.fail("Unexpected Exception raisesd: %s" % str(e))

    def test_close_ClosedNotConnected_Success(self):
        self.assertFalse(self.socket.isConnected())

        self.socket.connect()
        self.assertTrue(self.socket.isConnected())

        self.socket.close()
        self.assertFalse(self.socket.isConnected())



    # Socket.send

    def test_send_Integer_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.send(42)

    def test_send_Float_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.send(4.2)

    def test_send_Complex_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.send(complex(4, 2))

    def test_send_Tuple_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.send((4, 2))

    def test_send_List_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.send([4, 2])

    def test_send_Dict_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.send({
                'a': 4,
                'b': 2,
            })

    def test_send_Set_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.send(set([4, 2]))

    def test_send_FrozenSet_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.send(frozenset([4, 2]))

    def test_send_EmptyString_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.send('')

    def test_send_EmptyByteArray_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.send(bytearray())

    def test_send_EmptyBytes_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.send(bytes(''))

    def test_send_ClosedSocket_Exception(self):
        self.socket.close()
        with self.assertRaises(SocketConnectionException):
            self.socket.send('hello')

    def test_send_Interrupt_Exception(self):
        with mock.patch('uhppote_rfid.controller_socket.socket') as mock_socket:
            mockSocket = ControllerSocket('127.0.0.1')
            mockSocket.socket.send.return_value = 0

            mockSocket.connect()

            with self.assertRaises(SocketTransmitException):
                mockSocket.send('hello')

    def test_send_String_Valid(self):
        data = 'Hello World'

        with mock.patch('uhppote_rfid.controller_socket.socket') as mock_socket:
            mockSocket = ControllerSocket('127.0.0.1')
            mockSocket.connect()
            mockSocket.send(data)
            mockSocket.socket.send.assert_called_with(data)


    def test_send_ByteArray_Valid(self):
        data = bytearray(['h', 'e', 'l', 'l', 'o'])

        with mock.patch('uhppote_rfid.controller_socket.socket') as mock_socket:
            mockSocket = ControllerSocket('127.0.0.1')
            mockSocket.connect()
            mockSocket.send(data)
            mockSocket.socket.send.assert_called_with(data)

    def test_send_Bytes_Valid(self):
        data = bytes([10, 20, 30, 40])

        with mock.patch('uhppote_rfid.controller_socket.socket') as mock_socket:
            mockSocket = ControllerSocket('127.0.0.1')
            mockSocket.connect()
            mockSocket.send(data)
            mockSocket.socket.send.assert_called_with(data)


    # Socket.receive

    def test_receive_NegativeLength_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.receive(-1)

    def test_receive_ZeroLength_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.receive(0)

    def test_receive_NotMultipleOf8_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.receive(50)

    def test_receive_FloatLength_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.receive(8.8)

    def test_receive_ComplexLength_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.receive(complex(4, 2))

    def test_receive_TupleLength_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.receive((4, 2))

    def test_receive_ListLength_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.receive([4])

    def test_receive_DictLength_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.receive({
                'a': 1
            })

    def test_receive_SetLength_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.receive(set([4, 2]))

    def test_receive_FrozenSetLength_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.receive(frozenset([4, 2]))

    def test_receive_StringEmpty_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.receive('')

    def test_receive_StringAlpha_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.receive('a')

    def test_receive_StringZero_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.receive('0')

    def test_receive_StringNegative_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.receive('-1')

    def test_receive_StringNotMultipleOf8_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.receive('50')

    def test_receive_StringFloat_Exception(self):
        with self.assertRaises(ValueError):
            self.socket.receive('8.8')

    def test_receive_StringSize_Valid(self):
        pass

    def test_receive_ClosedSocket_Exception(self):
        self.socket.close()
        with self.assertRaises(SocketConnectionException):
            self.socket.receive()

    def test_receive_Cutoff_Exception(self):
        with mock.patch('uhppote_rfid.controller_socket.socket') as mock_socket:
            mockSocket = ControllerSocket('127.0.0.1')
            mockSocket.socket.recv.return_value = ''

            mockSocket.connect()

            with self.assertRaises(SocketTransmitException):
                mockSocket.receive()

    def test_receive_DefaultLength_Valid(self):
        arr = [1, 2, 3, 4, 5, 6, 7, 8]

        with mock.patch('uhppote_rfid.controller_socket.socket') as mock_socket:
            mockSocket = ControllerSocket('127.0.0.1')
            mockSocket.socket.recv.return_value = bytearray(arr)

            data = bytearray()
            for i in range(0, 8):
                data.extend(arr)

            mockSocket.connect()
            self.assertEquals(mockSocket.receive(), data)

    def test_receive_SetLength_Valid(self):
        data = bytearray([1, 2, 3, 4, 5, 6, 7, 8])

        with mock.patch('uhppote_rfid.controller_socket.socket') as mock_socket:
            mockSocket = ControllerSocket('127.0.0.1')
            mockSocket.socket.recv.return_value = data

            mockSocket.connect()
            self.assertEquals(mockSocket.receive(len(data)), data)




if __name__ == '__main__':
    unittest.main()
