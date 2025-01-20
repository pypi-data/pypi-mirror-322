'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.EGL import _types as _cs
# End users want this...
from OpenGL.raw.EGL._types import *
from OpenGL.raw.EGL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'EGL_KHR_debug'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.EGL,'EGL_KHR_debug',error_checker=_errors._error_checker)
EGL_DEBUG_CALLBACK_KHR=_C('EGL_DEBUG_CALLBACK_KHR',0x33B8)
EGL_DEBUG_MSG_CRITICAL_KHR=_C('EGL_DEBUG_MSG_CRITICAL_KHR',0x33B9)
EGL_DEBUG_MSG_ERROR_KHR=_C('EGL_DEBUG_MSG_ERROR_KHR',0x33BA)
EGL_DEBUG_MSG_INFO_KHR=_C('EGL_DEBUG_MSG_INFO_KHR',0x33BC)
EGL_DEBUG_MSG_WARN_KHR=_C('EGL_DEBUG_MSG_WARN_KHR',0x33BB)
EGL_OBJECT_CONTEXT_KHR=_C('EGL_OBJECT_CONTEXT_KHR',0x33B2)
EGL_OBJECT_DISPLAY_KHR=_C('EGL_OBJECT_DISPLAY_KHR',0x33B1)
EGL_OBJECT_IMAGE_KHR=_C('EGL_OBJECT_IMAGE_KHR',0x33B4)
EGL_OBJECT_STREAM_KHR=_C('EGL_OBJECT_STREAM_KHR',0x33B6)
EGL_OBJECT_SURFACE_KHR=_C('EGL_OBJECT_SURFACE_KHR',0x33B3)
EGL_OBJECT_SYNC_KHR=_C('EGL_OBJECT_SYNC_KHR',0x33B5)
EGL_OBJECT_THREAD_KHR=_C('EGL_OBJECT_THREAD_KHR',0x33B0)
@_f
@_p.types(_cs.EGLint,_cs.EGLDEBUGPROCKHR,arrays.EGLAttribArray)
def eglDebugMessageControlKHR(callback,attrib_list):pass
@_f
@_p.types(_cs.EGLint,_cs.EGLDisplay,_cs.EGLenum,_cs.EGLObjectKHR,_cs.EGLLabelKHR)
def eglLabelObjectKHR(display,objectType,object,label):pass
@_f
@_p.types(_cs.EGLBoolean,_cs.EGLint,arrays.EGLAttribArray)
def eglQueryDebugKHR(attribute,value):pass
