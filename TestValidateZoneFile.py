#!/usr/bin/env python

import unittest
from ValidateZoneFile import *

class TestIsCorrectZoneFile(unittest.TestCase):

    def testIsCorrectHostName(self):
        self.assertTrue(isCorrectHostName("cc.cmu.edu"))
        self.assertTrue(isCorrectHostName("a_b.cmu.edu")) # allow underscore
        self.assertTrue(isCorrectHostName("a-b.cmu.edu")) # allow hyphen
        self.assertFalse(isCorrectHostName("cc.cmu .edu")) # spaces not allowed
        self.assertFalse(isCorrectHostName("cc.cmu.edu*")) # invalid char

    def testIsCorrectInteger(self):
        self.assertTrue(isCorrectInteger("0"))
        self.assertTrue(isCorrectInteger("12"))
        self.assertTrue(isCorrectInteger("123"))
        self.assertFalse(isCorrectInteger("023"))
        self.assertFalse(isCorrectInteger("0a3"))

    def testIsCorrectIPv4(self):
        self.assertTrue(isCorrectIPv4("192.168.1.1"))
        self.assertTrue(isCorrectIPv4("255.255.255.255"))
        self.assertTrue(isCorrectIPv4("255.0.0.0"))
        self.assertFalse(isCorrectIPv4("255.256.255.255"))
        self.assertFalse(isCorrectIPv4("abc.255.255.255"))

if __name__ == "__main__":
    unittest.main()
