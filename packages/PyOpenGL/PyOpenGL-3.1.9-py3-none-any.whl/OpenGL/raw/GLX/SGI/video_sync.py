'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLX import _types as _cs
# End users want this...
from OpenGL.raw.GLX._types import *
from OpenGL.raw.GLX import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLX_SGI_video_sync'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLX,'GLX_SGI_video_sync',error_checker=_errors._error_checker)

@_f
@_p.types(_cs.c_int,ctypes.POINTER(_cs.c_uint))
def glXGetVideoSyncSGI(count):pass
@_f
@_p.types(_cs.c_int,_cs.c_int,_cs.c_int,ctypes.POINTER(_cs.c_uint))
def glXWaitVideoSyncSGI(divisor,remainder,count):pass
