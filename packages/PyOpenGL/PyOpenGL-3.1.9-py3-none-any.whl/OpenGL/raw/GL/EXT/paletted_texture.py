'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_EXT_paletted_texture'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_EXT_paletted_texture',error_checker=_errors._error_checker)
GL_COLOR_INDEX12_EXT=_C('GL_COLOR_INDEX12_EXT',0x80E6)
GL_COLOR_INDEX16_EXT=_C('GL_COLOR_INDEX16_EXT',0x80E7)
GL_COLOR_INDEX1_EXT=_C('GL_COLOR_INDEX1_EXT',0x80E2)
GL_COLOR_INDEX2_EXT=_C('GL_COLOR_INDEX2_EXT',0x80E3)
GL_COLOR_INDEX4_EXT=_C('GL_COLOR_INDEX4_EXT',0x80E4)
GL_COLOR_INDEX8_EXT=_C('GL_COLOR_INDEX8_EXT',0x80E5)
GL_TEXTURE_INDEX_SIZE_EXT=_C('GL_TEXTURE_INDEX_SIZE_EXT',0x80ED)
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,_cs.GLsizei,_cs.GLenum,_cs.GLenum,ctypes.c_void_p)
def glColorTableEXT(target,internalFormat,width,format,type,table):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,_cs.GLenum,ctypes.c_void_p)
def glGetColorTableEXT(target,format,type,data):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,arrays.GLfloatArray)
def glGetColorTableParameterfvEXT(target,pname,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,arrays.GLintArray)
def glGetColorTableParameterivEXT(target,pname,params):pass
