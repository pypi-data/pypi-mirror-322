'''OpenGL extension ARB.create_context_no_error

This module customises the behaviour of the 
OpenGL.raw.WGL.ARB.create_context_no_error to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension allows the creation of an OpenGL or OpenGL ES context that
	doesn't generate errors if the context supports a no error mode.  The
	implications of this feature are discussed in the GL_KHR_no_error
	extension.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/create_context_no_error.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.WGL import _types, _glgets
from OpenGL.raw.WGL.ARB.create_context_no_error import *
from OpenGL.raw.WGL.ARB.create_context_no_error import _EXTENSION_NAME

def glInitCreateContextNoErrorARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION