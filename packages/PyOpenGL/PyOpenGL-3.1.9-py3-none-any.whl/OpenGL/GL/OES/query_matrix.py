'''OpenGL extension OES.query_matrix

This module customises the behaviour of the 
OpenGL.raw.GL.OES.query_matrix to provide a more 
Python-friendly API

Overview (from the spec)
	
	Many applications may need to query the contents and status of the
	current matrix at least for debugging purposes, especially as the
	implementations are allowed to implement matrix machinery either in
	any (possibly proprietary) floating point format, or in a fixed point
	format that has the range and accuracy of at least 16.16 (signed 16 bit
	integer part, unsigned 16 bit fractional part).
	
	This extension is intended to allow application to query the components
	of the matrix and also their status, regardless whether the internal
	representation is in fixed point or floating point.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/OES/query_matrix.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.OES.query_matrix import *
from OpenGL.raw.GL.OES.query_matrix import _EXTENSION_NAME

def glInitQueryMatrixOES():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

glQueryMatrixxOES=wrapper.wrapper(glQueryMatrixxOES).setOutput(
    'exponent',size=(16,),orPassIn=True
).setOutput(
    'mantissa',size=(16,),orPassIn=True
)
### END AUTOGENERATED SECTION