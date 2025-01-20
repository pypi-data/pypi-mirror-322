'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLES2 import _types as _cs
# End users want this...
from OpenGL.raw.GLES2._types import *
from OpenGL.raw.GLES2 import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLES2_EXT_memory_object'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLES2,'GLES2_EXT_memory_object',error_checker=_errors._error_checker)
GL_DEDICATED_MEMORY_OBJECT_EXT=_C('GL_DEDICATED_MEMORY_OBJECT_EXT',0x9581)
GL_DEVICE_UUID_EXT=_C('GL_DEVICE_UUID_EXT',0x9597)
GL_DRIVER_UUID_EXT=_C('GL_DRIVER_UUID_EXT',0x9598)
GL_LINEAR_TILING_EXT=_C('GL_LINEAR_TILING_EXT',0x9585)
GL_NUM_DEVICE_UUIDS_EXT=_C('GL_NUM_DEVICE_UUIDS_EXT',0x9596)
GL_NUM_TILING_TYPES_EXT=_C('GL_NUM_TILING_TYPES_EXT',0x9582)
GL_OPTIMAL_TILING_EXT=_C('GL_OPTIMAL_TILING_EXT',0x9584)
GL_PROTECTED_MEMORY_OBJECT_EXT=_C('GL_PROTECTED_MEMORY_OBJECT_EXT',0x959B)
GL_TEXTURE_TILING_EXT=_C('GL_TEXTURE_TILING_EXT',0x9580)
GL_TILING_TYPES_EXT=_C('GL_TILING_TYPES_EXT',0x9583)
GL_UUID_SIZE_EXT=_C('GL_UUID_SIZE_EXT',16)
@_f
@_p.types(None,_cs.GLenum,_cs.GLsizeiptr,_cs.GLuint,_cs.GLuint64)
def glBufferStorageMemEXT(target,size,memory,offset):pass
@_f
@_p.types(None,_cs.GLsizei,arrays.GLuintArray)
def glCreateMemoryObjectsEXT(n,memoryObjects):pass
@_f
@_p.types(None,_cs.GLsizei,arrays.GLuintArray)
def glDeleteMemoryObjectsEXT(n,memoryObjects):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,arrays.GLintArray)
def glGetMemoryObjectParameterivEXT(memoryObject,pname,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,arrays.GLubyteArray)
def glGetUnsignedBytei_vEXT(target,index,data):pass
@_f
@_p.types(None,_cs.GLenum,arrays.GLubyteArray)
def glGetUnsignedBytevEXT(pname,data):pass
@_f
@_p.types(_cs.GLboolean,_cs.GLuint)
def glIsMemoryObjectEXT(memoryObject):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,arrays.GLintArray)
def glMemoryObjectParameterivEXT(memoryObject,pname,params):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLsizeiptr,_cs.GLuint,_cs.GLuint64)
def glNamedBufferStorageMemEXT(buffer,size,memory,offset):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLsizei,_cs.GLenum,_cs.GLsizei,_cs.GLuint,_cs.GLuint64)
def glTexStorageMem1DEXT(target,levels,internalFormat,width,memory,offset):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLsizei,_cs.GLenum,_cs.GLsizei,_cs.GLsizei,_cs.GLuint,_cs.GLuint64)
def glTexStorageMem2DEXT(target,levels,internalFormat,width,height,memory,offset):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLsizei,_cs.GLenum,_cs.GLsizei,_cs.GLsizei,_cs.GLboolean,_cs.GLuint,_cs.GLuint64)
def glTexStorageMem2DMultisampleEXT(target,samples,internalFormat,width,height,fixedSampleLocations,memory,offset):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLsizei,_cs.GLenum,_cs.GLsizei,_cs.GLsizei,_cs.GLsizei,_cs.GLuint,_cs.GLuint64)
def glTexStorageMem3DEXT(target,levels,internalFormat,width,height,depth,memory,offset):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLsizei,_cs.GLenum,_cs.GLsizei,_cs.GLsizei,_cs.GLsizei,_cs.GLboolean,_cs.GLuint,_cs.GLuint64)
def glTexStorageMem3DMultisampleEXT(target,samples,internalFormat,width,height,depth,fixedSampleLocations,memory,offset):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLsizei,_cs.GLenum,_cs.GLsizei,_cs.GLuint,_cs.GLuint64)
def glTextureStorageMem1DEXT(texture,levels,internalFormat,width,memory,offset):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLsizei,_cs.GLenum,_cs.GLsizei,_cs.GLsizei,_cs.GLuint,_cs.GLuint64)
def glTextureStorageMem2DEXT(texture,levels,internalFormat,width,height,memory,offset):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLsizei,_cs.GLenum,_cs.GLsizei,_cs.GLsizei,_cs.GLboolean,_cs.GLuint,_cs.GLuint64)
def glTextureStorageMem2DMultisampleEXT(texture,samples,internalFormat,width,height,fixedSampleLocations,memory,offset):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLsizei,_cs.GLenum,_cs.GLsizei,_cs.GLsizei,_cs.GLsizei,_cs.GLuint,_cs.GLuint64)
def glTextureStorageMem3DEXT(texture,levels,internalFormat,width,height,depth,memory,offset):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLsizei,_cs.GLenum,_cs.GLsizei,_cs.GLsizei,_cs.GLsizei,_cs.GLboolean,_cs.GLuint,_cs.GLuint64)
def glTextureStorageMem3DMultisampleEXT(texture,samples,internalFormat,width,height,depth,fixedSampleLocations,memory,offset):pass
