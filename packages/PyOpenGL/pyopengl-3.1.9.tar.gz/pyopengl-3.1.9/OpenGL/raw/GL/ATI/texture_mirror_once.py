'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ATI_texture_mirror_once'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ATI_texture_mirror_once',error_checker=_errors._error_checker)
GL_MIRROR_CLAMP_ATI=_C('GL_MIRROR_CLAMP_ATI',0x8742)
GL_MIRROR_CLAMP_TO_EDGE_ATI=_C('GL_MIRROR_CLAMP_TO_EDGE_ATI',0x8743)

