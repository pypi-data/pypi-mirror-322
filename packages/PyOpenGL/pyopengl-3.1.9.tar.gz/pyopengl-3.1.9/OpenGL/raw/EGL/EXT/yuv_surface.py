'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.EGL import _types as _cs
# End users want this...
from OpenGL.raw.EGL._types import *
from OpenGL.raw.EGL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'EGL_EXT_yuv_surface'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.EGL,'EGL_EXT_yuv_surface',error_checker=_errors._error_checker)
EGL_YUV_BUFFER_EXT=_C('EGL_YUV_BUFFER_EXT',0x3300)
EGL_YUV_CSC_STANDARD_2020_EXT=_C('EGL_YUV_CSC_STANDARD_2020_EXT',0x330D)
EGL_YUV_CSC_STANDARD_601_EXT=_C('EGL_YUV_CSC_STANDARD_601_EXT',0x330B)
EGL_YUV_CSC_STANDARD_709_EXT=_C('EGL_YUV_CSC_STANDARD_709_EXT',0x330C)
EGL_YUV_CSC_STANDARD_EXT=_C('EGL_YUV_CSC_STANDARD_EXT',0x330A)
EGL_YUV_DEPTH_RANGE_EXT=_C('EGL_YUV_DEPTH_RANGE_EXT',0x3317)
EGL_YUV_DEPTH_RANGE_FULL_EXT=_C('EGL_YUV_DEPTH_RANGE_FULL_EXT',0x3319)
EGL_YUV_DEPTH_RANGE_LIMITED_EXT=_C('EGL_YUV_DEPTH_RANGE_LIMITED_EXT',0x3318)
EGL_YUV_NUMBER_OF_PLANES_EXT=_C('EGL_YUV_NUMBER_OF_PLANES_EXT',0x3311)
EGL_YUV_ORDER_AYUV_EXT=_C('EGL_YUV_ORDER_AYUV_EXT',0x3308)
EGL_YUV_ORDER_EXT=_C('EGL_YUV_ORDER_EXT',0x3301)
EGL_YUV_ORDER_UYVY_EXT=_C('EGL_YUV_ORDER_UYVY_EXT',0x3305)
EGL_YUV_ORDER_VYUY_EXT=_C('EGL_YUV_ORDER_VYUY_EXT',0x3307)
EGL_YUV_ORDER_YUV_EXT=_C('EGL_YUV_ORDER_YUV_EXT',0x3302)
EGL_YUV_ORDER_YUYV_EXT=_C('EGL_YUV_ORDER_YUYV_EXT',0x3304)
EGL_YUV_ORDER_YVU_EXT=_C('EGL_YUV_ORDER_YVU_EXT',0x3303)
EGL_YUV_ORDER_YVYU_EXT=_C('EGL_YUV_ORDER_YVYU_EXT',0x3306)
EGL_YUV_PLANE_BPP_0_EXT=_C('EGL_YUV_PLANE_BPP_0_EXT',0x331B)
EGL_YUV_PLANE_BPP_10_EXT=_C('EGL_YUV_PLANE_BPP_10_EXT',0x331D)
EGL_YUV_PLANE_BPP_8_EXT=_C('EGL_YUV_PLANE_BPP_8_EXT',0x331C)
EGL_YUV_PLANE_BPP_EXT=_C('EGL_YUV_PLANE_BPP_EXT',0x331A)
EGL_YUV_SUBSAMPLE_4_2_0_EXT=_C('EGL_YUV_SUBSAMPLE_4_2_0_EXT',0x3313)
EGL_YUV_SUBSAMPLE_4_2_2_EXT=_C('EGL_YUV_SUBSAMPLE_4_2_2_EXT',0x3314)
EGL_YUV_SUBSAMPLE_4_4_4_EXT=_C('EGL_YUV_SUBSAMPLE_4_4_4_EXT',0x3315)
EGL_YUV_SUBSAMPLE_EXT=_C('EGL_YUV_SUBSAMPLE_EXT',0x3312)

