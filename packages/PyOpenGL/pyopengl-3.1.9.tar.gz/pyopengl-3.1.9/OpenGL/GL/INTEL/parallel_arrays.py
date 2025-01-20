'''OpenGL extension INTEL.parallel_arrays

This module customises the behaviour of the 
OpenGL.raw.GL.INTEL.parallel_arrays to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension adds the ability to format vertex arrays in a way that's 

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/INTEL/parallel_arrays.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.INTEL.parallel_arrays import *
from OpenGL.raw.GL.INTEL.parallel_arrays import _EXTENSION_NAME

def glInitParallelArraysINTEL():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

glVertexPointervINTEL=wrapper.wrapper(glVertexPointervINTEL).setInputArraySize(
    'pointer', 4
)
glNormalPointervINTEL=wrapper.wrapper(glNormalPointervINTEL).setInputArraySize(
    'pointer', 4
)
glColorPointervINTEL=wrapper.wrapper(glColorPointervINTEL).setInputArraySize(
    'pointer', 4
)
glTexCoordPointervINTEL=wrapper.wrapper(glTexCoordPointervINTEL).setInputArraySize(
    'pointer', 4
)
### END AUTOGENERATED SECTION