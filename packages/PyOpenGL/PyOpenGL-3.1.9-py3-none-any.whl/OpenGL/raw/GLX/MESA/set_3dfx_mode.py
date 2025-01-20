'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLX import _types as _cs
# End users want this...
from OpenGL.raw.GLX._types import *
from OpenGL.raw.GLX import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLX_MESA_set_3dfx_mode'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLX,'GLX_MESA_set_3dfx_mode',error_checker=_errors._error_checker)
GLX_3DFX_FULLSCREEN_MODE_MESA=_C('GLX_3DFX_FULLSCREEN_MODE_MESA',0x2)
GLX_3DFX_WINDOW_MODE_MESA=_C('GLX_3DFX_WINDOW_MODE_MESA',0x1)
@_f
@_p.types(_cs.GLboolean,_cs.GLint)
def glXSet3DfxModeMESA(mode):pass
