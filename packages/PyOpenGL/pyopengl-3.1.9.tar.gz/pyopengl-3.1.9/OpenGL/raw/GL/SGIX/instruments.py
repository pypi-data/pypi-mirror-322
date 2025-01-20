'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_SGIX_instruments'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_SGIX_instruments',error_checker=_errors._error_checker)
GL_INSTRUMENT_BUFFER_POINTER_SGIX=_C('GL_INSTRUMENT_BUFFER_POINTER_SGIX',0x8180)
GL_INSTRUMENT_MEASUREMENTS_SGIX=_C('GL_INSTRUMENT_MEASUREMENTS_SGIX',0x8181)
@_f
@_p.types(_cs.GLint,)
def glGetInstrumentsSGIX():pass
@_f
@_p.types(None,_cs.GLsizei,arrays.GLintArray)
def glInstrumentsBufferSGIX(size,buffer):pass
@_f
@_p.types(_cs.GLint,arrays.GLintArray)
def glPollInstrumentsSGIX(marker_p):pass
@_f
@_p.types(None,_cs.GLint)
def glReadInstrumentsSGIX(marker):pass
@_f
@_p.types(None,)
def glStartInstrumentsSGIX():pass
@_f
@_p.types(None,_cs.GLint)
def glStopInstrumentsSGIX(marker):pass
