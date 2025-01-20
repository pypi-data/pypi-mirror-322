'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_AMD_draw_buffers_blend'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_AMD_draw_buffers_blend',error_checker=_errors._error_checker)

@_f
@_p.types(None,_cs.GLuint,_cs.GLenum)
def glBlendEquationIndexedAMD(buf,mode):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,_cs.GLenum)
def glBlendEquationSeparateIndexedAMD(buf,modeRGB,modeAlpha):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,_cs.GLenum)
def glBlendFuncIndexedAMD(buf,src,dst):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,_cs.GLenum,_cs.GLenum,_cs.GLenum)
def glBlendFuncSeparateIndexedAMD(buf,srcRGB,dstRGB,srcAlpha,dstAlpha):pass
