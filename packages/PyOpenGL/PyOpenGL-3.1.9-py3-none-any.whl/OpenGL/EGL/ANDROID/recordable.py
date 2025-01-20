'''OpenGL extension ANDROID.recordable

This module customises the behaviour of the 
OpenGL.raw.EGL.ANDROID.recordable to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ANDROID/recordable.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.EGL import _types, _glgets
from OpenGL.raw.EGL.ANDROID.recordable import *
from OpenGL.raw.EGL.ANDROID.recordable import _EXTENSION_NAME

def glInitRecordableANDROID():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION