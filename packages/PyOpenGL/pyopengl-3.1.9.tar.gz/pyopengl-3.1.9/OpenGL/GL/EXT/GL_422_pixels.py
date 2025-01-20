'''OpenGL extension EXT.GL_422_pixels

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.GL_422_pixels to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension provides support for converting 422 pixels in host
	memory to 444 pixels as part of the pixel storage operation.
	
	The pixel unpack storage operation treats a 422 pixel as a 2 element
	format where the first element is C (chrominance) and the second
	element is L (luminance). Luminance is present on all pixels; a full
	chrominance value requires two pixels.
	
	The pixel pack storage operation converts RGB to a 422 pixel defined as
	a 2 element format where the first element stored is C (chrominance)
	and the second element stored is L (luminance).  Luminance is present
	on all pixels; a full chrominance value requires two pixels.
	
	Both averaging and non-averaging is supported for green and blue
	assignments for pack and unpack operations.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/GL_422_pixels.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.EXT.GL_422_pixels import *
from OpenGL.raw.GL.EXT.GL_422_pixels import _EXTENSION_NAME

def glInitGl422PixelsEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION