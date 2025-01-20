'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_NVX_gpu_memory_info'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_NVX_gpu_memory_info',error_checker=_errors._error_checker)
GL_GPU_MEMORY_INFO_CURRENT_AVAILABLE_VIDMEM_NVX=_C('GL_GPU_MEMORY_INFO_CURRENT_AVAILABLE_VIDMEM_NVX',0x9049)
GL_GPU_MEMORY_INFO_DEDICATED_VIDMEM_NVX=_C('GL_GPU_MEMORY_INFO_DEDICATED_VIDMEM_NVX',0x9047)
GL_GPU_MEMORY_INFO_EVICTED_MEMORY_NVX=_C('GL_GPU_MEMORY_INFO_EVICTED_MEMORY_NVX',0x904B)
GL_GPU_MEMORY_INFO_EVICTION_COUNT_NVX=_C('GL_GPU_MEMORY_INFO_EVICTION_COUNT_NVX',0x904A)
GL_GPU_MEMORY_INFO_TOTAL_AVAILABLE_MEMORY_NVX=_C('GL_GPU_MEMORY_INFO_TOTAL_AVAILABLE_MEMORY_NVX',0x9048)

