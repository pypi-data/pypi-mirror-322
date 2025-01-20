'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_EXT_geometry_shader4'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_EXT_geometry_shader4',error_checker=_errors._error_checker)
GL_FRAMEBUFFER_ATTACHMENT_LAYERED_EXT=_C('GL_FRAMEBUFFER_ATTACHMENT_LAYERED_EXT',0x8DA7)
GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LAYER_EXT=_C('GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LAYER_EXT',0x8CD4)
GL_FRAMEBUFFER_INCOMPLETE_LAYER_COUNT_EXT=_C('GL_FRAMEBUFFER_INCOMPLETE_LAYER_COUNT_EXT',0x8DA9)
GL_FRAMEBUFFER_INCOMPLETE_LAYER_TARGETS_EXT=_C('GL_FRAMEBUFFER_INCOMPLETE_LAYER_TARGETS_EXT',0x8DA8)
GL_GEOMETRY_INPUT_TYPE_EXT=_C('GL_GEOMETRY_INPUT_TYPE_EXT',0x8DDB)
GL_GEOMETRY_OUTPUT_TYPE_EXT=_C('GL_GEOMETRY_OUTPUT_TYPE_EXT',0x8DDC)
GL_GEOMETRY_SHADER_EXT=_C('GL_GEOMETRY_SHADER_EXT',0x8DD9)
GL_GEOMETRY_VERTICES_OUT_EXT=_C('GL_GEOMETRY_VERTICES_OUT_EXT',0x8DDA)
GL_LINES_ADJACENCY_EXT=_C('GL_LINES_ADJACENCY_EXT',0x000A)
GL_LINE_STRIP_ADJACENCY_EXT=_C('GL_LINE_STRIP_ADJACENCY_EXT',0x000B)
GL_MAX_GEOMETRY_OUTPUT_VERTICES_EXT=_C('GL_MAX_GEOMETRY_OUTPUT_VERTICES_EXT',0x8DE0)
GL_MAX_GEOMETRY_TEXTURE_IMAGE_UNITS_EXT=_C('GL_MAX_GEOMETRY_TEXTURE_IMAGE_UNITS_EXT',0x8C29)
GL_MAX_GEOMETRY_TOTAL_OUTPUT_COMPONENTS_EXT=_C('GL_MAX_GEOMETRY_TOTAL_OUTPUT_COMPONENTS_EXT',0x8DE1)
GL_MAX_GEOMETRY_UNIFORM_COMPONENTS_EXT=_C('GL_MAX_GEOMETRY_UNIFORM_COMPONENTS_EXT',0x8DDF)
GL_MAX_GEOMETRY_VARYING_COMPONENTS_EXT=_C('GL_MAX_GEOMETRY_VARYING_COMPONENTS_EXT',0x8DDD)
GL_MAX_VARYING_COMPONENTS_EXT=_C('GL_MAX_VARYING_COMPONENTS_EXT',0x8B4B)
GL_MAX_VERTEX_VARYING_COMPONENTS_EXT=_C('GL_MAX_VERTEX_VARYING_COMPONENTS_EXT',0x8DDE)
GL_PROGRAM_POINT_SIZE_EXT=_C('GL_PROGRAM_POINT_SIZE_EXT',0x8642)
GL_TRIANGLES_ADJACENCY_EXT=_C('GL_TRIANGLES_ADJACENCY_EXT',0x000C)
GL_TRIANGLE_STRIP_ADJACENCY_EXT=_C('GL_TRIANGLE_STRIP_ADJACENCY_EXT',0x000D)
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,_cs.GLint)
def glProgramParameteriEXT(program,pname,value):pass
