'''OpenGL extension EXT.texture_swizzle

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.texture_swizzle to provide a more 
Python-friendly API

Overview (from the spec)
	
	Classic OpenGL texture formats conflate texture storage and
	interpretation, and assume that textures represent color. In 
	modern applications, a significant quantity of textures don't
	represent color, but rather data like shadow maps, normal maps,
	page tables, occlusion data, etc.. For the latter class of data,
	calling the data "RGBA" is just a convenient mapping of what the
	data is onto the current model, but isn't an accurate reflection
	of the reality of the data.
	
	The existing texture formats provide an almost orthogonal set of
	data types, sizes, and number of components, but the mappings of 
	this storage into what the shader or fixed-function pipeline 
	fetches is very much non-orthogonal. Previous extensions have
	added some of the most demanded missing formats, but the problem
	has not been solved once and for all.
	
	This extension provides a mechanism to swizzle the components 
	of a texture before they are applied according to the texture
	environment in fixed-function or as they are returned to the 
	shader.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/texture_swizzle.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.EXT.texture_swizzle import *
from OpenGL.raw.GL.EXT.texture_swizzle import _EXTENSION_NAME

def glInitTextureSwizzleEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION