'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.EGL import _types as _cs
# End users want this...
from OpenGL.raw.EGL._types import *
from OpenGL.raw.EGL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'EGL_ANDROID_recordable'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.EGL,'EGL_ANDROID_recordable',error_checker=_errors._error_checker)
EGL_RECORDABLE_ANDROID=_C('EGL_RECORDABLE_ANDROID',0x3142)

