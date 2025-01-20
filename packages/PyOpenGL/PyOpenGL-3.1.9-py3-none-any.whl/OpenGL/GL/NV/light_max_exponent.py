'''OpenGL extension NV.light_max_exponent

This module customises the behaviour of the 
OpenGL.raw.GL.NV.light_max_exponent to provide a more 
Python-friendly API

Overview (from the spec)
	
	Default OpenGL does not permit a shininess or spot exponent over
	128.0.  This extension permits implementations to support and
	advertise a maximum shininess and spot exponent beyond 128.0.
	
	Note that extremely high exponents for shininess and/or spot light
	cutoff will require sufficiently high tessellation for acceptable
	lighting results.
	
	Paul Deifenbach's thesis suggests that higher exponents are
	necessary to approximate BRDFs with per-vertex ligthing and
	multiple passes.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/light_max_exponent.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.NV.light_max_exponent import *
from OpenGL.raw.GL.NV.light_max_exponent import _EXTENSION_NAME

def glInitLightMaxExponentNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION