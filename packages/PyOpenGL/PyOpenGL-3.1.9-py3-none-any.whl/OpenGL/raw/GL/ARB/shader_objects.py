'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ARB_shader_objects'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ARB_shader_objects',error_checker=_errors._error_checker)
GL_BOOL_ARB=_C('GL_BOOL_ARB',0x8B56)
GL_BOOL_VEC2_ARB=_C('GL_BOOL_VEC2_ARB',0x8B57)
GL_BOOL_VEC3_ARB=_C('GL_BOOL_VEC3_ARB',0x8B58)
GL_BOOL_VEC4_ARB=_C('GL_BOOL_VEC4_ARB',0x8B59)
GL_FLOAT_MAT2_ARB=_C('GL_FLOAT_MAT2_ARB',0x8B5A)
GL_FLOAT_MAT3_ARB=_C('GL_FLOAT_MAT3_ARB',0x8B5B)
GL_FLOAT_MAT4_ARB=_C('GL_FLOAT_MAT4_ARB',0x8B5C)
GL_FLOAT_VEC2_ARB=_C('GL_FLOAT_VEC2_ARB',0x8B50)
GL_FLOAT_VEC3_ARB=_C('GL_FLOAT_VEC3_ARB',0x8B51)
GL_FLOAT_VEC4_ARB=_C('GL_FLOAT_VEC4_ARB',0x8B52)
GL_INT_VEC2_ARB=_C('GL_INT_VEC2_ARB',0x8B53)
GL_INT_VEC3_ARB=_C('GL_INT_VEC3_ARB',0x8B54)
GL_INT_VEC4_ARB=_C('GL_INT_VEC4_ARB',0x8B55)
GL_OBJECT_ACTIVE_UNIFORMS_ARB=_C('GL_OBJECT_ACTIVE_UNIFORMS_ARB',0x8B86)
GL_OBJECT_ACTIVE_UNIFORM_MAX_LENGTH_ARB=_C('GL_OBJECT_ACTIVE_UNIFORM_MAX_LENGTH_ARB',0x8B87)
GL_OBJECT_ATTACHED_OBJECTS_ARB=_C('GL_OBJECT_ATTACHED_OBJECTS_ARB',0x8B85)
GL_OBJECT_COMPILE_STATUS_ARB=_C('GL_OBJECT_COMPILE_STATUS_ARB',0x8B81)
GL_OBJECT_DELETE_STATUS_ARB=_C('GL_OBJECT_DELETE_STATUS_ARB',0x8B80)
GL_OBJECT_INFO_LOG_LENGTH_ARB=_C('GL_OBJECT_INFO_LOG_LENGTH_ARB',0x8B84)
GL_OBJECT_LINK_STATUS_ARB=_C('GL_OBJECT_LINK_STATUS_ARB',0x8B82)
GL_OBJECT_SHADER_SOURCE_LENGTH_ARB=_C('GL_OBJECT_SHADER_SOURCE_LENGTH_ARB',0x8B88)
GL_OBJECT_SUBTYPE_ARB=_C('GL_OBJECT_SUBTYPE_ARB',0x8B4F)
GL_OBJECT_TYPE_ARB=_C('GL_OBJECT_TYPE_ARB',0x8B4E)
GL_OBJECT_VALIDATE_STATUS_ARB=_C('GL_OBJECT_VALIDATE_STATUS_ARB',0x8B83)
GL_PROGRAM_OBJECT_ARB=_C('GL_PROGRAM_OBJECT_ARB',0x8B40)
GL_SAMPLER_1D_ARB=_C('GL_SAMPLER_1D_ARB',0x8B5D)
GL_SAMPLER_1D_SHADOW_ARB=_C('GL_SAMPLER_1D_SHADOW_ARB',0x8B61)
GL_SAMPLER_2D_ARB=_C('GL_SAMPLER_2D_ARB',0x8B5E)
GL_SAMPLER_2D_RECT_ARB=_C('GL_SAMPLER_2D_RECT_ARB',0x8B63)
GL_SAMPLER_2D_RECT_SHADOW_ARB=_C('GL_SAMPLER_2D_RECT_SHADOW_ARB',0x8B64)
GL_SAMPLER_2D_SHADOW_ARB=_C('GL_SAMPLER_2D_SHADOW_ARB',0x8B62)
GL_SAMPLER_3D_ARB=_C('GL_SAMPLER_3D_ARB',0x8B5F)
GL_SAMPLER_CUBE_ARB=_C('GL_SAMPLER_CUBE_ARB',0x8B60)
GL_SHADER_OBJECT_ARB=_C('GL_SHADER_OBJECT_ARB',0x8B48)
@_f
@_p.types(None,_cs.GLhandleARB,_cs.GLhandleARB)
def glAttachObjectARB(containerObj,obj):pass
@_f
@_p.types(None,_cs.GLhandleARB)
def glCompileShaderARB(shaderObj):pass
@_f
@_p.types(_cs.GLhandleARB,)
def glCreateProgramObjectARB():pass
@_f
@_p.types(_cs.GLhandleARB,_cs.GLenum)
def glCreateShaderObjectARB(shaderType):pass
@_f
@_p.types(None,_cs.GLhandleARB)
def glDeleteObjectARB(obj):pass
@_f
@_p.types(None,_cs.GLhandleARB,_cs.GLhandleARB)
def glDetachObjectARB(containerObj,attachedObj):pass
@_f
@_p.types(None,_cs.GLhandleARB,_cs.GLuint,_cs.GLsizei,arrays.GLsizeiArray,arrays.GLintArray,arrays.GLuintArray,arrays.GLcharARBArray)
def glGetActiveUniformARB(programObj,index,maxLength,length,size,type,name):pass
@_f
@_p.types(None,_cs.GLhandleARB,_cs.GLsizei,arrays.GLsizeiArray,arrays.GLuintArray)
def glGetAttachedObjectsARB(containerObj,maxCount,count,obj):pass
@_f
@_p.types(_cs.GLhandleARB,_cs.GLenum)
def glGetHandleARB(pname):pass
@_f
@_p.types(None,_cs.GLhandleARB,_cs.GLsizei,arrays.GLsizeiArray,arrays.GLcharARBArray)
def glGetInfoLogARB(obj,maxLength,length,infoLog):pass
@_f
@_p.types(None,_cs.GLhandleARB,_cs.GLenum,arrays.GLfloatArray)
def glGetObjectParameterfvARB(obj,pname,params):pass
@_f
@_p.types(None,_cs.GLhandleARB,_cs.GLenum,arrays.GLintArray)
def glGetObjectParameterivARB(obj,pname,params):pass
@_f
@_p.types(None,_cs.GLhandleARB,_cs.GLsizei,arrays.GLsizeiArray,arrays.GLcharARBArray)
def glGetShaderSourceARB(obj,maxLength,length,source):pass
@_f
@_p.types(_cs.GLint,_cs.GLhandleARB,arrays.GLcharARBArray)
def glGetUniformLocationARB(programObj,name):pass
@_f
@_p.types(None,_cs.GLhandleARB,_cs.GLint,arrays.GLfloatArray)
def glGetUniformfvARB(programObj,location,params):pass
@_f
@_p.types(None,_cs.GLhandleARB,_cs.GLint,arrays.GLintArray)
def glGetUniformivARB(programObj,location,params):pass
@_f
@_p.types(None,_cs.GLhandleARB)
def glLinkProgramARB(programObj):pass
@_f
@_p.types(None,_cs.GLhandleARB,_cs.GLsizei,ctypes.POINTER( ctypes.POINTER( _cs.GLchar )),arrays.GLintArray)
def glShaderSourceARB(shaderObj,count,string,length):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLfloat)
def glUniform1fARB(location,v0):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLsizei,arrays.GLfloatArray)
def glUniform1fvARB(location,count,value):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLint)
def glUniform1iARB(location,v0):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLsizei,arrays.GLintArray)
def glUniform1ivARB(location,count,value):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLfloat,_cs.GLfloat)
def glUniform2fARB(location,v0,v1):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLsizei,arrays.GLfloatArray)
def glUniform2fvARB(location,count,value):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLint,_cs.GLint)
def glUniform2iARB(location,v0,v1):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLsizei,arrays.GLintArray)
def glUniform2ivARB(location,count,value):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLfloat,_cs.GLfloat,_cs.GLfloat)
def glUniform3fARB(location,v0,v1,v2):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLsizei,arrays.GLfloatArray)
def glUniform3fvARB(location,count,value):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint)
def glUniform3iARB(location,v0,v1,v2):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLsizei,arrays.GLintArray)
def glUniform3ivARB(location,count,value):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLfloat,_cs.GLfloat,_cs.GLfloat,_cs.GLfloat)
def glUniform4fARB(location,v0,v1,v2,v3):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLsizei,arrays.GLfloatArray)
def glUniform4fvARB(location,count,value):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint)
def glUniform4iARB(location,v0,v1,v2,v3):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLsizei,arrays.GLintArray)
def glUniform4ivARB(location,count,value):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLfloatArray)
def glUniformMatrix2fvARB(location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLfloatArray)
def glUniformMatrix3fvARB(location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLfloatArray)
def glUniformMatrix4fvARB(location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLhandleARB)
def glUseProgramObjectARB(programObj):pass
@_f
@_p.types(None,_cs.GLhandleARB)
def glValidateProgramARB(programObj):pass
