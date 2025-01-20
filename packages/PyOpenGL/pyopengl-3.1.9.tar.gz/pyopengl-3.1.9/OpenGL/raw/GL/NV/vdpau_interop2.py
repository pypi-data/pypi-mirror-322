'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_NV_vdpau_interop2'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_NV_vdpau_interop2',error_checker=_errors._error_checker)

@_f
@_p.types(_cs.GLvdpauSurfaceNV,ctypes.c_void_p,_cs.GLenum,_cs.GLsizei,arrays.GLuintArray,_cs.GLboolean)
def glVDPAURegisterVideoSurfaceWithPictureStructureNV(vdpSurface,target,numTextureNames,textureNames,isFrameStructure):pass
