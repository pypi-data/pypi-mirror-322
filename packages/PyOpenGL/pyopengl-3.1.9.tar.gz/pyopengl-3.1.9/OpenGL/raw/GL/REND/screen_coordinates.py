'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_REND_screen_coordinates'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_REND_screen_coordinates',error_checker=_errors._error_checker)
GL_INVERTED_SCREEN_W_REND=_C('GL_INVERTED_SCREEN_W_REND',0x8491)
GL_SCREEN_COORDINATES_REND=_C('GL_SCREEN_COORDINATES_REND',0x8490)

