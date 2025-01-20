'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.EGL import _types as _cs
# End users want this...
from OpenGL.raw.EGL._types import *
from OpenGL.raw.EGL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'EGL_NV_stream_sync'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.EGL,'EGL_NV_stream_sync',error_checker=_errors._error_checker)
EGL_SYNC_NEW_FRAME_NV=_C('EGL_SYNC_NEW_FRAME_NV',0x321F)
EGL_SYNC_TYPE_KHR=_C('EGL_SYNC_TYPE_KHR',0x30F7)
@_f
@_p.types(_cs.EGLSyncKHR,_cs.EGLDisplay,_cs.EGLStreamKHR,_cs.EGLenum,arrays.GLintArray)
def eglCreateStreamSyncNV(dpy,stream,type,attrib_list):pass
