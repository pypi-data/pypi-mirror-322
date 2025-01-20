'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_NV_gpu_program4'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_NV_gpu_program4',error_checker=_errors._error_checker)
GL_MAX_PROGRAM_ATTRIB_COMPONENTS_NV=_C('GL_MAX_PROGRAM_ATTRIB_COMPONENTS_NV',0x8908)
GL_MAX_PROGRAM_GENERIC_ATTRIBS_NV=_C('GL_MAX_PROGRAM_GENERIC_ATTRIBS_NV',0x8DA5)
GL_MAX_PROGRAM_GENERIC_RESULTS_NV=_C('GL_MAX_PROGRAM_GENERIC_RESULTS_NV',0x8DA6)
GL_MAX_PROGRAM_RESULT_COMPONENTS_NV=_C('GL_MAX_PROGRAM_RESULT_COMPONENTS_NV',0x8909)
GL_MAX_PROGRAM_TEXEL_OFFSET_NV=_C('GL_MAX_PROGRAM_TEXEL_OFFSET_NV',0x8905)
GL_MIN_PROGRAM_TEXEL_OFFSET_NV=_C('GL_MIN_PROGRAM_TEXEL_OFFSET_NV',0x8904)
GL_PROGRAM_ATTRIB_COMPONENTS_NV=_C('GL_PROGRAM_ATTRIB_COMPONENTS_NV',0x8906)
GL_PROGRAM_RESULT_COMPONENTS_NV=_C('GL_PROGRAM_RESULT_COMPONENTS_NV',0x8907)
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLintArray)
def glGetProgramEnvParameterIivNV(target,index,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLuintArray)
def glGetProgramEnvParameterIuivNV(target,index,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLintArray)
def glGetProgramLocalParameterIivNV(target,index,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLuintArray)
def glGetProgramLocalParameterIuivNV(target,index,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint)
def glProgramEnvParameterI4iNV(target,index,x,y,z,w):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLintArray)
def glProgramEnvParameterI4ivNV(target,index,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,_cs.GLuint,_cs.GLuint,_cs.GLuint,_cs.GLuint)
def glProgramEnvParameterI4uiNV(target,index,x,y,z,w):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLuintArray)
def glProgramEnvParameterI4uivNV(target,index,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,_cs.GLsizei,arrays.GLintArray)
def glProgramEnvParametersI4ivNV(target,index,count,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,_cs.GLsizei,arrays.GLuintArray)
def glProgramEnvParametersI4uivNV(target,index,count,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint)
def glProgramLocalParameterI4iNV(target,index,x,y,z,w):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLintArray)
def glProgramLocalParameterI4ivNV(target,index,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,_cs.GLuint,_cs.GLuint,_cs.GLuint,_cs.GLuint)
def glProgramLocalParameterI4uiNV(target,index,x,y,z,w):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLuintArray)
def glProgramLocalParameterI4uivNV(target,index,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,_cs.GLsizei,arrays.GLintArray)
def glProgramLocalParametersI4ivNV(target,index,count,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,_cs.GLsizei,arrays.GLuintArray)
def glProgramLocalParametersI4uivNV(target,index,count,params):pass
