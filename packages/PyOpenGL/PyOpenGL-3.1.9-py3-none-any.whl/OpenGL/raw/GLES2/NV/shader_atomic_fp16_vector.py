'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLES2 import _types as _cs
# End users want this...
from OpenGL.raw.GLES2._types import *
from OpenGL.raw.GLES2 import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLES2_NV_shader_atomic_fp16_vector'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLES2,'GLES2_NV_shader_atomic_fp16_vector',error_checker=_errors._error_checker)


