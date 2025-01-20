'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLES1 import _types as _cs
# End users want this...
from OpenGL.raw.GLES1._types import *
from OpenGL.raw.GLES1 import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLES1_EXT_texture_lod_bias'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLES1,'GLES1_EXT_texture_lod_bias',error_checker=_errors._error_checker)
GL_MAX_TEXTURE_LOD_BIAS_EXT=_C('GL_MAX_TEXTURE_LOD_BIAS_EXT',0x84FD)
GL_TEXTURE_FILTER_CONTROL_EXT=_C('GL_TEXTURE_FILTER_CONTROL_EXT',0x8500)
GL_TEXTURE_LOD_BIAS_EXT=_C('GL_TEXTURE_LOD_BIAS_EXT',0x8501)

