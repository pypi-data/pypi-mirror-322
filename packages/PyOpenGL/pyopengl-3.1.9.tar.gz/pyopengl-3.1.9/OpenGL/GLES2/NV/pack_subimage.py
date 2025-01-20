'''OpenGL extension NV.pack_subimage

This module customises the behaviour of the 
OpenGL.raw.GLES2.NV.pack_subimage to provide a more 
Python-friendly API

Overview (from the spec)
	
	This OpenGL ES 2.0 extension adds support for GL_PACK_ROW_LENGTH_NV,
	GL_PACK_SKIP_ROWS_NV and GL_PACK_SKIP_PIXELS_NV as valid enums to
	PixelStore. The functionality is the same as in OpenGL. These are
	useful to update a sub-rectangle in host memory with data that can
	be read from the framebuffer or a texture (using FBO and texture
	attachments).

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/pack_subimage.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.NV.pack_subimage import *
from OpenGL.raw.GLES2.NV.pack_subimage import _EXTENSION_NAME

def glInitPackSubimageNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION