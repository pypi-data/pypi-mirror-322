'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.WGL import _types as _cs
# End users want this...
from OpenGL.raw.WGL._types import *
from OpenGL.raw.WGL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'WGL_I3D_gamma'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.WGL,'WGL_I3D_gamma',error_checker=_errors._error_checker)
WGL_GAMMA_EXCLUDE_DESKTOP_I3D=_C('WGL_GAMMA_EXCLUDE_DESKTOP_I3D',0x204F)
WGL_GAMMA_TABLE_SIZE_I3D=_C('WGL_GAMMA_TABLE_SIZE_I3D',0x204E)
@_f
@_p.types(_cs.BOOL,_cs.HDC,_cs.c_int,ctypes.POINTER(_cs.USHORT),ctypes.POINTER(_cs.USHORT),ctypes.POINTER(_cs.USHORT))
def wglGetGammaTableI3D(hDC,iEntries,puRed,puGreen,puBlue):pass
@_f
@_p.types(_cs.BOOL,_cs.HDC,_cs.c_int,ctypes.POINTER(_cs.c_int))
def wglGetGammaTableParametersI3D(hDC,iAttribute,piValue):pass
@_f
@_p.types(_cs.BOOL,_cs.HDC,_cs.c_int,ctypes.POINTER(_cs.USHORT),ctypes.POINTER(_cs.USHORT),ctypes.POINTER(_cs.USHORT))
def wglSetGammaTableI3D(hDC,iEntries,puRed,puGreen,puBlue):pass
@_f
@_p.types(_cs.BOOL,_cs.HDC,_cs.c_int,ctypes.POINTER(_cs.c_int))
def wglSetGammaTableParametersI3D(hDC,iAttribute,piValue):pass
