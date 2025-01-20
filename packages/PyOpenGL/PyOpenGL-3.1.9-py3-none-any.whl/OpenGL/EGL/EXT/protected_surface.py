'''OpenGL extension EXT.protected_surface

This module customises the behaviour of the 
OpenGL.raw.EGL.EXT.protected_surface to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/protected_surface.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.EGL import _types, _glgets
from OpenGL.raw.EGL.EXT.protected_surface import *
from OpenGL.raw.EGL.EXT.protected_surface import _EXTENSION_NAME

def glInitProtectedSurfaceEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION