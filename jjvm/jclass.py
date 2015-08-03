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

OPCODE_NAMES = {
  0x12:"ldc",
  0x2a:"aload_0",
  0xb1:"return",
  0xb2:"getstatic",
  0xb6:"invokevirtual",
  0xb7:"invokespecial"
}

class jclass:
  # Indexed by field
  _utf8Strings = {}

  # FIXME: indexed by simple name
  _methods = {}

  def getMethod(self, name):
    if name in self._methods:
      return self._methods[name]
    else:
      return None

  def getMethods(self):
    return self._methods

  def __init__(self, path):
    with open(path, "rb") as f:
      f.seek(8)

      self._readCp(f)

      # Skip access flags, tjhis class, super class refs
      f.seek(6, os.SEEK_CUR)

      # TODO: Yes, need to deal with when these aren't actually 0!
      print "\nInterfaces count: %d" % readU2(f)
      print "Fields count: %d" % readU2(f)

      methodsCount = readU2(f)
      print "Methods count: %d\n" % methodsCount

      for i in range(methodsCount):
        m = jmethod(self, f)
        self._methods[m.getName()] = m

  def _readCp(self, f):
      cpCount = readU2(f) - 1
      cpIndex = 1

      print "Constant pool count: %d" % cpCount;

      while cpIndex <= cpCount:
        # print "Reading field %d" % cpIndex
        print "%d %s" % (cpIndex, self._readToNextCpStruct(f, cpIndex))
        cpIndex += 1

  def _readToNextCpStruct(self, f, index):
    tag = ord(f.read(1))

    # print "Tag %d %s" % (tag, TAG_NAMES[tag])
    res = TAG_NAMES[tag]

    remainingSeek = 0

    if tag == 1:
      # FIXME: Yes, this will blow badly on encountering anything other than ASCII
      # https://docs.oracle.com/javase/specs/jvms/se7/html/jvms-4.html
      strLen = readU2(f)
      res += " "
      utf8 = f.read(strLen)
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
      f.seek(remainingSeek, os.SEEK_CUR)

    return res

class jmethod:
  _clazz = None
  _nameIndex = -1
  _descriptorIndex = -1
  _code = None

  def __init__(self, clazz, f):
      self._clazz = clazz

      # access_flags
      readU2(f)
      self._nameIndex = readU2(f)
      self._descriptorIndex = readU2(f)
      self._readMethodAttributes(f)

      # print "\nPos: %x" % f.tell()

  def getName(self):
    return self._clazz._utf8Strings[self._nameIndex]
  
  def getDescriptor(self):
    return self._clazz._utf8Strings[self._descriptorIndex]

  def printCode(self):
    i = 0
    while i < len(self._code):
      opcode = self._code[i]
      name = ""

      if opcode in OPCODE_NAMES:
        name = OPCODE_NAMES[opcode]

      print "%d: %.2x %s" % (i, opcode, name)

      # XXX: Temporary, temporary hack to handle invokespecial
      if opcode == 0x12:
        i += 1
      elif opcode == 0xb2:
        i += 2
      elif opcode == 0xb6:
        i += 2
      elif opcode == 0xb7:
        i += 2

      i += 1

  def _readMethodAttributes(self, f):
      """Read the method attributes section"""
      attributesCount = readU2(f)
      # print "Attributes: %d" % attributesCount

      attributesIndex = 1
      while attributesIndex <= attributesCount:
        self._readMethodAttribute(f, attributesIndex)
        attributesIndex += 1

  def _readMethodAttribute(self, f, index):
      """Read the top level details of a method attribute"""
      attrNameIndex = readU2(f)
      attrName = self._clazz._utf8Strings[attrNameIndex]
      # print "Name: %s" % attrName

      if "Code" == attrName:
        self._readMethodCodeAttribute(f)
      else:
        attrLen = readU4(f)
        f.read(attrLen)

  def _readMethodCodeAttribute(self, f):
      """Read a method code attribute"""

      attrLen = readU4(f)
      # print "Length: %d" % attrLen
  
      # max stack
      readU2(f)
      # max locals
      readU2(f)

      codeLen = readU4(f)
      # print "Code length: %d" % codeLen
      
      self._code = []

      codeCount = 1
      while codeCount <= codeLen:
        self._code.append(ord(f.read(1)))
        codeCount += 1

      f.read(attrLen - codeLen - 8)
