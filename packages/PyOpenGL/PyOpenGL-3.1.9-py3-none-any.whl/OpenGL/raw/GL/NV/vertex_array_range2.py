'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_NV_vertex_array_range2'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_NV_vertex_array_range2',error_checker=_errors._error_checker)
GL_VERTEX_ARRAY_RANGE_WITHOUT_FLUSH_NV=_C('GL_VERTEX_ARRAY_RANGE_WITHOUT_FLUSH_NV',0x8533)

