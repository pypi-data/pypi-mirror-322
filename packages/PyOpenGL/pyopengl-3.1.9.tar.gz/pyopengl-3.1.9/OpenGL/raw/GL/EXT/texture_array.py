'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_EXT_texture_array'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_EXT_texture_array',error_checker=_errors._error_checker)
GL_COMPARE_REF_DEPTH_TO_TEXTURE_EXT=_C('GL_COMPARE_REF_DEPTH_TO_TEXTURE_EXT',0x884E)
GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LAYER_EXT=_C('GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LAYER_EXT',0x8CD4)
GL_MAX_ARRAY_TEXTURE_LAYERS_EXT=_C('GL_MAX_ARRAY_TEXTURE_LAYERS_EXT',0x88FF)
GL_PROXY_TEXTURE_1D_ARRAY_EXT=_C('GL_PROXY_TEXTURE_1D_ARRAY_EXT',0x8C19)
GL_PROXY_TEXTURE_2D_ARRAY_EXT=_C('GL_PROXY_TEXTURE_2D_ARRAY_EXT',0x8C1B)
GL_TEXTURE_1D_ARRAY_EXT=_C('GL_TEXTURE_1D_ARRAY_EXT',0x8C18)
GL_TEXTURE_2D_ARRAY_EXT=_C('GL_TEXTURE_2D_ARRAY_EXT',0x8C1A)
GL_TEXTURE_BINDING_1D_ARRAY_EXT=_C('GL_TEXTURE_BINDING_1D_ARRAY_EXT',0x8C1C)
GL_TEXTURE_BINDING_2D_ARRAY_EXT=_C('GL_TEXTURE_BINDING_2D_ARRAY_EXT',0x8C1D)
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,_cs.GLuint,_cs.GLint,_cs.GLint)
def glFramebufferTextureLayerEXT(target,attachment,texture,level,layer):pass
