'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ARB_vertex_shader'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ARB_vertex_shader',error_checker=_errors._error_checker)
GL_CURRENT_VERTEX_ATTRIB_ARB=_C('GL_CURRENT_VERTEX_ATTRIB_ARB',0x8626)
GL_FLOAT=_C('GL_FLOAT',0x1406)
GL_FLOAT_MAT2_ARB=_C('GL_FLOAT_MAT2_ARB',0x8B5A)
GL_FLOAT_MAT3_ARB=_C('GL_FLOAT_MAT3_ARB',0x8B5B)
GL_FLOAT_MAT4_ARB=_C('GL_FLOAT_MAT4_ARB',0x8B5C)
GL_FLOAT_VEC2_ARB=_C('GL_FLOAT_VEC2_ARB',0x8B50)
GL_FLOAT_VEC3_ARB=_C('GL_FLOAT_VEC3_ARB',0x8B51)
GL_FLOAT_VEC4_ARB=_C('GL_FLOAT_VEC4_ARB',0x8B52)
GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS_ARB=_C('GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS_ARB',0x8B4D)
GL_MAX_TEXTURE_COORDS_ARB=_C('GL_MAX_TEXTURE_COORDS_ARB',0x8871)
GL_MAX_TEXTURE_IMAGE_UNITS_ARB=_C('GL_MAX_TEXTURE_IMAGE_UNITS_ARB',0x8872)
GL_MAX_VARYING_FLOATS_ARB=_C('GL_MAX_VARYING_FLOATS_ARB',0x8B4B)
GL_MAX_VERTEX_ATTRIBS_ARB=_C('GL_MAX_VERTEX_ATTRIBS_ARB',0x8869)
GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS_ARB=_C('GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS_ARB',0x8B4C)
GL_MAX_VERTEX_UNIFORM_COMPONENTS_ARB=_C('GL_MAX_VERTEX_UNIFORM_COMPONENTS_ARB',0x8B4A)
GL_OBJECT_ACTIVE_ATTRIBUTES_ARB=_C('GL_OBJECT_ACTIVE_ATTRIBUTES_ARB',0x8B89)
GL_OBJECT_ACTIVE_ATTRIBUTE_MAX_LENGTH_ARB=_C('GL_OBJECT_ACTIVE_ATTRIBUTE_MAX_LENGTH_ARB',0x8B8A)
GL_VERTEX_ATTRIB_ARRAY_ENABLED_ARB=_C('GL_VERTEX_ATTRIB_ARRAY_ENABLED_ARB',0x8622)
GL_VERTEX_ATTRIB_ARRAY_NORMALIZED_ARB=_C('GL_VERTEX_ATTRIB_ARRAY_NORMALIZED_ARB',0x886A)
GL_VERTEX_ATTRIB_ARRAY_POINTER_ARB=_C('GL_VERTEX_ATTRIB_ARRAY_POINTER_ARB',0x8645)
GL_VERTEX_ATTRIB_ARRAY_SIZE_ARB=_C('GL_VERTEX_ATTRIB_ARRAY_SIZE_ARB',0x8623)
GL_VERTEX_ATTRIB_ARRAY_STRIDE_ARB=_C('GL_VERTEX_ATTRIB_ARRAY_STRIDE_ARB',0x8624)
GL_VERTEX_ATTRIB_ARRAY_TYPE_ARB=_C('GL_VERTEX_ATTRIB_ARRAY_TYPE_ARB',0x8625)
GL_VERTEX_PROGRAM_POINT_SIZE_ARB=_C('GL_VERTEX_PROGRAM_POINT_SIZE_ARB',0x8642)
GL_VERTEX_PROGRAM_TWO_SIDE_ARB=_C('GL_VERTEX_PROGRAM_TWO_SIDE_ARB',0x8643)
GL_VERTEX_SHADER_ARB=_C('GL_VERTEX_SHADER_ARB',0x8B31)
@_f
@_p.types(None,_cs.GLhandleARB,_cs.GLuint,arrays.GLcharARBArray)
def glBindAttribLocationARB(programObj,index,name):pass
@_f
@_p.types(None,_cs.GLuint)
def glDisableVertexAttribArrayARB(index):pass
@_f
@_p.types(None,_cs.GLuint)
def glEnableVertexAttribArrayARB(index):pass
@_f
@_p.types(None,_cs.GLhandleARB,_cs.GLuint,_cs.GLsizei,arrays.GLsizeiArray,arrays.GLintArray,arrays.GLuintArray,arrays.GLcharARBArray)
def glGetActiveAttribARB(programObj,index,maxLength,length,size,type,name):pass
@_f
@_p.types(_cs.GLint,_cs.GLhandleARB,arrays.GLcharARBArray)
def glGetAttribLocationARB(programObj,name):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,arrays.GLvoidpArray)
def glGetVertexAttribPointervARB(index,pname,pointer):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,arrays.GLdoubleArray)
def glGetVertexAttribdvARB(index,pname,params):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,arrays.GLfloatArray)
def glGetVertexAttribfvARB(index,pname,params):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,arrays.GLintArray)
def glGetVertexAttribivARB(index,pname,params):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLdouble)
def glVertexAttrib1dARB(index,x):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLdoubleArray)
def glVertexAttrib1dvARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLfloat)
def glVertexAttrib1fARB(index,x):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLfloatArray)
def glVertexAttrib1fvARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLshort)
def glVertexAttrib1sARB(index,x):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLshortArray)
def glVertexAttrib1svARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLdouble,_cs.GLdouble)
def glVertexAttrib2dARB(index,x,y):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLdoubleArray)
def glVertexAttrib2dvARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLfloat,_cs.GLfloat)
def glVertexAttrib2fARB(index,x,y):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLfloatArray)
def glVertexAttrib2fvARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLshort,_cs.GLshort)
def glVertexAttrib2sARB(index,x,y):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLshortArray)
def glVertexAttrib2svARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLdouble,_cs.GLdouble,_cs.GLdouble)
def glVertexAttrib3dARB(index,x,y,z):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLdoubleArray)
def glVertexAttrib3dvARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLfloat,_cs.GLfloat,_cs.GLfloat)
def glVertexAttrib3fARB(index,x,y,z):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLfloatArray)
def glVertexAttrib3fvARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLshort,_cs.GLshort,_cs.GLshort)
def glVertexAttrib3sARB(index,x,y,z):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLshortArray)
def glVertexAttrib3svARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLbyteArray)
def glVertexAttrib4NbvARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLintArray)
def glVertexAttrib4NivARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLshortArray)
def glVertexAttrib4NsvARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLubyte,_cs.GLubyte,_cs.GLubyte,_cs.GLubyte)
def glVertexAttrib4NubARB(index,x,y,z,w):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLubyteArray)
def glVertexAttrib4NubvARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLuintArray)
def glVertexAttrib4NuivARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLushortArray)
def glVertexAttrib4NusvARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLbyteArray)
def glVertexAttrib4bvARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLdouble,_cs.GLdouble,_cs.GLdouble,_cs.GLdouble)
def glVertexAttrib4dARB(index,x,y,z,w):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLdoubleArray)
def glVertexAttrib4dvARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLfloat,_cs.GLfloat,_cs.GLfloat,_cs.GLfloat)
def glVertexAttrib4fARB(index,x,y,z,w):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLfloatArray)
def glVertexAttrib4fvARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLintArray)
def glVertexAttrib4ivARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLshort,_cs.GLshort,_cs.GLshort,_cs.GLshort)
def glVertexAttrib4sARB(index,x,y,z,w):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLshortArray)
def glVertexAttrib4svARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLubyteArray)
def glVertexAttrib4ubvARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLuintArray)
def glVertexAttrib4uivARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,arrays.GLushortArray)
def glVertexAttrib4usvARB(index,v):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLint,_cs.GLenum,_cs.GLboolean,_cs.GLsizei,ctypes.c_void_p)
def glVertexAttribPointerARB(index,size,type,normalized,stride,pointer):pass
