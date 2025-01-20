'''OpenGL extension EXT.packed_depth_stencil

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.packed_depth_stencil to provide a more 
Python-friendly API

Overview (from the spec)
	
	Many OpenGL implementations have chosen to interleave the depth and
	stencil buffers into one buffer, often with 24 bits of depth
	precision and 8 bits of stencil data.  32 bits is more than is
	needed for the depth buffer much of the time; a 24-bit depth buffer,
	on the other hand, requires that reads and writes of depth data be
	unaligned with respect to power-of-two boundaries.  On the other
	hand, 8 bits of stencil data is more than sufficient for most
	applications, so it is only natural to pack the two buffers into a
	single buffer with both depth and stencil data.  OpenGL never
	provides direct access to the buffers, so the OpenGL implementation
	can provide an interface to applications where it appears the one
	merged buffer is composed of two logical buffers.
	
	One disadvantage of this scheme is that OpenGL lacks any means by
	which this packed data can be handled efficiently.  For example,
	when an application reads from the 24-bit depth buffer, using the
	type GL_UNSIGNED_SHORT will lose 8 bits of data, while
	GL_UNSIGNED_INT has 8 too many.  Both require expensive format
	conversion operations.  A 24-bit format would be no more suitable,
	because it would also suffer from the unaligned memory accesses that
	made the standalone 24-bit depth buffer an unattractive proposition
	in the first place.
	
	Many applications, such as parallel rendering applications, may also
	wish to draw to or read back from both the depth and stencil buffers
	at the same time.  Currently this requires two separate operations,
	reducing performance.  Since the buffers are interleaved, drawing to
	or reading from both should be no more expensive than using just
	one; in some cases, it may even be cheaper.
	
	This extension provides a new data format, GL_DEPTH_STENCIL_EXT,
	that can be used with the glDrawPixels, glReadPixels, and
	glCopyPixels commands, as well as a packed data type,
	GL_UNSIGNED_INT_24_8_EXT, that is meant to be used with
	GL_DEPTH_STENCIL_EXT.  No other data types are supported with
	GL_DEPTH_STENCIL_EXT.  If ARB_depth_texture or SGIX_depth_texture is
	supported, GL_DEPTH_STENCIL_EXT/GL_UNSIGNED_INT_24_8_EXT data can
	also be used for textures; this provides a more efficient way to
	supply data for a 24-bit depth texture.
	
	GL_DEPTH_STENCIL_EXT data, when passed through the pixel path,
	undergoes both depth and stencil operations.  The depth data is
	scaled and biased by the current GL_DEPTH_SCALE and GL_DEPTH_BIAS,
	while the stencil data is shifted and offset by the current
	GL_INDEX_SHIFT and GL_INDEX_OFFSET.  The stencil data is also put
	through the stencil-to-stencil pixel map.
	
	glDrawPixels of GL_DEPTH_STENCIL_EXT data operates similarly to that
	of GL_STENCIL_INDEX data, bypassing the OpenGL fragment pipeline
	entirely, unlike the treatment of GL_DEPTH_COMPONENT data.  The
	stencil and depth masks are applied, as are the pixel ownership and
	scissor tests, but all other operations are skipped.
	
	glReadPixels of GL_DEPTH_STENCIL_EXT data reads back a rectangle
	from both the depth and stencil buffers.
	
	glCopyPixels of GL_DEPTH_STENCIL_EXT data copies a rectangle from
	both the depth and stencil buffers.  Like glDrawPixels, it applies
	both the stencil and depth masks but skips the remainder of the
	OpenGL fragment pipeline.
	
	glTex[Sub]Image[1,2,3]D of GL_DEPTH_STENCIL_EXT data loads depth and
	stencil data into a depth_stencil texture.  glGetTexImage of
	GL_DEPTH_STENCIL_EXT data can be used to retrieve depth and stencil
	data from a depth/stencil texture.
	
	In addition, a new base internal format, GL_DEPTH_STENCIL_EXT, can
	be used by both texture images and renderbuffer storage.  When an
	image with a DEPTH_STENCIL_EXT internal format is attached to both
	the depth and stencil attachment points of a framebuffer object (see
	EXT_framebuffer_object), then it becomes both the depth and stencil
	buffers of the framebuffer.  This fits nicely with hardware that
	interleaves both depth and stencil data into a single buffer.  When
	a texture with DEPTH_STENCIL_EXT data is bound for texturing, only
	the depth component is accessible through the texture fetcher.  The
	stencil data can be written with TexImage or CopyTexImage, and can
	be read with GetTexImage.  When a DEPTH_STENCIL_EXT image is
	attached to the stencil attachment of the bound framebuffer object,
	the stencil data can be accessed through any operation that reads
	from or writes to the framebuffer's stencil buffer.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/packed_depth_stencil.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.EXT.packed_depth_stencil import *
from OpenGL.raw.GL.EXT.packed_depth_stencil import _EXTENSION_NAME

def glInitPackedDepthStencilEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION
# Setup the new image types
from OpenGL import images 
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_UNSIGNED_INT
images.TYPE_TO_ARRAYTYPE[ GL_UNSIGNED_INT_24_8_EXT ] = GL_UNSIGNED_INT
images.TIGHT_PACK_FORMATS[ GL_UNSIGNED_INT_24_8_EXT ] = 4
images.COMPONENT_COUNTS[ GL_DEPTH_STENCIL_EXT ] = 4
