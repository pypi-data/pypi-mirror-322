'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ARB_texture_multisample'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ARB_texture_multisample',error_checker=_errors._error_checker)
GL_INT_SAMPLER_2D_MULTISAMPLE=_C('GL_INT_SAMPLER_2D_MULTISAMPLE',0x9109)
GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY=_C('GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY',0x910C)
GL_MAX_COLOR_TEXTURE_SAMPLES=_C('GL_MAX_COLOR_TEXTURE_SAMPLES',0x910E)
GL_MAX_DEPTH_TEXTURE_SAMPLES=_C('GL_MAX_DEPTH_TEXTURE_SAMPLES',0x910F)
GL_MAX_INTEGER_SAMPLES=_C('GL_MAX_INTEGER_SAMPLES',0x9110)
GL_MAX_SAMPLE_MASK_WORDS=_C('GL_MAX_SAMPLE_MASK_WORDS',0x8E59)
GL_PROXY_TEXTURE_2D_MULTISAMPLE=_C('GL_PROXY_TEXTURE_2D_MULTISAMPLE',0x9101)
GL_PROXY_TEXTURE_2D_MULTISAMPLE_ARRAY=_C('GL_PROXY_TEXTURE_2D_MULTISAMPLE_ARRAY',0x9103)
GL_SAMPLER_2D_MULTISAMPLE=_C('GL_SAMPLER_2D_MULTISAMPLE',0x9108)
GL_SAMPLER_2D_MULTISAMPLE_ARRAY=_C('GL_SAMPLER_2D_MULTISAMPLE_ARRAY',0x910B)
GL_SAMPLE_MASK=_C('GL_SAMPLE_MASK',0x8E51)
GL_SAMPLE_MASK_VALUE=_C('GL_SAMPLE_MASK_VALUE',0x8E52)
GL_SAMPLE_POSITION=_C('GL_SAMPLE_POSITION',0x8E50)
GL_TEXTURE_2D_MULTISAMPLE=_C('GL_TEXTURE_2D_MULTISAMPLE',0x9100)
GL_TEXTURE_2D_MULTISAMPLE_ARRAY=_C('GL_TEXTURE_2D_MULTISAMPLE_ARRAY',0x9102)
GL_TEXTURE_BINDING_2D_MULTISAMPLE=_C('GL_TEXTURE_BINDING_2D_MULTISAMPLE',0x9104)
GL_TEXTURE_BINDING_2D_MULTISAMPLE_ARRAY=_C('GL_TEXTURE_BINDING_2D_MULTISAMPLE_ARRAY',0x9105)
GL_TEXTURE_FIXED_SAMPLE_LOCATIONS=_C('GL_TEXTURE_FIXED_SAMPLE_LOCATIONS',0x9107)
GL_TEXTURE_SAMPLES=_C('GL_TEXTURE_SAMPLES',0x9106)
GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE=_C('GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE',0x910A)
GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY=_C('GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY',0x910D)
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLfloatArray)
def glGetMultisamplefv(pname,index,val):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLbitfield)
def glSampleMaski(maskNumber,mask):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLsizei,_cs.GLenum,_cs.GLsizei,_cs.GLsizei,_cs.GLboolean)
def glTexImage2DMultisample(target,samples,internalformat,width,height,fixedsamplelocations):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLsizei,_cs.GLenum,_cs.GLsizei,_cs.GLsizei,_cs.GLsizei,_cs.GLboolean)
def glTexImage3DMultisample(target,samples,internalformat,width,height,depth,fixedsamplelocations):pass
