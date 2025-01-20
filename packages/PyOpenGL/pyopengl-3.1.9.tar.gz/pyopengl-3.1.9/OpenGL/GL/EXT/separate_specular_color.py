'''OpenGL extension EXT.separate_specular_color

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.separate_specular_color to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension adds a second color to rasterization when lighting is 
	enabled.  Its purpose is to produce textured objects with specular 
	highlights which are the color of the lights.  It applies only to 
	rgba lighting.
	
	The two colors are computed at the vertexes.  They are both clamped, 
	flat-shaded, clipped, and converted to fixed-point just like the 
	current rgba color (see Figure 2.8).  Rasterization interpolates 
	both colors to fragments.  If texture is enabled, the first (or 
	primary) color is the input to the texture environment; the fragment 
	color is the sum of the second color and the color resulting from 
	texture application.  If texture is not enabled, the fragment color 
	is the sum of the two colors.
	
	A new control to LightModel*, LIGHT_MODEL_COLOR_CONTROL_EXT, manages 
	the values of the two colors.  It takes values: SINGLE_COLOR_EXT, a 
	compatibility mode, and SEPARATE_SPECULAR_COLOR_EXT, the object of 
	this extension.  In single color mode, the primary color is the 
	current final color and the secondary color is 0.0.  In separate 
	specular mode, the primary color is the sum of the ambient, diffuse, 
	and emissive terms of final color and the secondary color is the 
	specular term.
	
	There is much concern that this extension may not be compatible with
	the future direction of OpenGL with regards to better lighting and
	shading models.  Until those impacts are resolved, serious
	consideration should be given before adding to the interface
	specified herein (for example, allowing the user to specify a
	second input color).

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/separate_specular_color.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.EXT.separate_specular_color import *
from OpenGL.raw.GL.EXT.separate_specular_color import _EXTENSION_NAME

def glInitSeparateSpecularColorEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION