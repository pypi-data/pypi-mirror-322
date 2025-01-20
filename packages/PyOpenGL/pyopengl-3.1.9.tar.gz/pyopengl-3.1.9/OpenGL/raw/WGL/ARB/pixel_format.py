'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.WGL import _types as _cs
# End users want this...
from OpenGL.raw.WGL._types import *
from OpenGL.raw.WGL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'WGL_ARB_pixel_format'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.WGL,'WGL_ARB_pixel_format',error_checker=_errors._error_checker)
WGL_ACCELERATION_ARB=_C('WGL_ACCELERATION_ARB',0x2003)
WGL_ACCUM_ALPHA_BITS_ARB=_C('WGL_ACCUM_ALPHA_BITS_ARB',0x2021)
WGL_ACCUM_BITS_ARB=_C('WGL_ACCUM_BITS_ARB',0x201D)
WGL_ACCUM_BLUE_BITS_ARB=_C('WGL_ACCUM_BLUE_BITS_ARB',0x2020)
WGL_ACCUM_GREEN_BITS_ARB=_C('WGL_ACCUM_GREEN_BITS_ARB',0x201F)
WGL_ACCUM_RED_BITS_ARB=_C('WGL_ACCUM_RED_BITS_ARB',0x201E)
WGL_ALPHA_BITS_ARB=_C('WGL_ALPHA_BITS_ARB',0x201B)
WGL_ALPHA_SHIFT_ARB=_C('WGL_ALPHA_SHIFT_ARB',0x201C)
WGL_AUX_BUFFERS_ARB=_C('WGL_AUX_BUFFERS_ARB',0x2024)
WGL_BLUE_BITS_ARB=_C('WGL_BLUE_BITS_ARB',0x2019)
WGL_BLUE_SHIFT_ARB=_C('WGL_BLUE_SHIFT_ARB',0x201A)
WGL_COLOR_BITS_ARB=_C('WGL_COLOR_BITS_ARB',0x2014)
WGL_DEPTH_BITS_ARB=_C('WGL_DEPTH_BITS_ARB',0x2022)
WGL_DOUBLE_BUFFER_ARB=_C('WGL_DOUBLE_BUFFER_ARB',0x2011)
WGL_DRAW_TO_BITMAP_ARB=_C('WGL_DRAW_TO_BITMAP_ARB',0x2002)
WGL_DRAW_TO_WINDOW_ARB=_C('WGL_DRAW_TO_WINDOW_ARB',0x2001)
WGL_FULL_ACCELERATION_ARB=_C('WGL_FULL_ACCELERATION_ARB',0x2027)
WGL_GENERIC_ACCELERATION_ARB=_C('WGL_GENERIC_ACCELERATION_ARB',0x2026)
WGL_GREEN_BITS_ARB=_C('WGL_GREEN_BITS_ARB',0x2017)
WGL_GREEN_SHIFT_ARB=_C('WGL_GREEN_SHIFT_ARB',0x2018)
WGL_NEED_PALETTE_ARB=_C('WGL_NEED_PALETTE_ARB',0x2004)
WGL_NEED_SYSTEM_PALETTE_ARB=_C('WGL_NEED_SYSTEM_PALETTE_ARB',0x2005)
WGL_NO_ACCELERATION_ARB=_C('WGL_NO_ACCELERATION_ARB',0x2025)
WGL_NUMBER_OVERLAYS_ARB=_C('WGL_NUMBER_OVERLAYS_ARB',0x2008)
WGL_NUMBER_PIXEL_FORMATS_ARB=_C('WGL_NUMBER_PIXEL_FORMATS_ARB',0x2000)
WGL_NUMBER_UNDERLAYS_ARB=_C('WGL_NUMBER_UNDERLAYS_ARB',0x2009)
WGL_PIXEL_TYPE_ARB=_C('WGL_PIXEL_TYPE_ARB',0x2013)
WGL_RED_BITS_ARB=_C('WGL_RED_BITS_ARB',0x2015)
WGL_RED_SHIFT_ARB=_C('WGL_RED_SHIFT_ARB',0x2016)
WGL_SHARE_ACCUM_ARB=_C('WGL_SHARE_ACCUM_ARB',0x200E)
WGL_SHARE_DEPTH_ARB=_C('WGL_SHARE_DEPTH_ARB',0x200C)
WGL_SHARE_STENCIL_ARB=_C('WGL_SHARE_STENCIL_ARB',0x200D)
WGL_STENCIL_BITS_ARB=_C('WGL_STENCIL_BITS_ARB',0x2023)
WGL_STEREO_ARB=_C('WGL_STEREO_ARB',0x2012)
WGL_SUPPORT_GDI_ARB=_C('WGL_SUPPORT_GDI_ARB',0x200F)
WGL_SUPPORT_OPENGL_ARB=_C('WGL_SUPPORT_OPENGL_ARB',0x2010)
WGL_SWAP_COPY_ARB=_C('WGL_SWAP_COPY_ARB',0x2029)
WGL_SWAP_EXCHANGE_ARB=_C('WGL_SWAP_EXCHANGE_ARB',0x2028)
WGL_SWAP_LAYER_BUFFERS_ARB=_C('WGL_SWAP_LAYER_BUFFERS_ARB',0x2006)
WGL_SWAP_METHOD_ARB=_C('WGL_SWAP_METHOD_ARB',0x2007)
WGL_SWAP_UNDEFINED_ARB=_C('WGL_SWAP_UNDEFINED_ARB',0x202A)
WGL_TRANSPARENT_ALPHA_VALUE_ARB=_C('WGL_TRANSPARENT_ALPHA_VALUE_ARB',0x203A)
WGL_TRANSPARENT_ARB=_C('WGL_TRANSPARENT_ARB',0x200A)
WGL_TRANSPARENT_BLUE_VALUE_ARB=_C('WGL_TRANSPARENT_BLUE_VALUE_ARB',0x2039)
WGL_TRANSPARENT_GREEN_VALUE_ARB=_C('WGL_TRANSPARENT_GREEN_VALUE_ARB',0x2038)
WGL_TRANSPARENT_INDEX_VALUE_ARB=_C('WGL_TRANSPARENT_INDEX_VALUE_ARB',0x203B)
WGL_TRANSPARENT_RED_VALUE_ARB=_C('WGL_TRANSPARENT_RED_VALUE_ARB',0x2037)
WGL_TYPE_COLORINDEX_ARB=_C('WGL_TYPE_COLORINDEX_ARB',0x202C)
WGL_TYPE_RGBA_ARB=_C('WGL_TYPE_RGBA_ARB',0x202B)
@_f
@_p.types(_cs.BOOL,_cs.HDC,ctypes.POINTER(_cs.c_int),ctypes.POINTER(_cs.FLOAT),_cs.UINT,ctypes.POINTER(_cs.c_int),ctypes.POINTER(_cs.UINT))
def wglChoosePixelFormatARB(hdc,piAttribIList,pfAttribFList,nMaxFormats,piFormats,nNumFormats):pass
@_f
@_p.types(_cs.BOOL,_cs.HDC,_cs.c_int,_cs.c_int,_cs.UINT,ctypes.POINTER(_cs.c_int),ctypes.POINTER(_cs.FLOAT))
def wglGetPixelFormatAttribfvARB(hdc,iPixelFormat,iLayerPlane,nAttributes,piAttributes,pfValues):pass
@_f
@_p.types(_cs.BOOL,_cs.HDC,_cs.c_int,_cs.c_int,_cs.UINT,ctypes.POINTER(_cs.c_int),ctypes.POINTER(_cs.c_int))
def wglGetPixelFormatAttribivARB(hdc,iPixelFormat,iLayerPlane,nAttributes,piAttributes,piValues):pass
