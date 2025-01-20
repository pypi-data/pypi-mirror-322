'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLES2 import _types as _cs
# End users want this...
from OpenGL.raw.GLES2._types import *
from OpenGL.raw.GLES2 import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLES2_EXT_map_buffer_range'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLES2,'GLES2_EXT_map_buffer_range',error_checker=_errors._error_checker)
GL_MAP_FLUSH_EXPLICIT_BIT_EXT=_C('GL_MAP_FLUSH_EXPLICIT_BIT_EXT',0x0010)
GL_MAP_INVALIDATE_BUFFER_BIT_EXT=_C('GL_MAP_INVALIDATE_BUFFER_BIT_EXT',0x0008)
GL_MAP_INVALIDATE_RANGE_BIT_EXT=_C('GL_MAP_INVALIDATE_RANGE_BIT_EXT',0x0004)
GL_MAP_READ_BIT_EXT=_C('GL_MAP_READ_BIT_EXT',0x0001)
GL_MAP_UNSYNCHRONIZED_BIT_EXT=_C('GL_MAP_UNSYNCHRONIZED_BIT_EXT',0x0020)
GL_MAP_WRITE_BIT_EXT=_C('GL_MAP_WRITE_BIT_EXT',0x0002)
@_f
@_p.types(None,_cs.GLenum,_cs.GLintptr,_cs.GLsizeiptr)
def glFlushMappedBufferRangeEXT(target,offset,length):pass
@_f
@_p.types(ctypes.c_void_p,_cs.GLenum,_cs.GLintptr,_cs.GLsizeiptr,_cs.GLbitfield)
def glMapBufferRangeEXT(target,offset,length,access):pass
