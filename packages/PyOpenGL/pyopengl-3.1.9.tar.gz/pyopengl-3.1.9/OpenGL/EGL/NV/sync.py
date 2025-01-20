'''OpenGL extension NV.sync

This module customises the behaviour of the 
OpenGL.raw.EGL.NV.sync to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/sync.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.EGL import _types, _glgets
from OpenGL.raw.EGL.NV.sync import *
from OpenGL.raw.EGL.NV.sync import _EXTENSION_NAME

def glInitSyncNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION