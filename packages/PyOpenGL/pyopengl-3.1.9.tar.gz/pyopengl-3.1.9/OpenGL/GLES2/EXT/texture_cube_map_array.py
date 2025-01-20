'''OpenGL extension EXT.texture_cube_map_array

This module customises the behaviour of the 
OpenGL.raw.GLES2.EXT.texture_cube_map_array to provide a more 
Python-friendly API

Overview (from the spec)
	
	OpenGL ES 3.1 supports two-dimensional array textures. An array texture
	is an ordered set of images with the same size and format. Each image in
	an array texture has a unique level. This extension expands texture
	array support to include cube map textures.
	
	A cube map array texture is a two-dimensional array texture that may
	contain many cube map layers. Each cube map layer is a unique cube map
	image set. Images in a cube map array have the same size and format
	limitations as two-dimensional array textures. A cube map array texture
	is specified using TexImage3D or TexStorage3D in a similar manner to
	two-dimensional arrays. Cube map array textures can be bound to a render
	targets of a frame buffer object just as two-dimensional arrays are,
	using FramebufferTextureLayer.
	
	When accessed by a shader, a cube map array texture acts as a single
	unit. The "s", "t", "r" texture coordinates are treated as a regular
	cube map texture fetch. The "q" texture is treated as an unnormalized
	floating-point value identifying the layer of the cube map array
	texture. Cube map array texture lookups do not filter between layers.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/texture_cube_map_array.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.EXT.texture_cube_map_array import *
from OpenGL.raw.GLES2.EXT.texture_cube_map_array import _EXTENSION_NAME

def glInitTextureCubeMapArrayEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION