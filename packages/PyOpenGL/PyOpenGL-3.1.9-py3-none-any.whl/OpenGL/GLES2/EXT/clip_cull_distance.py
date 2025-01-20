'''OpenGL extension EXT.clip_cull_distance

This module customises the behaviour of the 
OpenGL.raw.GLES2.EXT.clip_cull_distance to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension adds support for hardware clip planes and cull
	distances to OpenGL ES. The language for this extension is based
	on the OpenGL 4.5 API Specification (May 28, 2015) and
	ARB_clip_distance.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/clip_cull_distance.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.EXT.clip_cull_distance import *
from OpenGL.raw.GLES2.EXT.clip_cull_distance import _EXTENSION_NAME

def glInitClipCullDistanceEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION