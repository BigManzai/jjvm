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

clazz = jclass(args.path)

for m in clazz.getMethods().values():
  print "Method name: %s" % m.getName()
  print "Descriptor: %s" % m.getDescriptor()
  m.printCode()
  print
