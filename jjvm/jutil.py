import struct

def readU2(clazz):
  return struct.unpack(">H", clazz.read(2))[0]
