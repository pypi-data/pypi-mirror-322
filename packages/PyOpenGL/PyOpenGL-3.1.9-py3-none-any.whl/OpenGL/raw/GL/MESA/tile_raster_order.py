'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_MESA_tile_raster_order'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_MESA_tile_raster_order',error_checker=_errors._error_checker)
GL_TILE_RASTER_ORDER_FIXED_MESA=_C('GL_TILE_RASTER_ORDER_FIXED_MESA',0x8BB8)
GL_TILE_RASTER_ORDER_INCREASING_X_MESA=_C('GL_TILE_RASTER_ORDER_INCREASING_X_MESA',0x8BB9)
GL_TILE_RASTER_ORDER_INCREASING_Y_MESA=_C('GL_TILE_RASTER_ORDER_INCREASING_Y_MESA',0x8BBA)

