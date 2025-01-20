'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLES2 import _types as _cs
# End users want this...
from OpenGL.raw.GLES2._types import *
from OpenGL.raw.GLES2 import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLES2_IMG_texture_compression_pvrtc'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLES2,'GLES2_IMG_texture_compression_pvrtc',error_checker=_errors._error_checker)
GL_COMPRESSED_RGBA_PVRTC_2BPPV1_IMG=_C('GL_COMPRESSED_RGBA_PVRTC_2BPPV1_IMG',0x8C03)
GL_COMPRESSED_RGBA_PVRTC_4BPPV1_IMG=_C('GL_COMPRESSED_RGBA_PVRTC_4BPPV1_IMG',0x8C02)
GL_COMPRESSED_RGB_PVRTC_2BPPV1_IMG=_C('GL_COMPRESSED_RGB_PVRTC_2BPPV1_IMG',0x8C01)
GL_COMPRESSED_RGB_PVRTC_4BPPV1_IMG=_C('GL_COMPRESSED_RGB_PVRTC_4BPPV1_IMG',0x8C00)

