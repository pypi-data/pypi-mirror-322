'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ARB_polygon_offset_clamp'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ARB_polygon_offset_clamp',error_checker=_errors._error_checker)
GL_POLYGON_OFFSET_CLAMP=_C('GL_POLYGON_OFFSET_CLAMP',0x8E1B)
@_f
@_p.types(None,_cs.GLfloat,_cs.GLfloat,_cs.GLfloat)
def glPolygonOffsetClamp(factor,units,clamp):pass
