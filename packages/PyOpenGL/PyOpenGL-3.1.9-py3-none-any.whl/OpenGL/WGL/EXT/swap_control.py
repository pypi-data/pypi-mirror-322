'''OpenGL extension EXT.swap_control

This module customises the behaviour of the 
OpenGL.raw.WGL.EXT.swap_control to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension allows an application to specify a minimum
	periodicity of color buffer swaps, measured in video frame periods,
	for a particular drawable. It also allows an application to query
	the swap interval and the implementation-dependent maximum swap
	interval of a drawable.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/swap_control.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.WGL import _types, _glgets
from OpenGL.raw.WGL.EXT.swap_control import *
from OpenGL.raw.WGL.EXT.swap_control import _EXTENSION_NAME

def glInitSwapControlEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION