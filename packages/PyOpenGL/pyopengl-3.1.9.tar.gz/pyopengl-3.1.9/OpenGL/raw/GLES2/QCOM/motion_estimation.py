'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLES2 import _types as _cs
# End users want this...
from OpenGL.raw.GLES2._types import *
from OpenGL.raw.GLES2 import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLES2_QCOM_motion_estimation'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLES2,'GLES2_QCOM_motion_estimation',error_checker=_errors._error_checker)
GL_FOVEATION_SCALED_BIN_METHOD_BIT_QCOM=_C('GL_FOVEATION_SCALED_BIN_METHOD_BIT_QCOM',0x00000002)
GL_MOTION_ESTIMATION_SEARCH_BLOCK_X_QCOM=_C('GL_MOTION_ESTIMATION_SEARCH_BLOCK_X_QCOM',0x8C90)
GL_MOTION_ESTIMATION_SEARCH_BLOCK_Y_QCOM=_C('GL_MOTION_ESTIMATION_SEARCH_BLOCK_Y_QCOM',0x8C91)
@_f
@_p.types(None,_cs.GLuint,_cs.GLuint,_cs.GLuint)
def glTexEstimateMotionQCOM(ref,target,output):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLuint,_cs.GLuint,_cs.GLuint)
def glTexEstimateMotionRegionsQCOM(ref,target,output,mask):pass
