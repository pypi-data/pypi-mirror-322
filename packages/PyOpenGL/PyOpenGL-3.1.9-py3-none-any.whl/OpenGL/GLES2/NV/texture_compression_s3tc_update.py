'''OpenGL extension NV.texture_compression_s3tc_update

This module customises the behaviour of the 
OpenGL.raw.GLES2.NV.texture_compression_s3tc_update to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension allows for full or partial image updates to a
	compressed 2D texture from an uncompressed texel data buffer using
	TexImage2D and TexSubImage2D. Consquently, if a compressed internal
	format is used, all the restrictions associated with compressed
	textures will apply. These include sub-image updates aligned to 4x4
	pixel blocks and the restriction on usage as render targets.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/texture_compression_s3tc_update.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.NV.texture_compression_s3tc_update import *
from OpenGL.raw.GLES2.NV.texture_compression_s3tc_update import _EXTENSION_NAME

def glInitTextureCompressionS3TcUpdateNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION