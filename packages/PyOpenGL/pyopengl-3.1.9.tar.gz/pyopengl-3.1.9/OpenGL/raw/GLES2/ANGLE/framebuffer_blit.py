'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLES2 import _types as _cs
# End users want this...
from OpenGL.raw.GLES2._types import *
from OpenGL.raw.GLES2 import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLES2_ANGLE_framebuffer_blit'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLES2,'GLES2_ANGLE_framebuffer_blit',error_checker=_errors._error_checker)
GL_DRAW_FRAMEBUFFER_ANGLE=_C('GL_DRAW_FRAMEBUFFER_ANGLE',0x8CA9)
GL_DRAW_FRAMEBUFFER_BINDING_ANGLE=_C('GL_DRAW_FRAMEBUFFER_BINDING_ANGLE',0x8CA6)
GL_READ_FRAMEBUFFER_ANGLE=_C('GL_READ_FRAMEBUFFER_ANGLE',0x8CA8)
GL_READ_FRAMEBUFFER_BINDING_ANGLE=_C('GL_READ_FRAMEBUFFER_BINDING_ANGLE',0x8CAA)
@_f
@_p.types(None,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLbitfield,_cs.GLenum)
def glBlitFramebufferANGLE(srcX0,srcY0,srcX1,srcY1,dstX0,dstY0,dstX1,dstY1,mask,filter):pass
