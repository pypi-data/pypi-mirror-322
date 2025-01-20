'''OpenGL extension OES.packed_depth_stencil

This module customises the behaviour of the 
OpenGL.raw.GLES1.OES.packed_depth_stencil to provide a more 
Python-friendly API

Overview (from the spec)
	
	Many OpenGL implementations have chosen to interleave the depth and stencil
	buffers into one buffer, often with 24 bits of depth precision and 8 bits of
	stencil data.  32 bits is more than is needed for the depth buffer much of 
	the time; a 24-bit depth buffer, on the other hand, requires that reads and
	writes of depth data be unaligned with respect to power-of-two boundaries.
	On the other hand, 8 bits of stencil data is more than sufficient for most
	applications, so it is only natural to pack the two buffers into a single 
	buffer with both depth and stencil data.  OpenGL never provides direct 
	access to the buffers, so the OpenGL implementation can provide an interface
	to applications where it appears the one merged buffer is composed of two
	logical buffers.
	
	One disadvantage of this scheme is that OpenGL lacks any means by which this
	packed data can be handled efficiently.  For example, when an application
	reads from the 24-bit depth buffer, using the type GL_UNSIGNED_SHORT will 
	lose 8 bits of data, while GL_UNSIGNED_INT has 8 too many.  Both require 
	expensive format conversion operations.  A 24-bit format would be no more 
	suitable, because it would also suffer from the unaligned memory accesses 
	that made the standalone 24-bit depth buffer an unattractive proposition in
	the first place.
	
	If OES_depth_texture is supported, a new data format, GL_DEPTH_STENCIL_OES,
	as well as a packed data type, UNSIGNED_INT_24_8_OES, together can be used
	with glTex[Sub]Image2D.  This provides an efficient way to supply data for a
	24-bit depth texture.  When a texture with DEPTH_STENCIL_OES data is bound
	for texturing, only the depth component is accessible through the texture
	fetcher.  
	
	This extension also provides a new sized internal format,
	DEPTH24_STENCIL8_OES, which can be used for renderbuffer storage.  When a
	renderbuffer or texture image with a DEPTH_STENCIL_OES base internal format
	is attached to both the depth and stencil attachment points of a framebuffer
	object, then it becomes both the depth and stencil buffers of the
	framebuffer.  This fits nicely with hardware that interleaves both depth and
	stencil data into a single buffer.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/OES/packed_depth_stencil.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES1 import _types, _glgets
from OpenGL.raw.GLES1.OES.packed_depth_stencil import *
from OpenGL.raw.GLES1.OES.packed_depth_stencil import _EXTENSION_NAME

def glInitPackedDepthStencilOES():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION