'''OpenGL extension IMG.texture_filter_cubic

This module customises the behaviour of the 
OpenGL.raw.GLES2.IMG.texture_filter_cubic to provide a more 
Python-friendly API

Overview (from the spec)
	
	OpenGL ES provides two sampling methods available; nearest neighbor or
	linear filtering, with optional MIP Map sampling modes added to move between
	differently sized textures when downsampling.
	
	This extension adds an additional, high quality cubic filtering mode, using
	a Catmull-Rom bicubic filter. Performing this kind of filtering can be done
	in a shader by using 16 samples, but this can be inefficient. The cubic
	filter mode exposes an optimized high quality texture sampling using fixed
	functionality.
	
	This extension affects the way textures are sampled, by modifying the way
	texels within the same MIP-Map level are sampled and resolved. It does not
	affect MIP-Map filtering, which is still limited to linear or nearest.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/IMG/texture_filter_cubic.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.IMG.texture_filter_cubic import *
from OpenGL.raw.GLES2.IMG.texture_filter_cubic import _EXTENSION_NAME

def glInitTextureFilterCubicIMG():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION