'''OpenGL extension ARB.transpose_matrix

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.transpose_matrix to provide a more 
Python-friendly API

Overview (from the spec)
	
	New functions and tokens are added allowing application matrices
	stored in row major order rather than column major order to be
	transferred to the OpenGL implementation.  This allows an application
	to use standard C-language 2-dimensional arrays (m[row][col]) and
	have the array indices match the expected matrix row and column indexes.
	These arrays are referred to as transpose matrices since they are
	the transpose of the standard matrices passed to OpenGL.
	
	This extension adds an interface for transfering data to and from the
	OpenGL pipeline, it does not change any OpenGL processing or imply any
	changes in state representation.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/transpose_matrix.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.ARB.transpose_matrix import *
from OpenGL.raw.GL.ARB.transpose_matrix import _EXTENSION_NAME

def glInitTransposeMatrixARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

glLoadTransposeMatrixfARB=wrapper.wrapper(glLoadTransposeMatrixfARB).setInputArraySize(
    'm', 16
)
glLoadTransposeMatrixdARB=wrapper.wrapper(glLoadTransposeMatrixdARB).setInputArraySize(
    'm', 16
)
glMultTransposeMatrixfARB=wrapper.wrapper(glMultTransposeMatrixfARB).setInputArraySize(
    'm', 16
)
glMultTransposeMatrixdARB=wrapper.wrapper(glMultTransposeMatrixdARB).setInputArraySize(
    'm', 16
)
### END AUTOGENERATED SECTION
