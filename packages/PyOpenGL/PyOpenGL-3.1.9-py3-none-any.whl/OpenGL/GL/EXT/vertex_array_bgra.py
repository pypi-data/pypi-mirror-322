'''OpenGL extension EXT.vertex_array_bgra

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.vertex_array_bgra to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension provides a single new component format for vertex
	arrays to read 4-component unsigned byte vertex attributes with a
	BGRA component ordering.
	
	OpenGL expects vertex arrays containing 4 unsigned bytes per
	element to be in the RGBA, STRQ, or XYZW order (reading components
	left-to-right in their lower address to higher address order).
	Essentially the order the components appear in memory is the order
	the components appear in the resulting vertex attribute vector.
	
	However Direct3D has color (diffuse and specular) vertex arrays
	containing 4 unsigned bytes per element that are in a BGRA order
	(again reading components left-to-right in their lower address
	to higher address order).  Direct3D calls this "ARGB" reading the
	components in the opposite order (reading components left-to-right
	in their higher address to lower address order).  This ordering is
	generalized in the DirectX 10 by the DXGI_FORMAT_B8G8R8A8_UNORM
	format.
	
	For an OpenGL application to source color data from a vertex
	buffer formatted for Direct3D's color array format conventions,
	the application is forced to either:
	
	1.  Rely on a vertex program or shader to swizzle the color components
	    from the BGRA to conventional RGBA order.
	
	2.  Re-order the color data components in the vertex buffer from
	    Direct3D's native BGRA order to OpenGL's native RGBA order.
	
	Neither option is entirely satisfactory.
	
	Option 1 means vertex shaders have to be re-written to source colors
	differently.  If the same vertex shader is used with vertex arrays
	configured to source the color as 4 floating-point color components,
	the swizzle for BGRA colors stored as 4 unsigned bytes is no longer
	appropriate.  The shader's swizzling of colors becomes dependent on
	the type and number of color components.  Ideally the vertex shader
	should be independent from the format and component ordering of the
	data it sources.
	
	Option 2 is expensive because vertex buffers may have to be
	reformatted prior to use.  OpenGL treats the memory for vertex arrays
	(whether client-side memory or buffer objects) as essentially untyped
	memory and vertex arrays can be stored separately, interleaved,
	or even interwoven (where multiple arrays overlap with differing
	strides and formats).
	
	Rather than force a re-ordering of either vertex array components
	in memory or a vertex array format-dependent re-ordering of vertex
	shader inputs, OpenGL can simply provide a vertex array format that
	matches the Direct3D color component ordering.
	
	This approach mimics that of the EXT_bgra extension for pixel and
	texel formats except for vertex instead of image data.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/vertex_array_bgra.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.EXT.vertex_array_bgra import *
from OpenGL.raw.GL.EXT.vertex_array_bgra import _EXTENSION_NAME

def glInitVertexArrayBgraEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION