'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_EXT_blend_equation_separate'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_EXT_blend_equation_separate',error_checker=_errors._error_checker)
GL_BLEND_EQUATION_ALPHA_EXT=_C('GL_BLEND_EQUATION_ALPHA_EXT',0x883D)
GL_BLEND_EQUATION_RGB_EXT=_C('GL_BLEND_EQUATION_RGB_EXT',0x8009)
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum)
def glBlendEquationSeparateEXT(modeRGB,modeAlpha):pass
