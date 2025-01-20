'''OpenGL extension EXT.color_subtable

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.color_subtable to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension allows a portion of a color table to be redefined.
	If EXT_copy_texture is implemented, this extension also defines a
	method to load a portion of a color lookup table from the 
	framebuffer.
	

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/color_subtable.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.EXT.color_subtable import *
from OpenGL.raw.GL.EXT.color_subtable import _EXTENSION_NAME

def glInitColorSubtableEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# INPUT glColorSubTableEXT.data size not checked against 'format,type,count'
glColorSubTableEXT=wrapper.wrapper(glColorSubTableEXT).setInputArraySize(
    'data', None
)
### END AUTOGENERATED SECTION