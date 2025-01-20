'''OpenGL extension ARB.texture_gather

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.texture_gather to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension provides a new set of texture functions
	(textureGather) to the shading language that determine 2x2 footprint
	that are used for linear filtering in a texture lookup, and return a
	vector consisting of the first component from each of the four
	texels in the footprint.
	

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/texture_gather.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.ARB.texture_gather import *
from OpenGL.raw.GL.ARB.texture_gather import _EXTENSION_NAME

def glInitTextureGatherARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION