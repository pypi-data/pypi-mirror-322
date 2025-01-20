'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLES2 import _types as _cs
# End users want this...
from OpenGL.raw.GLES2._types import *
from OpenGL.raw.GLES2 import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLES2_QCOM_extended_get2'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLES2,'GLES2_QCOM_extended_get2',error_checker=_errors._error_checker)

@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,arrays.GLcharArray,arrays.GLintArray)
def glExtGetProgramBinarySourceQCOM(program,shadertype,source,length):pass
@_f
@_p.types(None,arrays.GLuintArray,_cs.GLint,arrays.GLintArray)
def glExtGetProgramsQCOM(programs,maxPrograms,numPrograms):pass
@_f
@_p.types(None,arrays.GLuintArray,_cs.GLint,arrays.GLintArray)
def glExtGetShadersQCOM(shaders,maxShaders,numShaders):pass
@_f
@_p.types(_cs.GLboolean,_cs.GLuint)
def glExtIsProgramBinaryQCOM(program):pass
