from jutil import readU2, readU4
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
  # Indexed by field
  _utf8Strings = {}

  def __init__(self, path):
    with open(path, "rb") as clazz:
      clazz.seek(8)

      self._readCp(clazz)

      # Skip access flags, tjhis class, super class refs
      clazz.seek(6, os.SEEK_CUR)

      # TODO: Yes, need to deal with when these aren't actually 0!
      print "\nInterfaces count: %d" % readU2(clazz)
      print "Fields count: %d" % readU2(clazz)

      methodsCount = readU2(clazz)
      print "Methods count: %d\n" % methodsCount

      # access_flags
      readU2(clazz)
      methodNameIndex = readU2(clazz)

      # print "First method name index: %d" % methodNameIndex
      print "Method name: %s" % self._utf8Strings[methodNameIndex]

      descriptorIndex = readU2(clazz)
      print "Descriptor: %s" % self._utf8Strings[descriptorIndex]

      self._readMethodAttributes(clazz)

      print "\nPos: %x" % clazz.tell()

  def _readMethodAttributes(self, clazz):
      """Read the method attributes section"""
      attributesCount = readU2(clazz)
      print "Attributes: %d" % attributesCount

      attributesIndex = 1
      while attributesIndex <= attributesCount:
        self._readMethodAttribute(clazz, attributesIndex)
        attributesIndex += 1

  def _readMethodAttribute(self, clazz, index):
      """Read the top level details of a method attribute"""
      attrNameIndex = readU2(clazz)
      attrName = self._utf8Strings[attrNameIndex]
      print "Name: %s" % attrName

      if "Code" == attrName:
        self._readMethodCodeAttribute(clazz)
      else:
        clazz.read(attrLen)

  def _readMethodCodeAttribute(self, clazz):
      """Read a method code attribute"""

      attrLen = readU4(clazz)
      print "Length: %d" % attrLen
  
      # max stack
      readU2(clazz)
      # max locals
      readU2(clazz)

      codeLen = readU4(clazz)
      print "Code length: %d" % codeLen

      codeCount = 1
      while codeCount <= codeLen:
        print "%d: %.2x" % (codeCount, ord(clazz.read(1)))
        codeCount += 1

      clazz.read(attrLen - 8)

  def _readCp(self, clazz):
      cpCount = readU2(clazz) - 1
      cpIndex = 1

      print "Constant pool count: %d" % cpCount;

      while cpIndex <= cpCount:
        # print "Reading field %d" % cpIndex
        print "%d %s" % (cpIndex, self._readToNextCpStruct(clazz, cpIndex))
        cpIndex += 1

  def _readToNextCpStruct(self, clazz, index):
    tag = ord(clazz.read(1))

    # print "Tag %d %s" % (tag, TAG_NAMES[tag])
    res = TAG_NAMES[tag]

    remainingSeek = 0

    if tag == 1:
      # FIXME: Yes, this will blow badly on encountering anything other than ASCII
      # https://docs.oracle.com/javase/specs/jvms/se7/html/jvms-4.html
      strLen = readU2(clazz)
      res += " "
      utf8 = clazz.read(strLen)
      self._utf8Strings[index] = utf8
      res += utf8
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
