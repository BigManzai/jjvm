#!/usr/bin/python

import argparse
import os
import struct
import sys

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
def readToNextCpStruct(clazz):
  tag = ord(clazz.read(1))

  print "Tag %d" % (tag)

  remainingSeek = 0

  if tag == 1:
    # FIXME: Yes, this will blow badly on encountering anything other than ASCII
    # https://docs.oracle.com/javase/specs/jvms/se7/html/jvms-4.html
    remainingSeek = struct.unpack(">H", clazz.read(2))[0]
  elif tag == 7:
    remainingSeek = 2
  elif tag == 10:
    remainingSeek = 4
  elif tag == 12:
    remainingSeek = 4
  else:
    print "ERROR: Unrecognized tag %d" % tag
    sys.exit(1)
  
  print "Remaining seek %d" % remainingSeek

  clazz.seek(remainingSeek, os.SEEK_CUR)

############
### MAIN ###
############
parser = MyParser('Run bytecode in jjvm')
parser.add_argument('path', help='path to class')
args = parser.parse_args()

with open(args.path, "rb") as clazz:
  clazz.seek(8)
  cpCount = struct.unpack(">H", clazz.read(2))[0] - 1
  cpIndex = 1

  print "Constant pool count: %d" % cpCount;

  while cpIndex <= cpCount:
    print "Reading field %d" % cpIndex
    readToNextCpStruct(clazz)
    cpIndex += 1

  print "Pos: %x" % clazz.tell()
