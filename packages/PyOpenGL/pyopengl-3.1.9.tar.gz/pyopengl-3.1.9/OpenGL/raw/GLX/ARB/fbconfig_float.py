'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLX import _types as _cs
# End users want this...
from OpenGL.raw.GLX._types import *
from OpenGL.raw.GLX import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLX_ARB_fbconfig_float'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLX,'GLX_ARB_fbconfig_float',error_checker=_errors._error_checker)
GLX_RGBA_FLOAT_BIT_ARB=_C('GLX_RGBA_FLOAT_BIT_ARB',0x00000004)
GLX_RGBA_FLOAT_TYPE_ARB=_C('GLX_RGBA_FLOAT_TYPE_ARB',0x20B9)

