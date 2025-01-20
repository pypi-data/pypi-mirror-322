'''OpenGL extension APPLE.clip_distance

This module customises the behaviour of the 
OpenGL.raw.GLES2.APPLE.clip_distance to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension adds support for hardware clip planes to OpenGL ES 2.0
	and 3.0.  These were present in OpenGL ES 1.1, but were removed to
	better match certain hardware.  Since they're useful for certain
	applications, notable CAD, we return them here.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/APPLE/clip_distance.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.APPLE.clip_distance import *
from OpenGL.raw.GLES2.APPLE.clip_distance import _EXTENSION_NAME

def glInitClipDistanceAPPLE():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION