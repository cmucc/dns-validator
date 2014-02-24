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

    def testValidateRecordPlus(self):
        self.assertTrue(validateRecordPlus(["a.cmu.edu", "192.168.1.1"])[0])
        self.assertTrue(validateRecordPlus(["a.cmu.edu", "192.168.1.1",
                                           "1234"])[0])
        self.assertFalse(validateRecordPlus(["a.cmu.edu", "192.168.1.1",
                                            "abc"])[0])
        self.assertFalse(validateRecordPlus(["a.cmu.edu", "b.cmu.edu",
                                            "1234"])[0])

    def testValidateRecordC(self):
        self.assertTrue(validateRecordC(["a.cmu.edu", "b.cmu.edu"])[0])
        self.assertTrue(validateRecordC(["a.cmu.edu", "b.cmu.edu",
                                           "1234"])[0])
        self.assertFalse(validateRecordC(["a.cmu.edu", "b.cmu.edu",
                                            "abc"])[0])
        self.assertTrue(validateRecordC(["a.cmu.edu", "192.168.1.1",
                                            "1234"])[0])

    def testStripComments(self):
        self.assertEqual(stripComments("#abcdef"), "")
        self.assertEqual(stripComments("abc#def"), "abc")
        self.assertEqual(stripComments("abcdef # #abc"), "abcdef ")

    def testValidateLine(self):
        self.assertTrue(validateLine("+a.cmu.edu:192.168.1.1:123")[0])
        self.assertTrue(validateLine("Ca.cmu.edu:192.168.1.1:123")[0])
        self.assertFalse(validateLine("+a.cmu.edu:b.cmu.edu:123")[0])
        self.assertTrue(validateLine("Ca.cmu.edu:b.cmu.edu:123")[0])

if __name__ == "__main__":
    unittest.main()
