#!/usr/bin/python

import argparse
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

############
### MAIN ###
############
parser = MyParser('Run bytecode in jjvm')
parser.add_argument('path', help='path to class')
args = parser.parse_args()

with open(args.path, "rb") as c:
  c.seek(8)
  cpcount = struct.unpack(">H", c.read(2))[0] - 1

  print "Constant pool count: %d" % cpcount;

  cptag = ord(c.read(1))

  print "Got tag: %d" % cptag
