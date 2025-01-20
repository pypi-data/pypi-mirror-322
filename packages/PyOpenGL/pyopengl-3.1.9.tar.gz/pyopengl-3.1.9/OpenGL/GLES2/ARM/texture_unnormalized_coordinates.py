'''OpenGL extension ARM.texture_unnormalized_coordinates

This module customises the behaviour of the 
OpenGL.raw.GLES2.ARM.texture_unnormalized_coordinates to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension provides the option to switch to unnormalized
	coordinates for texture lookups using a sampler parameter.
	
	Texture lookup in OpenGL ES is done using normalized coordinates. For
	certain applications it is convenient to work with non-normalized
	coordinates instead. It also beneficial to keep support for bilinear
	filtering.
	
	Additional restrictions apply to textures with non-normalized
	coordinates that affect texture completeness and the available
	texture lookup functions.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARM/texture_unnormalized_coordinates.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.ARM.texture_unnormalized_coordinates import *
from OpenGL.raw.GLES2.ARM.texture_unnormalized_coordinates import _EXTENSION_NAME

def glInitTextureUnnormalizedCoordinatesARM():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION