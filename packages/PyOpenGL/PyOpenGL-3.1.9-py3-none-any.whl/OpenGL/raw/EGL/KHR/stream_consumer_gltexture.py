'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.EGL import _types as _cs
# End users want this...
from OpenGL.raw.EGL._types import *
from OpenGL.raw.EGL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'EGL_KHR_stream_consumer_gltexture'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.EGL,'EGL_KHR_stream_consumer_gltexture',error_checker=_errors._error_checker)
EGL_CONSUMER_ACQUIRE_TIMEOUT_USEC_KHR=_C('EGL_CONSUMER_ACQUIRE_TIMEOUT_USEC_KHR',0x321E)
@_f
@_p.types(_cs.EGLBoolean,_cs.EGLDisplay,_cs.EGLStreamKHR)
def eglStreamConsumerAcquireKHR(dpy,stream):pass
@_f
@_p.types(_cs.EGLBoolean,_cs.EGLDisplay,_cs.EGLStreamKHR)
def eglStreamConsumerGLTextureExternalKHR(dpy,stream):pass
@_f
@_p.types(_cs.EGLBoolean,_cs.EGLDisplay,_cs.EGLStreamKHR)
def eglStreamConsumerReleaseKHR(dpy,stream):pass
