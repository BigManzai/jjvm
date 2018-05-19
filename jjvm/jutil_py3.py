import struct

def readU2(f):
  return struct.unpack(">H", f.read(2))[0]

def readU4(f):
  return struct.unpack(">L", f.read(4))[0]