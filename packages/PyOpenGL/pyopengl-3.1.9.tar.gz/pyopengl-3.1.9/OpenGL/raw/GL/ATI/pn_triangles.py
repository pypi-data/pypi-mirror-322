'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ATI_pn_triangles'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ATI_pn_triangles',error_checker=_errors._error_checker)
GL_MAX_PN_TRIANGLES_TESSELATION_LEVEL_ATI=_C('GL_MAX_PN_TRIANGLES_TESSELATION_LEVEL_ATI',0x87F1)
GL_PN_TRIANGLES_ATI=_C('GL_PN_TRIANGLES_ATI',0x87F0)
GL_PN_TRIANGLES_NORMAL_MODE_ATI=_C('GL_PN_TRIANGLES_NORMAL_MODE_ATI',0x87F3)
GL_PN_TRIANGLES_NORMAL_MODE_LINEAR_ATI=_C('GL_PN_TRIANGLES_NORMAL_MODE_LINEAR_ATI',0x87F7)
GL_PN_TRIANGLES_NORMAL_MODE_QUADRATIC_ATI=_C('GL_PN_TRIANGLES_NORMAL_MODE_QUADRATIC_ATI',0x87F8)
GL_PN_TRIANGLES_POINT_MODE_ATI=_C('GL_PN_TRIANGLES_POINT_MODE_ATI',0x87F2)
GL_PN_TRIANGLES_POINT_MODE_CUBIC_ATI=_C('GL_PN_TRIANGLES_POINT_MODE_CUBIC_ATI',0x87F6)
GL_PN_TRIANGLES_POINT_MODE_LINEAR_ATI=_C('GL_PN_TRIANGLES_POINT_MODE_LINEAR_ATI',0x87F5)
GL_PN_TRIANGLES_TESSELATION_LEVEL_ATI=_C('GL_PN_TRIANGLES_TESSELATION_LEVEL_ATI',0x87F4)
@_f
@_p.types(None,_cs.GLenum,_cs.GLfloat)
def glPNTrianglesfATI(pname,param):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLint)
def glPNTrianglesiATI(pname,param):pass
