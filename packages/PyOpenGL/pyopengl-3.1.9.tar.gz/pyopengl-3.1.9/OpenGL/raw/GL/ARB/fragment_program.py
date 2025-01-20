'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ARB_fragment_program'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ARB_fragment_program',error_checker=_errors._error_checker)
GL_CURRENT_MATRIX_ARB=_C('GL_CURRENT_MATRIX_ARB',0x8641)
GL_CURRENT_MATRIX_STACK_DEPTH_ARB=_C('GL_CURRENT_MATRIX_STACK_DEPTH_ARB',0x8640)
GL_FRAGMENT_PROGRAM_ARB=_C('GL_FRAGMENT_PROGRAM_ARB',0x8804)
GL_MATRIX0_ARB=_C('GL_MATRIX0_ARB',0x88C0)
GL_MATRIX10_ARB=_C('GL_MATRIX10_ARB',0x88CA)
GL_MATRIX11_ARB=_C('GL_MATRIX11_ARB',0x88CB)
GL_MATRIX12_ARB=_C('GL_MATRIX12_ARB',0x88CC)
GL_MATRIX13_ARB=_C('GL_MATRIX13_ARB',0x88CD)
GL_MATRIX14_ARB=_C('GL_MATRIX14_ARB',0x88CE)
GL_MATRIX15_ARB=_C('GL_MATRIX15_ARB',0x88CF)
GL_MATRIX16_ARB=_C('GL_MATRIX16_ARB',0x88D0)
GL_MATRIX17_ARB=_C('GL_MATRIX17_ARB',0x88D1)
GL_MATRIX18_ARB=_C('GL_MATRIX18_ARB',0x88D2)
GL_MATRIX19_ARB=_C('GL_MATRIX19_ARB',0x88D3)
GL_MATRIX1_ARB=_C('GL_MATRIX1_ARB',0x88C1)
GL_MATRIX20_ARB=_C('GL_MATRIX20_ARB',0x88D4)
GL_MATRIX21_ARB=_C('GL_MATRIX21_ARB',0x88D5)
GL_MATRIX22_ARB=_C('GL_MATRIX22_ARB',0x88D6)
GL_MATRIX23_ARB=_C('GL_MATRIX23_ARB',0x88D7)
GL_MATRIX24_ARB=_C('GL_MATRIX24_ARB',0x88D8)
GL_MATRIX25_ARB=_C('GL_MATRIX25_ARB',0x88D9)
GL_MATRIX26_ARB=_C('GL_MATRIX26_ARB',0x88DA)
GL_MATRIX27_ARB=_C('GL_MATRIX27_ARB',0x88DB)
GL_MATRIX28_ARB=_C('GL_MATRIX28_ARB',0x88DC)
GL_MATRIX29_ARB=_C('GL_MATRIX29_ARB',0x88DD)
GL_MATRIX2_ARB=_C('GL_MATRIX2_ARB',0x88C2)
GL_MATRIX30_ARB=_C('GL_MATRIX30_ARB',0x88DE)
GL_MATRIX31_ARB=_C('GL_MATRIX31_ARB',0x88DF)
GL_MATRIX3_ARB=_C('GL_MATRIX3_ARB',0x88C3)
GL_MATRIX4_ARB=_C('GL_MATRIX4_ARB',0x88C4)
GL_MATRIX5_ARB=_C('GL_MATRIX5_ARB',0x88C5)
GL_MATRIX6_ARB=_C('GL_MATRIX6_ARB',0x88C6)
GL_MATRIX7_ARB=_C('GL_MATRIX7_ARB',0x88C7)
GL_MATRIX8_ARB=_C('GL_MATRIX8_ARB',0x88C8)
GL_MATRIX9_ARB=_C('GL_MATRIX9_ARB',0x88C9)
GL_MAX_PROGRAM_ALU_INSTRUCTIONS_ARB=_C('GL_MAX_PROGRAM_ALU_INSTRUCTIONS_ARB',0x880B)
GL_MAX_PROGRAM_ATTRIBS_ARB=_C('GL_MAX_PROGRAM_ATTRIBS_ARB',0x88AD)
GL_MAX_PROGRAM_ENV_PARAMETERS_ARB=_C('GL_MAX_PROGRAM_ENV_PARAMETERS_ARB',0x88B5)
GL_MAX_PROGRAM_INSTRUCTIONS_ARB=_C('GL_MAX_PROGRAM_INSTRUCTIONS_ARB',0x88A1)
GL_MAX_PROGRAM_LOCAL_PARAMETERS_ARB=_C('GL_MAX_PROGRAM_LOCAL_PARAMETERS_ARB',0x88B4)
GL_MAX_PROGRAM_MATRICES_ARB=_C('GL_MAX_PROGRAM_MATRICES_ARB',0x862F)
GL_MAX_PROGRAM_MATRIX_STACK_DEPTH_ARB=_C('GL_MAX_PROGRAM_MATRIX_STACK_DEPTH_ARB',0x862E)
GL_MAX_PROGRAM_NATIVE_ALU_INSTRUCTIONS_ARB=_C('GL_MAX_PROGRAM_NATIVE_ALU_INSTRUCTIONS_ARB',0x880E)
GL_MAX_PROGRAM_NATIVE_ATTRIBS_ARB=_C('GL_MAX_PROGRAM_NATIVE_ATTRIBS_ARB',0x88AF)
GL_MAX_PROGRAM_NATIVE_INSTRUCTIONS_ARB=_C('GL_MAX_PROGRAM_NATIVE_INSTRUCTIONS_ARB',0x88A3)
GL_MAX_PROGRAM_NATIVE_PARAMETERS_ARB=_C('GL_MAX_PROGRAM_NATIVE_PARAMETERS_ARB',0x88AB)
GL_MAX_PROGRAM_NATIVE_TEMPORARIES_ARB=_C('GL_MAX_PROGRAM_NATIVE_TEMPORARIES_ARB',0x88A7)
GL_MAX_PROGRAM_NATIVE_TEX_INDIRECTIONS_ARB=_C('GL_MAX_PROGRAM_NATIVE_TEX_INDIRECTIONS_ARB',0x8810)
GL_MAX_PROGRAM_NATIVE_TEX_INSTRUCTIONS_ARB=_C('GL_MAX_PROGRAM_NATIVE_TEX_INSTRUCTIONS_ARB',0x880F)
GL_MAX_PROGRAM_PARAMETERS_ARB=_C('GL_MAX_PROGRAM_PARAMETERS_ARB',0x88A9)
GL_MAX_PROGRAM_TEMPORARIES_ARB=_C('GL_MAX_PROGRAM_TEMPORARIES_ARB',0x88A5)
GL_MAX_PROGRAM_TEX_INDIRECTIONS_ARB=_C('GL_MAX_PROGRAM_TEX_INDIRECTIONS_ARB',0x880D)
GL_MAX_PROGRAM_TEX_INSTRUCTIONS_ARB=_C('GL_MAX_PROGRAM_TEX_INSTRUCTIONS_ARB',0x880C)
GL_MAX_TEXTURE_COORDS_ARB=_C('GL_MAX_TEXTURE_COORDS_ARB',0x8871)
GL_MAX_TEXTURE_IMAGE_UNITS_ARB=_C('GL_MAX_TEXTURE_IMAGE_UNITS_ARB',0x8872)
GL_PROGRAM_ALU_INSTRUCTIONS_ARB=_C('GL_PROGRAM_ALU_INSTRUCTIONS_ARB',0x8805)
GL_PROGRAM_ATTRIBS_ARB=_C('GL_PROGRAM_ATTRIBS_ARB',0x88AC)
GL_PROGRAM_BINDING_ARB=_C('GL_PROGRAM_BINDING_ARB',0x8677)
GL_PROGRAM_ERROR_POSITION_ARB=_C('GL_PROGRAM_ERROR_POSITION_ARB',0x864B)
GL_PROGRAM_ERROR_STRING_ARB=_C('GL_PROGRAM_ERROR_STRING_ARB',0x8874)
GL_PROGRAM_FORMAT_ARB=_C('GL_PROGRAM_FORMAT_ARB',0x8876)
GL_PROGRAM_FORMAT_ASCII_ARB=_C('GL_PROGRAM_FORMAT_ASCII_ARB',0x8875)
GL_PROGRAM_INSTRUCTIONS_ARB=_C('GL_PROGRAM_INSTRUCTIONS_ARB',0x88A0)
GL_PROGRAM_LENGTH_ARB=_C('GL_PROGRAM_LENGTH_ARB',0x8627)
GL_PROGRAM_NATIVE_ALU_INSTRUCTIONS_ARB=_C('GL_PROGRAM_NATIVE_ALU_INSTRUCTIONS_ARB',0x8808)
GL_PROGRAM_NATIVE_ATTRIBS_ARB=_C('GL_PROGRAM_NATIVE_ATTRIBS_ARB',0x88AE)
GL_PROGRAM_NATIVE_INSTRUCTIONS_ARB=_C('GL_PROGRAM_NATIVE_INSTRUCTIONS_ARB',0x88A2)
GL_PROGRAM_NATIVE_PARAMETERS_ARB=_C('GL_PROGRAM_NATIVE_PARAMETERS_ARB',0x88AA)
GL_PROGRAM_NATIVE_TEMPORARIES_ARB=_C('GL_PROGRAM_NATIVE_TEMPORARIES_ARB',0x88A6)
GL_PROGRAM_NATIVE_TEX_INDIRECTIONS_ARB=_C('GL_PROGRAM_NATIVE_TEX_INDIRECTIONS_ARB',0x880A)
GL_PROGRAM_NATIVE_TEX_INSTRUCTIONS_ARB=_C('GL_PROGRAM_NATIVE_TEX_INSTRUCTIONS_ARB',0x8809)
GL_PROGRAM_PARAMETERS_ARB=_C('GL_PROGRAM_PARAMETERS_ARB',0x88A8)
GL_PROGRAM_STRING_ARB=_C('GL_PROGRAM_STRING_ARB',0x8628)
GL_PROGRAM_TEMPORARIES_ARB=_C('GL_PROGRAM_TEMPORARIES_ARB',0x88A4)
GL_PROGRAM_TEX_INDIRECTIONS_ARB=_C('GL_PROGRAM_TEX_INDIRECTIONS_ARB',0x8807)
GL_PROGRAM_TEX_INSTRUCTIONS_ARB=_C('GL_PROGRAM_TEX_INSTRUCTIONS_ARB',0x8806)
GL_PROGRAM_UNDER_NATIVE_LIMITS_ARB=_C('GL_PROGRAM_UNDER_NATIVE_LIMITS_ARB',0x88B6)
GL_TRANSPOSE_CURRENT_MATRIX_ARB=_C('GL_TRANSPOSE_CURRENT_MATRIX_ARB',0x88B7)
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint)
def glBindProgramARB(target,program):pass
@_f
@_p.types(None,_cs.GLsizei,arrays.GLuintArray)
def glDeleteProgramsARB(n,programs):pass
@_f
@_p.types(None,_cs.GLsizei,arrays.GLuintArray)
def glGenProgramsARB(n,programs):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLdoubleArray)
def glGetProgramEnvParameterdvARB(target,index,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLfloatArray)
def glGetProgramEnvParameterfvARB(target,index,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLdoubleArray)
def glGetProgramLocalParameterdvARB(target,index,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLfloatArray)
def glGetProgramLocalParameterfvARB(target,index,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,ctypes.c_void_p)
def glGetProgramStringARB(target,pname,string):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,arrays.GLintArray)
def glGetProgramivARB(target,pname,params):pass
@_f
@_p.types(_cs.GLboolean,_cs.GLuint)
def glIsProgramARB(program):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,_cs.GLdouble,_cs.GLdouble,_cs.GLdouble,_cs.GLdouble)
def glProgramEnvParameter4dARB(target,index,x,y,z,w):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLdoubleArray)
def glProgramEnvParameter4dvARB(target,index,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,_cs.GLfloat,_cs.GLfloat,_cs.GLfloat,_cs.GLfloat)
def glProgramEnvParameter4fARB(target,index,x,y,z,w):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLfloatArray)
def glProgramEnvParameter4fvARB(target,index,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,_cs.GLdouble,_cs.GLdouble,_cs.GLdouble,_cs.GLdouble)
def glProgramLocalParameter4dARB(target,index,x,y,z,w):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLdoubleArray)
def glProgramLocalParameter4dvARB(target,index,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,_cs.GLfloat,_cs.GLfloat,_cs.GLfloat,_cs.GLfloat)
def glProgramLocalParameter4fARB(target,index,x,y,z,w):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLfloatArray)
def glProgramLocalParameter4fvARB(target,index,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,_cs.GLsizei,ctypes.c_void_p)
def glProgramStringARB(target,format,len,string):pass
