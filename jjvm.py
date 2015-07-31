#!/usr/bin/python

import argparse
import sys

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser('Run bytecode in jjvm')
parser.add_argument('path', help='path to class')
args = parser.parse_args()

with open(args.path, "rb") as c:
  byte = c.read(1)
  while byte:
    print '{0:02x}'.format(ord(byte))
    byte = c.read(1)
