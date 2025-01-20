'''OpenGL extension I3D.gamma

This module customises the behaviour of the 
OpenGL.raw.WGL.I3D.gamma to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/I3D/gamma.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.WGL import _types, _glgets
from OpenGL.raw.WGL.I3D.gamma import *
from OpenGL.raw.WGL.I3D.gamma import _EXTENSION_NAME

def glInitGammaI3D():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION