'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_EXT_texture_sRGB_decode'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_EXT_texture_sRGB_decode',error_checker=_errors._error_checker)
GL_DECODE_EXT=_C('GL_DECODE_EXT',0x8A49)
GL_SKIP_DECODE_EXT=_C('GL_SKIP_DECODE_EXT',0x8A4A)
GL_TEXTURE_SRGB_DECODE_EXT=_C('GL_TEXTURE_SRGB_DECODE_EXT',0x8A48)

