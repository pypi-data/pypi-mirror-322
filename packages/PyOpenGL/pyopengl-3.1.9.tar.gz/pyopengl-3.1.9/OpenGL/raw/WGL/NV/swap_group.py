'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.WGL import _types as _cs
# End users want this...
from OpenGL.raw.WGL._types import *
from OpenGL.raw.WGL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'WGL_NV_swap_group'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.WGL,'WGL_NV_swap_group',error_checker=_errors._error_checker)

@_f
@_p.types(_cs.BOOL,_cs.GLuint,_cs.GLuint)
def wglBindSwapBarrierNV(group,barrier):pass
@_f
@_p.types(_cs.BOOL,_cs.HDC,_cs.GLuint)
def wglJoinSwapGroupNV(hDC,group):pass
@_f
@_p.types(_cs.BOOL,_cs.HDC,arrays.GLuintArray)
def wglQueryFrameCountNV(hDC,count):pass
@_f
@_p.types(_cs.BOOL,_cs.HDC,arrays.GLuintArray,arrays.GLuintArray)
def wglQueryMaxSwapGroupsNV(hDC,maxGroups,maxBarriers):pass
@_f
@_p.types(_cs.BOOL,_cs.HDC,arrays.GLuintArray,arrays.GLuintArray)
def wglQuerySwapGroupNV(hDC,group,barrier):pass
@_f
@_p.types(_cs.BOOL,_cs.HDC)
def wglResetFrameCountNV(hDC):pass
