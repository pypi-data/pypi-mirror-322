'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ARB_separate_shader_objects'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ARB_separate_shader_objects',error_checker=_errors._error_checker)
GL_ACTIVE_PROGRAM=_C('GL_ACTIVE_PROGRAM',0x8259)
GL_ALL_SHADER_BITS=_C('GL_ALL_SHADER_BITS',0xFFFFFFFF)
GL_FRAGMENT_SHADER_BIT=_C('GL_FRAGMENT_SHADER_BIT',0x00000002)
GL_GEOMETRY_SHADER_BIT=_C('GL_GEOMETRY_SHADER_BIT',0x00000004)
GL_PROGRAM_PIPELINE_BINDING=_C('GL_PROGRAM_PIPELINE_BINDING',0x825A)
GL_PROGRAM_SEPARABLE=_C('GL_PROGRAM_SEPARABLE',0x8258)
GL_TESS_CONTROL_SHADER_BIT=_C('GL_TESS_CONTROL_SHADER_BIT',0x00000008)
GL_TESS_EVALUATION_SHADER_BIT=_C('GL_TESS_EVALUATION_SHADER_BIT',0x00000010)
GL_VERTEX_SHADER_BIT=_C('GL_VERTEX_SHADER_BIT',0x00000001)
@_f
@_p.types(None,_cs.GLuint,_cs.GLuint)
def glActiveShaderProgram(pipeline,program):pass
@_f
@_p.types(None,_cs.GLuint)
def glBindProgramPipeline(pipeline):pass
@_f
@_p.types(_cs.GLuint,_cs.GLenum,_cs.GLsizei,ctypes.POINTER( ctypes.POINTER( _cs.GLchar )))
def glCreateShaderProgramv(type,count,strings):pass
@_f
@_p.types(None,_cs.GLsizei,arrays.GLuintArray)
def glDeleteProgramPipelines(n,pipelines):pass
@_f
@_p.types(None,_cs.GLsizei,arrays.GLuintArray)
def glGenProgramPipelines(n,pipelines):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLsizei,arrays.GLsizeiArray,arrays.GLcharArray)
def glGetProgramPipelineInfoLog(pipeline,bufSize,length,infoLog):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,arrays.GLintArray)
def glGetProgramPipelineiv(pipeline,pname,params):pass
@_f
@_p.types(_cs.GLboolean,_cs.GLuint)
def glIsProgramPipeline(pipeline):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,_cs.GLint)
def glProgramParameteri(program,pname,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLdouble)
def glProgramUniform1d(program,location,v0):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,arrays.GLdoubleArray)
def glProgramUniform1dv(program,location,count,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLfloat)
def glProgramUniform1f(program,location,v0):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,arrays.GLfloatArray)
def glProgramUniform1fv(program,location,count,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLint)
def glProgramUniform1i(program,location,v0):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,arrays.GLintArray)
def glProgramUniform1iv(program,location,count,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLuint)
def glProgramUniform1ui(program,location,v0):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,arrays.GLuintArray)
def glProgramUniform1uiv(program,location,count,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLdouble,_cs.GLdouble)
def glProgramUniform2d(program,location,v0,v1):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,arrays.GLdoubleArray)
def glProgramUniform2dv(program,location,count,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLfloat,_cs.GLfloat)
def glProgramUniform2f(program,location,v0,v1):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,arrays.GLfloatArray)
def glProgramUniform2fv(program,location,count,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLint,_cs.GLint)
def glProgramUniform2i(program,location,v0,v1):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,arrays.GLintArray)
def glProgramUniform2iv(program,location,count,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLuint,_cs.GLuint)
def glProgramUniform2ui(program,location,v0,v1):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,arrays.GLuintArray)
def glProgramUniform2uiv(program,location,count,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLdouble,_cs.GLdouble,_cs.GLdouble)
def glProgramUniform3d(program,location,v0,v1,v2):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,arrays.GLdoubleArray)
def glProgramUniform3dv(program,location,count,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLfloat,_cs.GLfloat,_cs.GLfloat)
def glProgramUniform3f(program,location,v0,v1,v2):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,arrays.GLfloatArray)
def glProgramUniform3fv(program,location,count,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint)
def glProgramUniform3i(program,location,v0,v1,v2):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,arrays.GLintArray)
def glProgramUniform3iv(program,location,count,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLuint,_cs.GLuint,_cs.GLuint)
def glProgramUniform3ui(program,location,v0,v1,v2):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,arrays.GLuintArray)
def glProgramUniform3uiv(program,location,count,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLdouble,_cs.GLdouble,_cs.GLdouble,_cs.GLdouble)
def glProgramUniform4d(program,location,v0,v1,v2,v3):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,arrays.GLdoubleArray)
def glProgramUniform4dv(program,location,count,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLfloat,_cs.GLfloat,_cs.GLfloat,_cs.GLfloat)
def glProgramUniform4f(program,location,v0,v1,v2,v3):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,arrays.GLfloatArray)
def glProgramUniform4fv(program,location,count,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint)
def glProgramUniform4i(program,location,v0,v1,v2,v3):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,arrays.GLintArray)
def glProgramUniform4iv(program,location,count,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLuint,_cs.GLuint,_cs.GLuint,_cs.GLuint)
def glProgramUniform4ui(program,location,v0,v1,v2,v3):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,arrays.GLuintArray)
def glProgramUniform4uiv(program,location,count,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLdoubleArray)
def glProgramUniformMatrix2dv(program,location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLfloatArray)
def glProgramUniformMatrix2fv(program,location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLdoubleArray)
def glProgramUniformMatrix2x3dv(program,location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLfloatArray)
def glProgramUniformMatrix2x3fv(program,location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLdoubleArray)
def glProgramUniformMatrix2x4dv(program,location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLfloatArray)
def glProgramUniformMatrix2x4fv(program,location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLdoubleArray)
def glProgramUniformMatrix3dv(program,location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLfloatArray)
def glProgramUniformMatrix3fv(program,location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLdoubleArray)
def glProgramUniformMatrix3x2dv(program,location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLfloatArray)
def glProgramUniformMatrix3x2fv(program,location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLdoubleArray)
def glProgramUniformMatrix3x4dv(program,location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLfloatArray)
def glProgramUniformMatrix3x4fv(program,location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLdoubleArray)
def glProgramUniformMatrix4dv(program,location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLfloatArray)
def glProgramUniformMatrix4fv(program,location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLdoubleArray)
def glProgramUniformMatrix4x2dv(program,location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLfloatArray)
def glProgramUniformMatrix4x2fv(program,location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLdoubleArray)
def glProgramUniformMatrix4x3dv(program,location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLfloatArray)
def glProgramUniformMatrix4x3fv(program,location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLbitfield,_cs.GLuint)
def glUseProgramStages(pipeline,stages,program):pass
@_f
@_p.types(None,_cs.GLuint)
def glValidateProgramPipeline(pipeline):pass
