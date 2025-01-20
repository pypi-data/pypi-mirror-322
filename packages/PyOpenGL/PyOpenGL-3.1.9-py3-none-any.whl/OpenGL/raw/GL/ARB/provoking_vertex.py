'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ARB_provoking_vertex'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ARB_provoking_vertex',error_checker=_errors._error_checker)
GL_FIRST_VERTEX_CONVENTION=_C('GL_FIRST_VERTEX_CONVENTION',0x8E4D)
GL_LAST_VERTEX_CONVENTION=_C('GL_LAST_VERTEX_CONVENTION',0x8E4E)
GL_PROVOKING_VERTEX=_C('GL_PROVOKING_VERTEX',0x8E4F)
GL_QUADS_FOLLOW_PROVOKING_VERTEX_CONVENTION=_C('GL_QUADS_FOLLOW_PROVOKING_VERTEX_CONVENTION',0x8E4C)
@_f
@_p.types(None,_cs.GLenum)
def glProvokingVertex(mode):pass
