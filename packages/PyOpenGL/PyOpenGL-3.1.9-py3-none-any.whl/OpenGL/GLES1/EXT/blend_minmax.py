'''OpenGL extension EXT.blend_minmax

This module customises the behaviour of the 
OpenGL.raw.GLES1.EXT.blend_minmax to provide a more 
Python-friendly API

Overview (from the spec)
	
	Blending capability is extended by respecifying the entire blend
	equation.  While this document defines only two new equations, the
	BlendEquationEXT procedure that it defines will be used by subsequent
	extensions to define additional blending equations.
	
	The two new equations defined by this extension produce the minimum
	(or maximum) color components of the source and destination colors.
	Taking the maximum is useful for applications such as maximum projection
	in medical imaging.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/blend_minmax.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES1 import _types, _glgets
from OpenGL.raw.GLES1.EXT.blend_minmax import *
from OpenGL.raw.GLES1.EXT.blend_minmax import _EXTENSION_NAME

def glInitBlendMinmaxEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION