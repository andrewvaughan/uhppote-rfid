#!/usr/bin/env python
"""
Test suite for the UHPPOTE RFID controller board module.

.. moduleauthor:: Andrew Vaughan <hello@andrewvaughan.io>
"""

import unittest

if __name__ == '__main__':
    testsuite = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=1).run(testsuite)
