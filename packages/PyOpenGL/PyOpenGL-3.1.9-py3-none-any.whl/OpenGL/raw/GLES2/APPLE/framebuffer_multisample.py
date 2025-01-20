'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLES2 import _types as _cs
# End users want this...
from OpenGL.raw.GLES2._types import *
from OpenGL.raw.GLES2 import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLES2_APPLE_framebuffer_multisample'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLES2,'GLES2_APPLE_framebuffer_multisample',error_checker=_errors._error_checker)
GL_DRAW_FRAMEBUFFER_APPLE=_C('GL_DRAW_FRAMEBUFFER_APPLE',0x8CA9)
GL_DRAW_FRAMEBUFFER_BINDING_APPLE=_C('GL_DRAW_FRAMEBUFFER_BINDING_APPLE',0x8CA6)
GL_FRAMEBUFFER_INCOMPLETE_MULTISAMPLE_APPLE=_C('GL_FRAMEBUFFER_INCOMPLETE_MULTISAMPLE_APPLE',0x8D56)
GL_MAX_SAMPLES_APPLE=_C('GL_MAX_SAMPLES_APPLE',0x8D57)
GL_READ_FRAMEBUFFER_APPLE=_C('GL_READ_FRAMEBUFFER_APPLE',0x8CA8)
GL_READ_FRAMEBUFFER_BINDING_APPLE=_C('GL_READ_FRAMEBUFFER_BINDING_APPLE',0x8CAA)
GL_RENDERBUFFER_SAMPLES_APPLE=_C('GL_RENDERBUFFER_SAMPLES_APPLE',0x8CAB)
@_f
@_p.types(None,_cs.GLenum,_cs.GLsizei,_cs.GLenum,_cs.GLsizei,_cs.GLsizei)
def glRenderbufferStorageMultisampleAPPLE(target,samples,internalformat,width,height):pass
@_f
@_p.types(None,)
def glResolveMultisampleFramebufferAPPLE():pass
