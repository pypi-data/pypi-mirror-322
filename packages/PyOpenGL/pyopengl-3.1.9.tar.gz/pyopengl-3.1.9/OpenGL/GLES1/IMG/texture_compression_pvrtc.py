'''OpenGL extension IMG.texture_compression_pvrtc

This module customises the behaviour of the 
OpenGL.raw.GLES1.IMG.texture_compression_pvrtc to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension provides additional texture compression functionality
	specific to Imagination Technologies PowerVR Texture compression format
	(called PVRTC) subject to all the requirements and limitations described 
	by the OpenGL 1.3 specifications.
	
	This extension supports 4 and 2 bit per pixel texture compression
	formats. Because the compression of PVRTC is very CPU intensive,
	it is not appropriate to carry out compression on the target
	platform. Therefore this extension only supports the loading of
	compressed texture data.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/IMG/texture_compression_pvrtc.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES1 import _types, _glgets
from OpenGL.raw.GLES1.IMG.texture_compression_pvrtc import *
from OpenGL.raw.GLES1.IMG.texture_compression_pvrtc import _EXTENSION_NAME

def glInitTextureCompressionPvrtcIMG():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION