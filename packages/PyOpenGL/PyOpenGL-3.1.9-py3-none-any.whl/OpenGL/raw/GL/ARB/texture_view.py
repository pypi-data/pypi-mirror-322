'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ARB_texture_view'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ARB_texture_view',error_checker=_errors._error_checker)
GL_TEXTURE_IMMUTABLE_LEVELS=_C('GL_TEXTURE_IMMUTABLE_LEVELS',0x82DF)
GL_TEXTURE_VIEW_MIN_LAYER=_C('GL_TEXTURE_VIEW_MIN_LAYER',0x82DD)
GL_TEXTURE_VIEW_MIN_LEVEL=_C('GL_TEXTURE_VIEW_MIN_LEVEL',0x82DB)
GL_TEXTURE_VIEW_NUM_LAYERS=_C('GL_TEXTURE_VIEW_NUM_LAYERS',0x82DE)
GL_TEXTURE_VIEW_NUM_LEVELS=_C('GL_TEXTURE_VIEW_NUM_LEVELS',0x82DC)
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,_cs.GLuint,_cs.GLenum,_cs.GLuint,_cs.GLuint,_cs.GLuint,_cs.GLuint)
def glTextureView(texture,target,origtexture,internalformat,minlevel,numlevels,minlayer,numlayers):pass
