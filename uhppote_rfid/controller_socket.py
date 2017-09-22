# -*- coding: utf-8 -*-
"""
Provides socket and communication support for UHPPOTE RFID control boards.

   :copyright: (c) 2017 by Andrew Vaughan.
   :license: Apache 2.0, see LICENSE for more details.

.. module:: ControllerSocket
"""

import binascii
import logging
import re
import socket


class ControllerSocket(object):
    """
    Manages socket communication and transport for UHPPOTE RFID boards.

    .. class:: ControllerSocket
    .. versionadded:: 0.1.0
    """

    def __init__(self, host, port=60000):
        """
        Initialize a new Socket given an IP address and port for the control board.

           :param host: the hostname or IP address of the control board
           :type host: str
           :param port: the port of the control board (default: 60000)
           :type port: int

           :raises ValueError: if provided an invalid host or port

        .. versionadded:: 0.1.0
        .. function:: __init__(host[, port])
        """
        self.logger = logging.getLogger("UHPPOTE.ControllerSocket")

        self.setHost(host)
        self.setPort(port)
        self.connected = False

        self.logger.debug("Creating socket on %s:%d (not connected)" % (self.getHost(), self.getPort()))
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )


    def connect(self, attempts=3):
        """
        Attempt to connect to the target as-configured.

           :param attempts: the number of times to retry connecting before throwing an exception (default: 3)
           :type attempts: int

           :raises ValueError: if attempts is below 1
           :raises SocketConnectionException: if unable to connect after the prescribed number of retries

        .. versionadded:: 0.1.0
        .. function:: connect([attempts])
        """
        self.logger.debug("Connecting to %s:%d via socket" % (self.host, self.port))

        if int(attempts) <= 0:
            raise ValueError("Invalid number of attempts for socket connection: %d" % int(attempts))

        for attempt in range(1, attempts + 1):
            self.logger.debug("Attempt #%d..." % attempt)

            try:
                self.socket.connect((self.host, self.port))
                self.connected = True
                self.logger.debug("Connection successful.")
                return

            except Exception, e:
                self.logger.warn("Connection attempt #%d to %s:%d unsuccessful.  Error message: %s" % (attempt, self.host, self.port, str(e)))
                pass

        raise SocketConnectionException("Unable to connect to %s:%d after %d attempts." % (self.host, self.port, int(attempts)))


    def close(self):
        """
        Attempt to close the open connection.

           :returns: True if the socket was closed, or False if it remains open
           :rtype: bool

        .. versionadded:: 0.1.0
        .. function:: close()
        """
        self.logger.debug("Closing socket...")
        self.socket.close()
        self.connected = False


    def send(self, msg):
        """
        Send a message through a connected socket.

           :param msg: the message to send through the socket
           :type msg: str or bytearray or bytes

           :raises ValueError: if the message being sent is in an invalid format
           :raises SocketConnectionException: if the socket does not have a working connection
           :raises SocketTransmitException: if the socket connection is broken during transmission

        .. versionadded:: 0.1.0
        .. function:: send(msg)
        """
        if not isinstance(msg, (str, bytes, bytearray)):
            raise ValueError("Invalid message sent to socket.  Expected str, bytes, or bytearray; received %s." % type(msg))

        messageLength = len(msg)

        if messageLength <= 0:
            raise ValueError("Expected message to be sent.  Received blank message.")

        if not self.isConnected():
            raise SocketConnectionException("Socket not connected. Cannot send.")

        self.logger.debug("Attempting to send message through socket of length %d." % messageLength)
        self.logger.log(1, binascii.hexlify(msg))

        byteCount = 0
        while byteCount < messageLength:
            sent = self.socket.send(msg[byteCount:])

            if sent == 0:
                raise SocketTransmitException("Connection broken.")

            self.logger.log(1, "%d bytes sent in chunk..." % sent)
            byteCount += sent

        self.logger.debug("Send complete (%d bytes)." % byteCount)


    def receive(self, size=64):
        """
        Receive a message through a connected socket.  Will block I/O until enough bytes to get `size` are returned.

           :param size: the size, in bytes, expected for the incoming message
           :type size: int

           :returns: the received message
           :rtype: bytearray

           :raises ValueError: if the size is not a positive multiple of 8
           :raises SocketConnectionException: if the socket does not have a working connection
           :raises SocketTransmitException: if the socket connection is broken during transmission

        .. versionadded:: 0.1.0
        .. function:: receive([size])
        """
        self.logger.debug("Listening for message via socket of length %s..." % str(size))

        if isinstance(size, str):
            if not size.isdigit():
                raise ValueError("Invalid size. Non-Integer string provided: \"%s\"." % size)

            size = int(size)

        if not isinstance(size, (int, long)):
            raise ValueError("Invalid size. Expected positive integer; received \"%s\"." % type(size))

        if size <= 0:
            raise ValueError("Packet size must be a positive integer; received \"%d\"." % size)

        if size % 8 != 0:
            raise ValueError("Packet size must be a multiple of 8; received \"%d\"." % size)

        if not self.isConnected():
            raise SocketConnectionException("Socket not connected. Cannot receive.")

        received = bytearray()
        received_bytes = 0
        while received_bytes < size:
            chunk = self.socket.recv(min(size, 2048))

            if chunk == '':
                raise SocketTransmitException("Unexpected end of connection.  Received %d bytes, but expected %d." % (received_bytes, size))

            received.extend(chunk)
            received_bytes += len(chunk)

            self.logger.log(1, "%d bytes received in chunk..." % len(chunk))

        self.logger.log(1, binascii.hexlify(received))

        return received


    def getHost(self):
        """
        Return the hostname of the socket.

           :returns: the hosthame of the socket
           :rtype: str

        .. versionadded:: 0.1.0
        .. function:: getHost()
        """
        return self.host


    def setHost(self, host):
        """
        Set the hostname for the socket.

           :param host: the hostname for the socket
           :type host: str or bytearray

           :raises ValueError: if provided an invalid host

        .. versionadded: 0.1.0
        .. function:: setHost(host)
        """
        if not isinstance(host, (str, bytearray)):
            raise ValueError("Invalid host provided. Expected string or bytearray; received %s." % type(host))

        if isinstance(host, bytearray):
            if len(host) != 4:
                raise ValueError("Invalid host provided. Bytearray must contain 4 values; received %d values." % len(host))

            host = "%d.%d.%d.%d" % (host[0], host[1], host[2], host[3])

        if len(host) <= 0 or len(host) > 255:
            raise ValueError("Invalid host provided. Length cannot be 0 or longer than 255 characters; received \"%s\"." % host)

        # Valid hostnames can have one dot at the end; strip it if it exists
        if host[-1] == ".":
            host = host[:-1]

        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        if not all(allowed.match(c) for c in host.split(".")):
            raise ValueError("Invalid host provided. Received \"%s\"." % host)

        self.host = host


    def getPort(self):
        """
        Return the port for the socket.

           :returns: the port for the socket
           :rtype: int

        .. versionadded:: 0.1.0
        .. function:: getPort()
        """
        return self.port


    def setPort(self, port):
        """
        Set the port for the socket.

           :param port: the port for the socket
           :type port: int

           :raises ValueError: if provided an invalid port

        .. versionadded:: 0.1.0
        .. function:: setPort(port)
        """
        if isinstance(port, str):
            if not port.isdigit():
                raise ValueError("Invalid port. Non-Integer string provided: \"%s\"." % port)

        elif not isinstance(port, (int, long)):
            raise ValueError("Invalid port. Expected positive integer; received \"%s\"." % type(port))

        if int(port) <= 0:
            raise ValueError("Invalid port. Expected positive integer; received \"%d\"." % port)

        if int(port) > 65535:
            raise ValueError("Invalid port. Exceeds maximum of 65535; received \"%d\"." % port)

        self.port = int(port)


    def isConnected(self):
        """
        Return whether the socket is currently connected to a server.

           :returns: whether the socket is currently connected to a server
           :rtype: bool

        .. versionadded: 0.1.0
        .. function:: isConnected()
        """
        return self.connected




class SocketConnectionException(Exception):
    """
    Custom exception raised if a socket fails to connect to its target.

    .. versionadded:: 0.1.0
    """

    pass


class SocketTransmitException(Exception):
    """
    Custom exception raised if a problem occurs during transmission.

    .. versionadded:: 0.1.0
    """

    pass
