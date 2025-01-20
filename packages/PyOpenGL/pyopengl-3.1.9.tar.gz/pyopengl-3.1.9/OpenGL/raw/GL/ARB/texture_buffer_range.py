'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ARB_texture_buffer_range'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ARB_texture_buffer_range',error_checker=_errors._error_checker)
GL_TEXTURE_BUFFER_OFFSET=_C('GL_TEXTURE_BUFFER_OFFSET',0x919D)
GL_TEXTURE_BUFFER_OFFSET_ALIGNMENT=_C('GL_TEXTURE_BUFFER_OFFSET_ALIGNMENT',0x919F)
GL_TEXTURE_BUFFER_SIZE=_C('GL_TEXTURE_BUFFER_SIZE',0x919E)
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,_cs.GLuint,_cs.GLintptr,_cs.GLsizeiptr)
def glTexBufferRange(target,internalformat,buffer,offset,size):pass
