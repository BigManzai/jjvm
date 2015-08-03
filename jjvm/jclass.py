from jutil import readU2
import os
import sys

TAG_NAMES = { 
  1:"Utf8",
  3:"Integer",
  4:"Float",
  5:"Long",
  6:"Double",
  7:"Class", 
  8:"String",
  9:"Fieldref", 
  10:"Methodref", 
  11:"InterfaceMethodref",
  12:"NameAndType",
  15:"MethodHandle",
  16:"MethodType",
  18:"InvokeDynamic"
}

class jclass:
  @staticmethod
  def readToNextCpStruct(clazz):
    tag = ord(clazz.read(1))

    # print "Tag %d %s" % (tag, TAG_NAMES[tag])
    res = TAG_NAMES[tag]

    remainingSeek = 0

    if tag == 1:
      # FIXME: Yes, this will blow badly on encountering anything other than ASCII
      # https://docs.oracle.com/javase/specs/jvms/se7/html/jvms-4.html
      strLen = readU2(clazz)
      res += " "
      res += clazz.read(strLen)
      # print struct.unpack("s", clazz.read(strLen))[0]
      # remainingSeek = readU2(clazz)
    elif tag == 7:
      remainingSeek = 2
    elif tag == 8:
      remainingSeek = 2
    elif tag == 9:
      remainingSeek = 4
    elif tag == 10:
      remainingSeek = 4
    elif tag == 12:
      remainingSeek = 4
    else:
      print "ERROR: Unrecognized tag %d" % tag
      sys.exit(1)
    
    # print "Remaining seek %d" % remainingSeek

    if remainingSeek > 0:
      clazz.seek(remainingSeek, os.SEEK_CUR)

    return res
