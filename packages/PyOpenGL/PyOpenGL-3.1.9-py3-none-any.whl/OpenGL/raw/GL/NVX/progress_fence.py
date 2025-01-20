'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_NVX_progress_fence'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_NVX_progress_fence',error_checker=_errors._error_checker)

@_f
@_p.types(None,_cs.GLsizei,arrays.GLuintArray,arrays.GLuint64Array)
def glClientWaitSemaphoreui64NVX(fenceObjectCount,semaphoreArray,fenceValueArray):pass
@_f
@_p.types(_cs.GLuint,)
def glCreateProgressFenceNVX():pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLsizei,arrays.GLuintArray,arrays.GLuint64Array)
def glSignalSemaphoreui64NVX(signalGpu,fenceObjectCount,semaphoreArray,fenceValueArray):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLsizei,arrays.GLuintArray,arrays.GLuint64Array)
def glWaitSemaphoreui64NVX(waitGpu,fenceObjectCount,semaphoreArray,fenceValueArray):pass
