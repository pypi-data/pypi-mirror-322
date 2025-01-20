'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ARB_compute_shader'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ARB_compute_shader',error_checker=_errors._error_checker)
GL_ATOMIC_COUNTER_BUFFER_REFERENCED_BY_COMPUTE_SHADER=_C('GL_ATOMIC_COUNTER_BUFFER_REFERENCED_BY_COMPUTE_SHADER',0x90ED)
GL_COMPUTE_SHADER=_C('GL_COMPUTE_SHADER',0x91B9)
GL_COMPUTE_SHADER_BIT=_C('GL_COMPUTE_SHADER_BIT',0x00000020)
GL_COMPUTE_WORK_GROUP_SIZE=_C('GL_COMPUTE_WORK_GROUP_SIZE',0x8267)
GL_DISPATCH_INDIRECT_BUFFER=_C('GL_DISPATCH_INDIRECT_BUFFER',0x90EE)
GL_DISPATCH_INDIRECT_BUFFER_BINDING=_C('GL_DISPATCH_INDIRECT_BUFFER_BINDING',0x90EF)
GL_MAX_COMBINED_COMPUTE_UNIFORM_COMPONENTS=_C('GL_MAX_COMBINED_COMPUTE_UNIFORM_COMPONENTS',0x8266)
GL_MAX_COMPUTE_ATOMIC_COUNTERS=_C('GL_MAX_COMPUTE_ATOMIC_COUNTERS',0x8265)
GL_MAX_COMPUTE_ATOMIC_COUNTER_BUFFERS=_C('GL_MAX_COMPUTE_ATOMIC_COUNTER_BUFFERS',0x8264)
GL_MAX_COMPUTE_IMAGE_UNIFORMS=_C('GL_MAX_COMPUTE_IMAGE_UNIFORMS',0x91BD)
GL_MAX_COMPUTE_SHARED_MEMORY_SIZE=_C('GL_MAX_COMPUTE_SHARED_MEMORY_SIZE',0x8262)
GL_MAX_COMPUTE_TEXTURE_IMAGE_UNITS=_C('GL_MAX_COMPUTE_TEXTURE_IMAGE_UNITS',0x91BC)
GL_MAX_COMPUTE_UNIFORM_BLOCKS=_C('GL_MAX_COMPUTE_UNIFORM_BLOCKS',0x91BB)
GL_MAX_COMPUTE_UNIFORM_COMPONENTS=_C('GL_MAX_COMPUTE_UNIFORM_COMPONENTS',0x8263)
GL_MAX_COMPUTE_WORK_GROUP_COUNT=_C('GL_MAX_COMPUTE_WORK_GROUP_COUNT',0x91BE)
GL_MAX_COMPUTE_WORK_GROUP_INVOCATIONS=_C('GL_MAX_COMPUTE_WORK_GROUP_INVOCATIONS',0x90EB)
GL_MAX_COMPUTE_WORK_GROUP_SIZE=_C('GL_MAX_COMPUTE_WORK_GROUP_SIZE',0x91BF)
GL_UNIFORM_BLOCK_REFERENCED_BY_COMPUTE_SHADER=_C('GL_UNIFORM_BLOCK_REFERENCED_BY_COMPUTE_SHADER',0x90EC)
@_f
@_p.types(None,_cs.GLuint,_cs.GLuint,_cs.GLuint)
def glDispatchCompute(num_groups_x,num_groups_y,num_groups_z):pass
@_f
@_p.types(None,_cs.GLintptr)
def glDispatchComputeIndirect(indirect):pass
