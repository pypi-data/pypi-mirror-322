'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLES2 import _types as _cs
# End users want this...
from OpenGL.raw.GLES2._types import *
from OpenGL.raw.GLES2 import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLES2_OES_compressed_paletted_texture'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLES2,'GLES2_OES_compressed_paletted_texture',error_checker=_errors._error_checker)
GL_PALETTE4_R5_G6_B5_OES=_C('GL_PALETTE4_R5_G6_B5_OES',0x8B92)
GL_PALETTE4_RGB5_A1_OES=_C('GL_PALETTE4_RGB5_A1_OES',0x8B94)
GL_PALETTE4_RGB8_OES=_C('GL_PALETTE4_RGB8_OES',0x8B90)
GL_PALETTE4_RGBA4_OES=_C('GL_PALETTE4_RGBA4_OES',0x8B93)
GL_PALETTE4_RGBA8_OES=_C('GL_PALETTE4_RGBA8_OES',0x8B91)
GL_PALETTE8_R5_G6_B5_OES=_C('GL_PALETTE8_R5_G6_B5_OES',0x8B97)
GL_PALETTE8_RGB5_A1_OES=_C('GL_PALETTE8_RGB5_A1_OES',0x8B99)
GL_PALETTE8_RGB8_OES=_C('GL_PALETTE8_RGB8_OES',0x8B95)
GL_PALETTE8_RGBA4_OES=_C('GL_PALETTE8_RGBA4_OES',0x8B98)
GL_PALETTE8_RGBA8_OES=_C('GL_PALETTE8_RGBA8_OES',0x8B96)

