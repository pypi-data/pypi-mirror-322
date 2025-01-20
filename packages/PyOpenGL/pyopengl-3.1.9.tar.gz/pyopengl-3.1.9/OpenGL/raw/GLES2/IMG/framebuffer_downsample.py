'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLES2 import _types as _cs
# End users want this...
from OpenGL.raw.GLES2._types import *
from OpenGL.raw.GLES2 import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLES2_IMG_framebuffer_downsample'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLES2,'GLES2_IMG_framebuffer_downsample',error_checker=_errors._error_checker)
GL_DOWNSAMPLE_SCALES_IMG=_C('GL_DOWNSAMPLE_SCALES_IMG',0x913E)
GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_SCALE_IMG=_C('GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_SCALE_IMG',0x913F)
GL_FRAMEBUFFER_INCOMPLETE_MULTISAMPLE_AND_DOWNSAMPLE_IMG=_C('GL_FRAMEBUFFER_INCOMPLETE_MULTISAMPLE_AND_DOWNSAMPLE_IMG',0x913C)
GL_NUM_DOWNSAMPLE_SCALES_IMG=_C('GL_NUM_DOWNSAMPLE_SCALES_IMG',0x913D)
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,_cs.GLenum,_cs.GLuint,_cs.GLint,_cs.GLint,_cs.GLint)
def glFramebufferTexture2DDownsampleIMG(target,attachment,textarget,texture,level,xscale,yscale):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,_cs.GLuint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint)
def glFramebufferTextureLayerDownsampleIMG(target,attachment,texture,level,layer,xscale,yscale):pass
