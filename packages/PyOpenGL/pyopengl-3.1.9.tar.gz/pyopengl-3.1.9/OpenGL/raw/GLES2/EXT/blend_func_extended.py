'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLES2 import _types as _cs
# End users want this...
from OpenGL.raw.GLES2._types import *
from OpenGL.raw.GLES2 import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLES2_EXT_blend_func_extended'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLES2,'GLES2_EXT_blend_func_extended',error_checker=_errors._error_checker)
GL_LOCATION_INDEX_EXT=_C('GL_LOCATION_INDEX_EXT',0x930F)
GL_MAX_DUAL_SOURCE_DRAW_BUFFERS_EXT=_C('GL_MAX_DUAL_SOURCE_DRAW_BUFFERS_EXT',0x88FC)
GL_ONE_MINUS_SRC1_ALPHA_EXT=_C('GL_ONE_MINUS_SRC1_ALPHA_EXT',0x88FB)
GL_ONE_MINUS_SRC1_COLOR_EXT=_C('GL_ONE_MINUS_SRC1_COLOR_EXT',0x88FA)
GL_SRC1_ALPHA_EXT=_C('GL_SRC1_ALPHA_EXT',0x8589)
GL_SRC1_COLOR_EXT=_C('GL_SRC1_COLOR_EXT',0x88F9)
GL_SRC_ALPHA_SATURATE_EXT=_C('GL_SRC_ALPHA_SATURATE_EXT',0x0308)
@_f
@_p.types(None,_cs.GLuint,_cs.GLuint,arrays.GLcharArray)
def glBindFragDataLocationEXT(program,color,name):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLuint,_cs.GLuint,arrays.GLcharArray)
def glBindFragDataLocationIndexedEXT(program,colorNumber,index,name):pass
@_f
@_p.types(_cs.GLint,_cs.GLuint,arrays.GLcharArray)
def glGetFragDataIndexEXT(program,name):pass
@_f
@_p.types(_cs.GLint,_cs.GLuint,_cs.GLenum,arrays.GLcharArray)
def glGetProgramResourceLocationIndexEXT(program,programInterface,name):pass
