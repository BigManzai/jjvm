#!/usr/bin/python

import argparse
from jjvm.jclass import jclass
from jjvm.jutil import readU2
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

############
### MAIN ###
############
parser = MyParser('Run bytecode in jjvm')
parser.add_argument('path', help='path to class')
args = parser.parse_args()

with open(args.path, "rb") as clazz:
  clazz.seek(8)
  cpCount = readU2(clazz) - 1
  cpIndex = 1

  print "Constant pool count: %d" % cpCount;

  while cpIndex <= cpCount:
    # print "Reading field %d" % cpIndex
    print "%d %s" % (cpIndex, jclass.readToNextCpStruct(clazz))
    cpIndex += 1

  # Skip access flags, tjhis class, super class refs
  clazz.seek(6, os.SEEK_CUR)

  # TODO: Yes, need to deal with when these aren't actually 0!
  print "\nInterfaces count: %d" % readU2(clazz)
  print "Fields count: %d" % readU2(clazz)

  methodsCount = readU2(clazz)
  print "Methods count: %d" % methodsCount

  readU2(clazz)
  methodNameIndex = readU2(clazz)

  print "First method name index: %d" % methodNameIndex

  print "Pos: %x" % clazz.tell()
