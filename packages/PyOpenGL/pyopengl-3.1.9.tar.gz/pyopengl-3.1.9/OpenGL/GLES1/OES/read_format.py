'''OpenGL extension OES.read_format

This module customises the behaviour of the 
OpenGL.raw.GLES1.OES.read_format to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension provides the capability to query an OpenGL
	implementation for a preferred type and format combination
	for use with reading the color buffer with the ReadPixels
	command.  The purpose is to enable embedded implementations
	to support a greatly reduced set of type/format combinations
	and provide a mechanism for applications to determine which
	implementation-specific combination is supported.
	
	The preferred type and format combination returned may depend
	on the read surface bound to the current GL context.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/OES/read_format.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES1 import _types, _glgets
from OpenGL.raw.GLES1.OES.read_format import *
from OpenGL.raw.GLES1.OES.read_format import _EXTENSION_NAME

def glInitReadFormatOES():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION