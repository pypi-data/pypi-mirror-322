'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ARB_debug_output'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ARB_debug_output',error_checker=_errors._error_checker)
GL_DEBUG_CALLBACK_FUNCTION_ARB=_C('GL_DEBUG_CALLBACK_FUNCTION_ARB',0x8244)
GL_DEBUG_CALLBACK_USER_PARAM_ARB=_C('GL_DEBUG_CALLBACK_USER_PARAM_ARB',0x8245)
GL_DEBUG_LOGGED_MESSAGES_ARB=_C('GL_DEBUG_LOGGED_MESSAGES_ARB',0x9145)
GL_DEBUG_NEXT_LOGGED_MESSAGE_LENGTH_ARB=_C('GL_DEBUG_NEXT_LOGGED_MESSAGE_LENGTH_ARB',0x8243)
GL_DEBUG_OUTPUT_SYNCHRONOUS_ARB=_C('GL_DEBUG_OUTPUT_SYNCHRONOUS_ARB',0x8242)
GL_DEBUG_SEVERITY_HIGH_ARB=_C('GL_DEBUG_SEVERITY_HIGH_ARB',0x9146)
GL_DEBUG_SEVERITY_LOW_ARB=_C('GL_DEBUG_SEVERITY_LOW_ARB',0x9148)
GL_DEBUG_SEVERITY_MEDIUM_ARB=_C('GL_DEBUG_SEVERITY_MEDIUM_ARB',0x9147)
GL_DEBUG_SOURCE_API_ARB=_C('GL_DEBUG_SOURCE_API_ARB',0x8246)
GL_DEBUG_SOURCE_APPLICATION_ARB=_C('GL_DEBUG_SOURCE_APPLICATION_ARB',0x824A)
GL_DEBUG_SOURCE_OTHER_ARB=_C('GL_DEBUG_SOURCE_OTHER_ARB',0x824B)
GL_DEBUG_SOURCE_SHADER_COMPILER_ARB=_C('GL_DEBUG_SOURCE_SHADER_COMPILER_ARB',0x8248)
GL_DEBUG_SOURCE_THIRD_PARTY_ARB=_C('GL_DEBUG_SOURCE_THIRD_PARTY_ARB',0x8249)
GL_DEBUG_SOURCE_WINDOW_SYSTEM_ARB=_C('GL_DEBUG_SOURCE_WINDOW_SYSTEM_ARB',0x8247)
GL_DEBUG_TYPE_DEPRECATED_BEHAVIOR_ARB=_C('GL_DEBUG_TYPE_DEPRECATED_BEHAVIOR_ARB',0x824D)
GL_DEBUG_TYPE_ERROR_ARB=_C('GL_DEBUG_TYPE_ERROR_ARB',0x824C)
GL_DEBUG_TYPE_OTHER_ARB=_C('GL_DEBUG_TYPE_OTHER_ARB',0x8251)
GL_DEBUG_TYPE_PERFORMANCE_ARB=_C('GL_DEBUG_TYPE_PERFORMANCE_ARB',0x8250)
GL_DEBUG_TYPE_PORTABILITY_ARB=_C('GL_DEBUG_TYPE_PORTABILITY_ARB',0x824F)
GL_DEBUG_TYPE_UNDEFINED_BEHAVIOR_ARB=_C('GL_DEBUG_TYPE_UNDEFINED_BEHAVIOR_ARB',0x824E)
GL_MAX_DEBUG_LOGGED_MESSAGES_ARB=_C('GL_MAX_DEBUG_LOGGED_MESSAGES_ARB',0x9144)
GL_MAX_DEBUG_MESSAGE_LENGTH_ARB=_C('GL_MAX_DEBUG_MESSAGE_LENGTH_ARB',0x9143)
@_f
@_p.types(None,_cs.GLDEBUGPROCARB,ctypes.c_void_p)
def glDebugMessageCallbackARB(callback,userParam):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,_cs.GLenum,_cs.GLsizei,arrays.GLuintArray,_cs.GLboolean)
def glDebugMessageControlARB(source,type,severity,count,ids,enabled):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,_cs.GLuint,_cs.GLenum,_cs.GLsizei,arrays.GLcharArray)
def glDebugMessageInsertARB(source,type,id,severity,length,buf):pass
@_f
@_p.types(_cs.GLuint,_cs.GLuint,_cs.GLsizei,arrays.GLuintArray,arrays.GLuintArray,arrays.GLuintArray,arrays.GLuintArray,arrays.GLsizeiArray,arrays.GLcharArray)
def glGetDebugMessageLogARB(count,bufSize,sources,types,ids,severities,lengths,messageLog):pass
