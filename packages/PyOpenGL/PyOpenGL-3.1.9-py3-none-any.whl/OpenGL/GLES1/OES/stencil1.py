'''OpenGL extension OES.stencil1

This module customises the behaviour of the 
OpenGL.raw.GLES1.OES.stencil1 to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension enables 1-bit stencil component as a valid
	render buffer storage format.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/OES/stencil1.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES1 import _types, _glgets
from OpenGL.raw.GLES1.OES.stencil1 import *
from OpenGL.raw.GLES1.OES.stencil1 import _EXTENSION_NAME

def glInitStencil1OES():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION