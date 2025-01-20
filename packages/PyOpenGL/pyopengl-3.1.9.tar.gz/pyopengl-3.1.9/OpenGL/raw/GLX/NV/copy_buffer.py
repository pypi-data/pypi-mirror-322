'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLX import _types as _cs
# End users want this...
from OpenGL.raw.GLX._types import *
from OpenGL.raw.GLX import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLX_NV_copy_buffer'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLX,'GLX_NV_copy_buffer',error_checker=_errors._error_checker)

@_f
@_p.types(None,ctypes.POINTER(_cs.Display),_cs.GLXContext,_cs.GLXContext,_cs.GLenum,_cs.GLenum,_cs.GLintptr,_cs.GLintptr,_cs.GLsizeiptr)
def glXCopyBufferSubDataNV(dpy,readCtx,writeCtx,readTarget,writeTarget,readOffset,writeOffset,size):pass
@_f
@_p.types(None,ctypes.POINTER(_cs.Display),_cs.GLXContext,_cs.GLXContext,_cs.GLuint,_cs.GLuint,_cs.GLintptr,_cs.GLintptr,_cs.GLsizeiptr)
def glXNamedCopyBufferSubDataNV(dpy,readCtx,writeCtx,readBuffer,writeBuffer,readOffset,writeOffset,size):pass
