'''OpenGL extension IMG.program_binary

This module customises the behaviour of the 
OpenGL.raw.GLES2.IMG.program_binary to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension makes available a program binary format, SGX_PROGRAM_BINARY_IMG.
	It enables retrieving and loading of pre-linked program objects on chips designed 
	by Imagination Technologies. 

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/IMG/program_binary.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.IMG.program_binary import *
from OpenGL.raw.GLES2.IMG.program_binary import _EXTENSION_NAME

def glInitProgramBinaryIMG():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION