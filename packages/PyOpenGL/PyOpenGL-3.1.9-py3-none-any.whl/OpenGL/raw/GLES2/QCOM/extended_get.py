'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLES2 import _types as _cs
# End users want this...
from OpenGL.raw.GLES2._types import *
from OpenGL.raw.GLES2 import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLES2_QCOM_extended_get'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLES2,'GLES2_QCOM_extended_get',error_checker=_errors._error_checker)
GL_STATE_RESTORE=_C('GL_STATE_RESTORE',0x8BDC)
GL_TEXTURE_DEPTH_QCOM=_C('GL_TEXTURE_DEPTH_QCOM',0x8BD4)
GL_TEXTURE_FORMAT_QCOM=_C('GL_TEXTURE_FORMAT_QCOM',0x8BD6)
GL_TEXTURE_HEIGHT_QCOM=_C('GL_TEXTURE_HEIGHT_QCOM',0x8BD3)
GL_TEXTURE_IMAGE_VALID_QCOM=_C('GL_TEXTURE_IMAGE_VALID_QCOM',0x8BD8)
GL_TEXTURE_INTERNAL_FORMAT_QCOM=_C('GL_TEXTURE_INTERNAL_FORMAT_QCOM',0x8BD5)
GL_TEXTURE_NUM_LEVELS_QCOM=_C('GL_TEXTURE_NUM_LEVELS_QCOM',0x8BD9)
GL_TEXTURE_OBJECT_VALID_QCOM=_C('GL_TEXTURE_OBJECT_VALID_QCOM',0x8BDB)
GL_TEXTURE_TARGET_QCOM=_C('GL_TEXTURE_TARGET_QCOM',0x8BDA)
GL_TEXTURE_TYPE_QCOM=_C('GL_TEXTURE_TYPE_QCOM',0x8BD7)
GL_TEXTURE_WIDTH_QCOM=_C('GL_TEXTURE_WIDTH_QCOM',0x8BD2)
@_f
@_p.types(None,_cs.GLenum,arrays.GLvoidpArray)
def glExtGetBufferPointervQCOM(target,params):pass
@_f
@_p.types(None,arrays.GLuintArray,_cs.GLint,arrays.GLintArray)
def glExtGetBuffersQCOM(buffers,maxBuffers,numBuffers):pass
@_f
@_p.types(None,arrays.GLuintArray,_cs.GLint,arrays.GLintArray)
def glExtGetFramebuffersQCOM(framebuffers,maxFramebuffers,numFramebuffers):pass
@_f
@_p.types(None,arrays.GLuintArray,_cs.GLint,arrays.GLintArray)
def glExtGetRenderbuffersQCOM(renderbuffers,maxRenderbuffers,numRenderbuffers):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,_cs.GLint,_cs.GLenum,arrays.GLintArray)
def glExtGetTexLevelParameterivQCOM(texture,face,level,pname,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLsizei,_cs.GLsizei,_cs.GLsizei,_cs.GLenum,_cs.GLenum,ctypes.c_void_p)
def glExtGetTexSubImageQCOM(target,level,xoffset,yoffset,zoffset,width,height,depth,format,type,texels):pass
@_f
@_p.types(None,arrays.GLuintArray,_cs.GLint,arrays.GLintArray)
def glExtGetTexturesQCOM(textures,maxTextures,numTextures):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,_cs.GLint)
def glExtTexObjectStateOverrideiQCOM(target,pname,param):pass
