'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_EXT_memory_object_win32'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_EXT_memory_object_win32',error_checker=_errors._error_checker)
GL_DEVICE_LUID_EXT=_C('GL_DEVICE_LUID_EXT',0x9599)
GL_DEVICE_NODE_MASK_EXT=_C('GL_DEVICE_NODE_MASK_EXT',0x959A)
GL_HANDLE_TYPE_D3D11_IMAGE_EXT=_C('GL_HANDLE_TYPE_D3D11_IMAGE_EXT',0x958B)
GL_HANDLE_TYPE_D3D11_IMAGE_KMT_EXT=_C('GL_HANDLE_TYPE_D3D11_IMAGE_KMT_EXT',0x958C)
GL_HANDLE_TYPE_D3D12_RESOURCE_EXT=_C('GL_HANDLE_TYPE_D3D12_RESOURCE_EXT',0x958A)
GL_HANDLE_TYPE_D3D12_TILEPOOL_EXT=_C('GL_HANDLE_TYPE_D3D12_TILEPOOL_EXT',0x9589)
GL_HANDLE_TYPE_OPAQUE_WIN32_EXT=_C('GL_HANDLE_TYPE_OPAQUE_WIN32_EXT',0x9587)
GL_HANDLE_TYPE_OPAQUE_WIN32_KMT_EXT=_C('GL_HANDLE_TYPE_OPAQUE_WIN32_KMT_EXT',0x9588)
GL_LUID_SIZE_EXT=_C('GL_LUID_SIZE_EXT',8)
@_f
@_p.types(None,_cs.GLuint,_cs.GLuint64,_cs.GLenum,ctypes.c_void_p)
def glImportMemoryWin32HandleEXT(memory,size,handleType,handle):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLuint64,_cs.GLenum,ctypes.c_void_p)
def glImportMemoryWin32NameEXT(memory,size,handleType,name):pass
