'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLX import _types as _cs
# End users want this...
from OpenGL.raw.GLX._types import *
from OpenGL.raw.GLX import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLX_ARB_create_context'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLX,'GLX_ARB_create_context',error_checker=_errors._error_checker)
GLX_CONTEXT_DEBUG_BIT_ARB=_C('GLX_CONTEXT_DEBUG_BIT_ARB',0x00000001)
GLX_CONTEXT_FLAGS_ARB=_C('GLX_CONTEXT_FLAGS_ARB',0x2094)
GLX_CONTEXT_FORWARD_COMPATIBLE_BIT_ARB=_C('GLX_CONTEXT_FORWARD_COMPATIBLE_BIT_ARB',0x00000002)
GLX_CONTEXT_MAJOR_VERSION_ARB=_C('GLX_CONTEXT_MAJOR_VERSION_ARB',0x2091)
GLX_CONTEXT_MINOR_VERSION_ARB=_C('GLX_CONTEXT_MINOR_VERSION_ARB',0x2092)
@_f
@_p.types(_cs.GLXContext,ctypes.POINTER(_cs.Display),_cs.GLXFBConfig,_cs.GLXContext,_cs.Bool,ctypes.POINTER(_cs.c_int))
def glXCreateContextAttribsARB(dpy,config,share_context,direct,attrib_list):pass
