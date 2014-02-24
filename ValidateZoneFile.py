#!/usr/bin/env python

import re

def validateHostName(name):
    if name.find(' ') != -1: # name contains spaces
        return False
    for part in name.split('.'): # split the parts of the server name
        if not re.match("^[a-zA-Z0-9_\-]+$", part):
            return False
    return True

def validateInteger(s):
    return re.match("^(0|[1-9][0-9]*)$", s) != None

def validateIPv4(addr):
    parts = addr.split('.')
    if len(parts) != 4: # ipv4 contains 4 numbers
        return False
    for part in parts:
        if not validateInteger(part): # check if it's a number
            return False
        if int(part) > 255: # check if the number is within 0~255
            return False
    return True
