#!/usr/bin/env python

import re
import sys

IGNORE_PREFIX="#@Z:'&"

def isCorrectHostName(name):
    if name.find(' ') != -1: # name contains spaces
        return False
    for part in name.split('.'): # split the parts of the server name
        if not re.match("^[a-zA-Z0-9_\-]*$", part):
            return False
    return True

def isCorrectInteger(s):
    return re.match("^(0|[1-9][0-9]*)$", s) != None

def isCorrectIPv4(addr):
    parts = addr.split('.')
    if len(parts) != 4: # ipv4 contains 4 numbers
        return False
    for part in parts:
        if not isCorrectInteger(part): # check if it's a number
            return False
        if int(part) > 255: # check if the number is within 0~255
            return False
    return True

def validateRecordPlus(fields):
    if len(fields) < 2: # check if the record contains at least 2 fields
        return (False, "+ records must have at least 2 fields")
    if not isCorrectHostName(fields[0]):
        return (False, "incorrect hostname: \"%s\"" % (fields[0]))
    if not isCorrectIPv4(fields[1]):
        return (False, "incorrect ipv4 address: \"%s\"" % (fields[1]))
    if len(fields) >= 3 and not isCorrectInteger(fields[2]):
        return (False, "should be an integer: %s" % (fields[2]))
    return (True,"")

def validateRecordC(fields):
    if len(fields) < 2: # check if the record contains at least 2 fields
        return (False, "+ records must have at least 2 fields")
    if not isCorrectHostName(fields[0]):
        return (False, "incorrect hostname: \"%s\"" % (fields[0]))
    if not isCorrectHostName(fields[1]):
        return (False, "incorrect ipv4 address: \"%s\"" % (fields[1]))
    if len(fields) >= 3 and not isCorrectInteger(fields[2]):
        return (False, "should be an integer: %s" % (fields[2]))
    return (True,"")

def stripComments(line):
    hashIndex = line.find('#')
    if hashIndex >= 0:
        return line[:hashIndex]
    else:
        return line

def validateLine(line):
    line = stripComments(line).strip()
    if len(line) == 0: # empty or comment line
        return (True,"")

    # select validate function based on its prefix
    prefix = line[0]
    if prefix in IGNORE_PREFIX:
        return (True,"")
    fields = line[1:].split(':')
    if prefix == '+':
        return validateRecordPlus(fields)
    elif prefix == 'C':
        return validateRecordC(fields)
    else:
        return (False, "unknown prefix: \"%s\"" % (prefix))

def reportError(lineno, errmsg):
    print "error: line %d: %s" % (lineno, errmsg)

def validateFile(fin):
    lineno = 0
    for line in fin:
        lineno += 1
        line = line.strip()
        (success, errmsg) = validateLine(line)
        if not success:
            reportError(lineno, errmsg)
    if line != "": # last line must be a newline
        reportError(lineno, "file must end with a newline")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            validateFile(f)
    else:
        validateFile(sys.stdin)
