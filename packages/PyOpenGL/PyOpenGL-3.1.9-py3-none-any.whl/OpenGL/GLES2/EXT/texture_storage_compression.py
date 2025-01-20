'''OpenGL extension EXT.texture_storage_compression

This module customises the behaviour of the 
OpenGL.raw.GLES2.EXT.texture_storage_compression to provide a more 
Python-friendly API

Overview (from the spec)
	
	Applications may wish to take advantage of framebuffer compression. Some
	platforms may support framebuffer compression at fixed bitrates. Such
	compression algorithms generally produce results that are visually lossless,
	but the results are typically not bit-exact when compared to a non-compressed
	result.
	
	This extension enables applications to opt-in to compression for
	immutable textures.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/texture_storage_compression.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.EXT.texture_storage_compression import *
from OpenGL.raw.GLES2.EXT.texture_storage_compression import _EXTENSION_NAME

def glInitTextureStorageCompressionEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION