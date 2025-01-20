'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_NV_conservative_raster_dilate'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_NV_conservative_raster_dilate',error_checker=_errors._error_checker)
GL_CONSERVATIVE_RASTER_DILATE_GRANULARITY_NV=_C('GL_CONSERVATIVE_RASTER_DILATE_GRANULARITY_NV',0x937B)
GL_CONSERVATIVE_RASTER_DILATE_NV=_C('GL_CONSERVATIVE_RASTER_DILATE_NV',0x9379)
GL_CONSERVATIVE_RASTER_DILATE_RANGE_NV=_C('GL_CONSERVATIVE_RASTER_DILATE_RANGE_NV',0x937A)
@_f
@_p.types(None,_cs.GLenum,_cs.GLfloat)
def glConservativeRasterParameterfNV(pname,value):pass
