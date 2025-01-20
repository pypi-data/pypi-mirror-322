'''OpenGL extension OES.texture_compression_astc

This module customises the behaviour of the 
OpenGL.raw.GLES2.OES.texture_compression_astc to provide a more 
Python-friendly API

Overview (from the spec)
	
	Adaptive Scalable Texture Compression (ASTC) is a new texture
	compression technology that offers unprecendented flexibility,
	while producing better or comparable results than existing texture
	compressions at all bit rates. It includes support for 2D and 3D
	textures, with low and high dynamic range, at bitrates from below
	1 bit/pixel up to 8 bits/pixel in fine steps.
	
	The goal of this extension is to support the full profile of the
	ASTC texture compression specification.
	
	ASTC-compressed textures are handled in OpenGL ES and OpenGL by
	adding new supported formats to the existing mechanisms for handling
	compressed textures.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/OES/texture_compression_astc.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.OES.texture_compression_astc import *
from OpenGL.raw.GLES2.OES.texture_compression_astc import _EXTENSION_NAME

def glInitTextureCompressionAstcOES():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION