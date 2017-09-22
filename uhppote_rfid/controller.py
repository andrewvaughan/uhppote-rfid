# -*- coding: utf-8 -*-
"""
Integrates with UHPPOTE RFID access control boards.

   :copyright: (c) 2017 by Andrew Vaughan.
   :license: Apache 2.0, see LICENSE for more details.

.. module:: Controller
"""

import logging
import binascii

from . import ControllerSocket, SerialNumber


class Controller(object):
    """
    Communicates with UHPPOTE RFID access control boards.

    .. class:: Controller
    .. versionadded:: 0.1.0
    """

    VERSION = 0x17

    def __init__(self, host, serial_number, port=60000):
        """
        Create a new connection to a UHPPOTE RFID control board.

           :param host: the hostname or IP address of the control board
           :type host: str
           :param serial_number: the serial number of the control board
           :type serial_number: str
           :param port: the port of the control board (default: 60000)
           :type port: int

           :raises ValueError: if provided an invalid host or port
           :raisess SerialNumberException: if the provided serial number is in the incorrect format

        .. versionadded:: 0.1.0
        .. function:: __init__(host, serial_number[, port])
        """
        self.logger = logging.getLogger("UHPPOTE")

        self.socket = ControllerSocket(host, port)
        self.serial_number = SerialNumber(serial_number)

        self.logger.debug("Creating Controller for board at %s:%d (not connected)" % (self.getHost(), self.getPort()))


    def getStatus(self):
        """
        Poll the control board for its current status.

            :returns: a dict containing the status of the control board
            :rtype: dict

        .. versionadded:: 0.1.0
        .. function:: getStatus(self)
        """
        self.logger.debug(
            "Requesting current status from control board at %s:%d..." % (self.getHost(), self.getPort())
        )

        received = self._communicate(
            ControllerFunction.DEV_STATUS
        )

        return ControllerStatus(received)


    def getHost(self):
        """
        Return the hostname of the control board.

           :returns: the hosthame of the control board, as configured
           :rtype: str

        .. versionadded:: 0.1.0
        .. function:: getHost()
        """
        return self.socket.getHost()


    def setHost(self, host):
        """
        Set the hostname for the control board.

           :param host: the hostname for the control board
           :type host: str or bytearray

           :raises ValueError: if provided an invalid host

        .. versionadded: 0.1.0
        .. function:: setHost(host)
        """
        self.socket.setHost(host)


    def getPort(self):
        """
        Return the port for the control board.

           :returns: the port for the control board
           :rtype: int

        .. versionadded:: 0.1.0
        .. function:: getPort()
        """
        return self.socket.getPort()


    def setPort(self, port):
        """
        Set the port for the control board.

           :param port: the port for the control board
           :type port: int

           :raises ValueError: if provided an invalid port

        .. versionadded:: 0.1.0
        .. function:: setPort(port)
        """
        self.socket.setPort(port)


    def _communicate(self, function, args=bytearray(), send_serial=True):
        """
        Send a message to the control board.

        Will ensure a 64-byte array (or 128-length hex string) message and listens for a response.

            :param function: the function to communicate to the board
            :type function: int
            :param args: an array of bytes to append to the message (default: none)
            :type args: bytearray
            :param send_serial: whether or not to send the reversed serial number with the command (default: True)
            :type send_serial: bool

            :raises ValueError: if the function provided is an invalid integer
            :raises ValueError: if the args provided are too long or in an invalid format

        .. versionadded:: 0.1.0
        .. function:: _communicate(port)
        """
        if not isinstance(function, (int, long)):
            raise ValueError("Function to communicate must be an integer.  Received %s." % type(function))

        if function < 0x20 or function > 0x82:
            raise ValueError("Function to communicate must be within range 0x20 to 0x82.  Received %d." % function)

        if not isinstance(args, bytearray):
            raise ValueError("Invalid arguments provided for communication. Expected bytearray, receveid %s." % args)

        if len(args) + (1 if send_serial else 0) > 60:
            raise ValueError("Too many arguments.  Total messgae must be less than 64-bytes.")

        self.logger.debug("Communicating to control board for function %s." % hex(function))

        # Build the output as configured by the control board
        output = bytearray()

        output.extend([0x17])       # Type/Version used by board
        output.extend([function])   # The function to send to the board
        output.extend([0x0, 0x0])   # Two-byte zero buffer

        # Add the reversed serial number, if it is required
        if send_serial:
            serialFormat = self.serial_number.getByteArray(True)
            output.extend(serialFormat)

        # Add any other arguments to the output, in order
        output.extend(args)

        # Pad to exactly 64-bytes for the server
        output.extend("\0" * (64 - len(output)))

        self.logger.debug(binascii.hexlify(output))

        self.socket.connect()
        self.socket.send(output)

        self.logger.debug("Send complete.")

        # Wait to listen for a response...
        self.logger.debug("Waiting for response...")
        returnValue = self.socket.receive(64)
        self.logger.debug(binascii.hexlify(returnValue))

        if len(returnValue) != 64:
            raise InvalidResponseException(
                "Unexpected response from controller; expected length 64, received length %d." % len(returnValue)
            )

        if returnValue[0] != Controller.VERSION:
            raise InvalidResponseException(
                "Unexpected version responded from controller; expected [0] to contain version %s, received %s" % (
                    hex(Controller.VERSION),
                    hex(returnValue[0]),
                )
            )

        if returnValue[1] != function:
            raise InvalidResponseException(
                "Unexpected response from controller; expected [1] to contain function %s, received %s" % (
                    hex(function),
                    hex(returnValue[1]),
                )
            )

        if returnValue[2:3] != 0x0:
            raise InvalidResponseException(
                "Unexpected response from controller; expected [2:3] to contain buffer 0x0 0x0, receved %s %s" % (
                    hex(returnValue[2]),
                    hex(returnValue[3]),
                )
            )

        if send_serial:
            if returnValue[4:8] != serialFormat:
                raise InvalidResponseException(
                    "Unexpected response from controller; expected [4:8] to contain serial %s, received %s." % (
                        binascii.hexlify(serialFormat),
                        hex(returnValue[4:8]),
                    )
                )

        self.socket.close()

        return returnValue




class ControllerFunction(object):
    """
    Enumeration for UHPPOTE RFID controllers.

    .. class:: ControllerFunctions
    .. versionadded:: 0.1.0
    """

    DEV_STATUS = 0x20




class ControllerStatus(object):
    """
    Contains information regarding status from the controller.

    Response bytes is as-follows:

             00 | 1 Byte  | Version Check (0x17)
             01 | 1 Byte  | Function Check (0x20)
        02 - 03 | 2 Bytes | Buffer (0x00, 0x00)
        04 - 07 | 4 Bytes | Serial Number (Reversed)
        08 - 11 | 4 Bytes | "Last Index (Reversed)"
             12 | 1 Byte  | "Latest Swipe"
             13 | 1 Byte  | "No Access"
             14 | 1 Byte  | Last Door Number
             15 | 1 Byte  | Last Door Is Open (0 closed, 1 open)
        16 - 19 | 4 Bytes | Last Card ID (Reversed)
        20 - 26 | 7 Bytes | Last Swipe Time
             27 | 1 Byte  | Last Swipe Reason
             28 | 1 Byte  | Door 1 Status (0 closed, 1 open)
             29 | 1 Byte  | Door 2 Status (0 closed, 1 open)
             30 | 1 Byte  | Door 3 Status (0 closed, 1 open)
             31 | 1 Byte  | Door 4 Status (0 closed, 1 open)
             32 | 1 Byte  | Door 1 Button Status (0 released, 1 pressed)
             33 | 1 Byte  | Door 2 Button Status (0 released, 1 pressed)
             34 | 1 Byte  | Door 3 Button Status (0 released, 1 pressed)
             35 | 1 Byte  | Door 4 Button Status (0 released, 1 pressed)
             36 | 1 Byte  | System Status (0 okay, other is error code)
        37 - 39 | 3 Bytes | System Time (HH, MM, SS)
        40 - 43 | 4 Bytes | "Packet Serial Number"
        44 - 47 | 4 Bytes | "Backup"
             48 | 1 Byte  | "Special Message"
             49 | 1 Byte  | Bit-Based Door Relay Status
                          |     & 0x1 = 1 (Door 1 unlocked)
                          |     & 0x2 = 1 (Door 2 unlocked)
                          |     & 0x4 = 1 (Door 3 unlocked)
                          |     & 0x8 = 1 (Door 4 unlocked)
             50 | 1 Byte  | Bit-Based Fire Status
                          |     & 0x1 = 1 (Forced lock door)
                          |     & 0x2 = 1 (Fire)
        51 - 53 | 3 Bytes | System Date (YY, MM, DD)

    .. class:: ControllerStatus
    .. versionadded:: 0.1.0
    """

    def __init__(self, bytecode):
        """
        Initialize a new controller status object.

           :param bytecode: the bytecode resposne from the controller board
           :type bytecode: bytearray

           :raises ValueError: if the bytecode provided is not the right type or exactly 64-bytes

        .. function:: __init__(bytecode)
        .. versionadded:: 0.1.0
        """
        if not isinstance(bytecode, bytearray):
            raise ValueError("Invalid type provided; expected bytearray, recevied %s." % type(bytecode))

        if len(bytecode) != 64:
            raise ValueError("Invalid length bytearray; expected 64-bytes, received %d-bytes." % len(bytecode))

        self.bytecode = bytecode


    def getLastIndex(self):
        """
        Return the Last Index of the controller board.

            :returns: an integer representation of the last index
            :rtype: int

        .. warning:: It is unknown what this field currently means.  This will be resolved at a later time.  Until
                     then, this function's return value should be expected to change.

        .. function:: getLastIndex()
        .. versionadded:: 0.1.0
        """
        return self._getInteger(8, 4, True)


    def _getHexString(begin, length=1, reverse=False):
        """
        Convert a section of the bytearray to a hexadecimal string.

            :param begin: the index of the bytearray to start
            :type begin: int
            :param length: the length of the bytecode to convert (default: 1)
            :type length: int
            :param reverse: whether to reverse the bytes (default: False)
            :type reverse: bool

            :returns: the provided bytes as a hexadecimal string
            :rtype: string

            :raises ValueError: if the byte locations are invalid
        """
        if begin < 0 or begin >= 64:
            raise ValueError("Invalid range provided; expected start between 0 and 63, received %d." % begin)

        if length <= 0:
            raise ValueError("Invalid length provided; expected positive number, received %d." % length)

        if begin + length >= 64:
            raise ValueError("Invalid range provided; end expected to be within 63, received %d." % (begin + length))




    def _getInteger(begin, length=1, reverse=False):
        """
        Convert a section of the bytearray to an integer.

            :param begin: the index of the bytearray to start
            :type begin: int
            :param length: the length of the bytecode to convert (default: 1)
            :type length: int
            :param reverse: whether to reverse the bytes before conversion (default: False)
            :type reverse: bool

            :returns: the provided bytes in integer form
            :rtype: int

            :raises ValueError: if the byte locations are invalid
        """
        hexCode = self._getHexString(begin, length, reverse)

        return int(hexCode, 16)




class InvalidResponseException(Exception):
    """
    Raise an exception for an unexpected response from the controller.

    .. class:: InvalidResponseException
    .. versionadded:: 0.1.0
    """

    pass
