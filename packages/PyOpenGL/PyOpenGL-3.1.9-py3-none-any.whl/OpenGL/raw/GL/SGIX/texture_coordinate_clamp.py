'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_SGIX_texture_coordinate_clamp'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_SGIX_texture_coordinate_clamp',error_checker=_errors._error_checker)
GL_TEXTURE_MAX_CLAMP_R_SGIX=_C('GL_TEXTURE_MAX_CLAMP_R_SGIX',0x836B)
GL_TEXTURE_MAX_CLAMP_S_SGIX=_C('GL_TEXTURE_MAX_CLAMP_S_SGIX',0x8369)
GL_TEXTURE_MAX_CLAMP_T_SGIX=_C('GL_TEXTURE_MAX_CLAMP_T_SGIX',0x836A)

