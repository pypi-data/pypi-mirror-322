'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ARB_texture_compression_bptc'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ARB_texture_compression_bptc',error_checker=_errors._error_checker)
GL_COMPRESSED_RGBA_BPTC_UNORM_ARB=_C('GL_COMPRESSED_RGBA_BPTC_UNORM_ARB',0x8E8C)
GL_COMPRESSED_RGB_BPTC_SIGNED_FLOAT_ARB=_C('GL_COMPRESSED_RGB_BPTC_SIGNED_FLOAT_ARB',0x8E8E)
GL_COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT_ARB=_C('GL_COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT_ARB',0x8E8F)
GL_COMPRESSED_SRGB_ALPHA_BPTC_UNORM_ARB=_C('GL_COMPRESSED_SRGB_ALPHA_BPTC_UNORM_ARB',0x8E8D)

