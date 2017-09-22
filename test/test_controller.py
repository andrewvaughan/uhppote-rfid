#!/usr/bin/env python

import mock
import os
import socket
import threading
import time
import unittest

from uhppote_rfid import Controller, ControllerFunction, InvalidResponseException


class TestController(unittest.TestCase):
    """
    Tests the main UHPPOTE RFID controller and related classes.
    """

    def test_constructor_BadHost_Exception(self):
        pass




if __name__ == '__main__':
    unittest.main()
