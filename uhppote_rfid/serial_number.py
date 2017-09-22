# -*- coding: utf-8 -*-
"""
Provides serial number support for UHPPOTE RFID control boards.

   :copyright: (c) 2017 by Andrew Vaughan.
   :license: Apache 2.0, see LICENSE for more details.

.. module:: SerialNumber
"""

import binascii
import logging
import string


class SerialNumber(object):
    """
    Manages serial numbers for UHPPOTE RFID systems.

    .. class:: SerialNumber
    .. versionadded:: 0.1.0
    """

    def __init__(self, serial):
        """
        Initialize a new SerialNumber.  Serial numbers can be provided in one of several formats.

        Serial Number Formats
        ---------------------

        9-Digit `int` or `str`
        ++++++++++++++++++++++
        If a 9-digit `int` or `str` (e.g., "9b87a8") is provided, it will be treated as the 9-digit value from the
        sticker on the physical controller board.

        Hexadecimal
        +++++++++++
        If a hexadecimal value (e.g., "0x9b87a8") or an 8-character string of hexadecimal numbers is provided, it will
        be treated as the final four pairs of hexadecimal numbers from the MAC address of the controller board.  The
        MAC address of the controller board can be found by running a Search function on the controller board.

        4-Byte `bytearray`
        ++++++++++++++++++
        If a 4-byte `bytearray` is provided, it will be treated as the final four pairs of hexadecimal numbers from
        the MAC address of the controller board, in order.

           :param serial: the serial number as either a string, integer, or bytearray
           :type serial: str or int or bytearray

           :raisess SerialNumberException: if the provided serial number is in the incorrect format

        .. versionadded:: 0.1.0
        .. function:: __init__(serial)
        """
        self.logger = logging.getLogger("UHPPOTE.SerialNumber")

        # If this is a bytearray, convert it to a 9-digit integer for transformation later
        if isinstance(serial, bytearray):
            self.logger.debug("Serial number provided as bytearray length %d.  Converting from bytes to integer.", len(serial))

            if len(serial) != 4:
                raise SerialNumberException("SerialNumber as bytearray requires exactly 4 bytes.  Received bytearray of length %d." % len(serial))

            self.serialInteger = int(binascii.hexlify(serial), 16)

        # If this is a string, check for different types
        elif isinstance(serial, str):
            self.logger.debug("Serial number provided as string (%s).  Converting from hexadecimal to integer.", serial)

            # If it's a hexadecimal number in python-format, convert it from base-16
            if serial[0:2] == "0x":
                if not all(c in string.hexdigits for c in serial[2:]):
                    raise SerialNumberException("SerialNumber provided invalid hexadecimal string.  Received \"%s\"." % serial)

                self.serialInteger = int(serial, 16)

            # If the serial number is 8-digits and all hex, convert it as hex
            elif len(serial) == 8 and all(c in string.hexdigits for c in serial):
                self.serialInteger = int("0x" + serial, 16)

            # Otherwise, treat the string as a controller-board, 9-digit serial
            elif len(serial) == 9:
                try:
                    self.serialInteger = int(serial)
                except ValueError:
                    raise SerialNumberException("SerialNumber invalid.  Received \"%s\"." % str(serial))

            else:
                raise SerialNumberException("SerialNumber as string must be hexadecimal or 9-digit integer.  Received \"%s\"." % str(serial))


        # If provided an integer, use it
        elif isinstance(serial, (int, long)):
            self.logger.debug("Serial number provided as integer (%d).", serial)
            self.serialInteger = int(serial)

        # Unknown type
        else:
            raise SerialNumberException("SerialNumber provided as unknown type.  Expected integer, string, or bytearray.")


        # Check bounds
        if self.serialInteger < 0 or self.serialInteger > 999999999:
            raise SerialNumberException("SerialNumber is out of bounds.  Must be between 0 and 999,999,999.  Received \"%d\"." % self.serialInteger)

        self.logger.debug("Serial number stored as %d (%s)." % (self.getInteger(), self.getHexadecimalString()))


    def __str__(self):
        """
        Return a string representation of the SerialNumber.

           :returns: the serial number as a string
           :rtype: str

        .. versionadded:: 0.1.0
        .. SerialNumber:function:: __str__()
        """
        return self.getHexadecimalString()


    def getInteger(self):
        """
        Return the serial number as an integer.

        It may not be 9-digits if pre-padded by 0s.  Use a string representation if 9-digits are required.

           :returns: the serial number as an integer
           :rtype: int

        .. versionadded:: 0.1.0
        .. SerialNumber:function:: getInteger()
        """
        return self.serialInteger


    def getIntegerString(self):
        """
        Return the serial number as a 9-digit string representation.

           :returns: the serial number as a 9-digit string
           :rtype: str

        .. versionadded:: 0.1.0
        .. SerialNumber:function:: getIntegerString()
        """
        return str(self.getInteger()).zfill(9)


    def getHexadecimal(self):
        """
        Return the serial number as a hexadecimal.

           .. note::
              The hexadecimal value provided may not be exactly 8-digits and should not be used for direct communication
              with the control board.

           :returns: the serial number as a hexadecimal string
           :rtype: str

        .. versionadded:: 0.1.0
        .. SerialNumber:function:: getHexadecimal()
        """
        return hex(self.getInteger())


    def getHexadecimalString(self, reverse=False):
        """
        Return the serial number as a 8-character string of hexadecimal digits.

        Certain functions for the control board require the hexadecimal pairs to be reversed, so a `reverse` parameter
        is provided.

           :param reverse: whether to return the number as reversed bytes (default False)
           :type reverse: bool

           :returns: the serial number as a hexadecimal string without the "0x" prefix
           :rtype: str

        .. versionadded:: 0.1.0
        .. SerialNumber:function:: getHexadecimalString([reverse])
        """
        if not reverse:
            return "{:08x}".format(self.getInteger())

        to_reverse = self.getHexadecimalString()
        return "".join(reversed([to_reverse[i:i + 2] for i in range(0, len(to_reverse), 2)]))


    def getByteArray(self, reverse=False):
        """
        Return the serial number as a 4-length byte array of hexadecimal values.

        Certain functions for the control board require the hexadecimal pairs to be reversed, so a `reverse` parameter
        is provided.

           :param reverse: whether to return the serial number as reversed bytes
           :type reverse: bool

           :returns: the serial number as a 4-length array of bytes
           :rtype: bytearray

        .. versionadded:: 0.1.0
        .. SerialNumber:function:: getByteArray([reverse])
        """
        return bytearray.fromhex(self.getHexadecimalString(reverse))




class SerialNumberException(Exception):
    """
    Custom exception for use with SerialNumber objects.

    .. versionadded:: 0.1.0
    """

    pass
