'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_MESA_ycbcr_texture'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_MESA_ycbcr_texture',error_checker=_errors._error_checker)
GL_UNSIGNED_SHORT_8_8_MESA=_C('GL_UNSIGNED_SHORT_8_8_MESA',0x85BA)
GL_UNSIGNED_SHORT_8_8_REV_MESA=_C('GL_UNSIGNED_SHORT_8_8_REV_MESA',0x85BB)
GL_YCBCR_MESA=_C('GL_YCBCR_MESA',0x8757)

