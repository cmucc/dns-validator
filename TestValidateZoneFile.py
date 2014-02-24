#!/usr/bin/env python

import unittest
from ValidateZoneFile import *

class TestValidateZoneFile(unittest.TestCase):

    def testValidateHostName(self):
        self.assertTrue(validateHostName("cc.cmu.edu"))
        self.assertTrue(validateHostName("a_b.cmu.edu")) # allow underscore
        self.assertTrue(validateHostName("a-b.cmu.edu")) # allow hyphen
        self.assertFalse(validateHostName("cc.cmu .edu")) # spaces not allowed
        self.assertFalse(validateHostName("cc.cmu.edu*")) # invalid char

    def testValidateInteger(self):
        self.assertTrue(validateInteger("0"))
        self.assertTrue(validateInteger("12"))
        self.assertTrue(validateInteger("123"))
        self.assertFalse(validateInteger("023"))
        self.assertFalse(validateInteger("0a3"))

    def testValidateIPv4(self):
        self.assertTrue(validateIPv4("192.168.1.1"))
        self.assertTrue(validateIPv4("255.255.255.255"))
        self.assertTrue(validateIPv4("255.0.0.0"))
        self.assertFalse(validateIPv4("255.256.255.255"))
        self.assertFalse(validateIPv4("abc.255.255.255"))

if __name__ == "__main__":
    unittest.main()
