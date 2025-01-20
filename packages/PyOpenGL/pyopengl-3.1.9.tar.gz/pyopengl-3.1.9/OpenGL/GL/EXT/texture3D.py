'''OpenGL extension EXT.texture3D

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.texture3D to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension defines 3-dimensional texture mapping.  In order to
	define a 3D texture image conveniently, this extension also defines the
	in-memory formats for 3D images, and adds pixel storage modes to support
	them.
	
	One important application of 3D textures is rendering volumes of image
	data.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/texture3D.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.EXT.texture3D import *
from OpenGL.raw.GL.EXT.texture3D import _EXTENSION_NAME

def glInitTexture3DEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# INPUT glTexImage3DEXT.pixels size not checked against 'format,type,width,height,depth'
glTexImage3DEXT=wrapper.wrapper(glTexImage3DEXT).setInputArraySize(
    'pixels', None
)
# INPUT glTexSubImage3DEXT.pixels size not checked against 'format,type,width,height,depth'
glTexSubImage3DEXT=wrapper.wrapper(glTexSubImage3DEXT).setInputArraySize(
    'pixels', None
)
### END AUTOGENERATED SECTION