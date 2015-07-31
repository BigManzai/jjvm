#!/usr/bin/python

import argparse
import os
import struct
import sys

CP_STRUCT_SIZES = { 7:3, 10:5 }

###############
### CLASSES ###
###############
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

###################
### SUBROUTINES ###
###################
def lenCpStruct(tag):
  if tag in CP_STRUCT_SIZES:
    return CP_STRUCT_SIZES[tag]
  else:
    return -1

############
### MAIN ###
############
parser = MyParser('Run bytecode in jjvm')
parser.add_argument('path', help='path to class')
args = parser.parse_args()

with open(args.path, "rb") as c:
  c.seek(8)
  cpCount = struct.unpack(">H", c.read(2))[0] - 1

  print "Constant pool count: %d" % cpCount;

  while cpCount >= 0:
    cpTag = ord(c.read(1))

    print "Got tag: %d" % cpTag
    cpStructSize = lenCpStruct(cpTag)

    if cpStructSize < 0:
      print "ERROR: cpStructSize %d for tag %d" % (cpStructSize, cpTag)
      sys.exit(1)

    print "Size: %d" % cpStructSize
  
    cpCount -= 1
    c.seek(cpStructSize - 1, os.SEEK_CUR)
