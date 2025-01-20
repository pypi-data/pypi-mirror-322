'''OpenGL extension SUN.global_alpha

This module customises the behaviour of the 
OpenGL.raw.GL.SUN.global_alpha to provide a more 
Python-friendly API

Overview (from the spec)
	
	Transparency is done in OpenGL using alpha blending. An alpha value
	of 0.0 is used for fully transparent objects, while an alpha value
	of 1.0 is used for fully opaque objects.  A value of 0.25 is 75%
	transparent, and so on.
	
	OpenGL defines alpha as a component of the vertex color state.
	Whenever a color is set, the alpha component is set along with the
	red, green, and blue components.  This means that transparency
	can't be changed for primitives with per-vertex colors without
	modifying the color of each vertex, replacing the old alpha
	component with the new alpha component.  This can be very expensive
	for objects that are drawn using vertex arrays; it all but
	precludes the use of display lists.
	
	This extension defines a new global alpha attribute that can be
	used to specify an alpha factor that is independent from the alpha
	component of the color value.  The global alpha factor is
	multiplied by the fragment's alpha value after primitive
	rasterization and prior to texture mapping, replacing the
	fragment's alpha value.  The global alpha extension is only
	specified in RGBA mode and must be applied prior to any texture
	mapping operation.  It is enabled by a new GLOBAL_ALPHA flag.
	

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/SUN/global_alpha.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.SUN.global_alpha import *
from OpenGL.raw.GL.SUN.global_alpha import _EXTENSION_NAME

def glInitGlobalAlphaSUN():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION