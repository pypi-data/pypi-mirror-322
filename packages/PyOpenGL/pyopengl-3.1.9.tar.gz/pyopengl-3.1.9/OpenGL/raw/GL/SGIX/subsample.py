'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_SGIX_subsample'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_SGIX_subsample',error_checker=_errors._error_checker)
GL_PACK_SUBSAMPLE_RATE_SGIX=_C('GL_PACK_SUBSAMPLE_RATE_SGIX',0x85A0)
GL_PIXEL_SUBSAMPLE_2424_SGIX=_C('GL_PIXEL_SUBSAMPLE_2424_SGIX',0x85A3)
GL_PIXEL_SUBSAMPLE_4242_SGIX=_C('GL_PIXEL_SUBSAMPLE_4242_SGIX',0x85A4)
GL_PIXEL_SUBSAMPLE_4444_SGIX=_C('GL_PIXEL_SUBSAMPLE_4444_SGIX',0x85A2)
GL_UNPACK_SUBSAMPLE_RATE_SGIX=_C('GL_UNPACK_SUBSAMPLE_RATE_SGIX',0x85A1)

