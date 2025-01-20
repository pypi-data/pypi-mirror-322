'''OpenGL extension EXT.pbuffer

This module customises the behaviour of the 
OpenGL.raw.WGL.EXT.pbuffer to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/pbuffer.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.WGL import _types, _glgets
from OpenGL.raw.WGL.EXT.pbuffer import *
from OpenGL.raw.WGL.EXT.pbuffer import _EXTENSION_NAME

def glInitPbufferEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION