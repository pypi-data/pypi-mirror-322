'''OpenGL extension ARB.vertex_buffer_object

This module customises the behaviour of the 
OpenGL.raw.GLX.ARB.vertex_buffer_object to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension defines an interface that allows various types of data
	(especially vertex array data) to be cached in high-performance
	graphics memory on the server, thereby increasing the rate of data
	transfers.
	
	Chunks of data are encapsulated within "buffer objects", which
	conceptually are nothing more than arrays of bytes, just like any
	chunk of memory.  An API is provided whereby applications can read
	from or write to buffers, either via the GL itself (glBufferData,
	glBufferSubData, glGetBufferSubData) or via a pointer to the memory.
	
	The latter technique is known as "mapping" a buffer.  When an
	application maps a buffer, it is given a pointer to the memory.  When
	the application finishes reading from or writing to the memory, it is
	required to "unmap" the buffer before it is once again permitted to
	use that buffer as a GL data source or sink.  Mapping often allows
	applications to eliminate an extra data copy otherwise required to
	access the buffer, thereby enhancing performance.  In addition,
	requiring that applications unmap the buffer to use it as a data
	source or sink ensures that certain classes of latent synchronization
	bugs cannot occur.
	
	Although this extension only defines hooks for buffer objects to be
	used with OpenGL's vertex array APIs, the API defined in this
	extension permits buffer objects to be used as either data sources or
	sinks for any GL command that takes a pointer as an argument.
	Normally, in the absence of this extension, a pointer passed into the
	GL is simply a pointer to the user's data.  This extension defines
	a mechanism whereby this pointer is used not as a pointer to the data
	itself, but as an offset into a currently bound buffer object.  The
	buffer object ID zero is reserved, and when buffer object zero is
	bound to a given target, the commands affected by that buffer binding
	behave normally.  When a nonzero buffer ID is bound, then the pointer
	represents an offset.
	
	In the case of vertex arrays, this extension defines not merely one
	binding for all attributes, but a separate binding for each
	individual attribute.  As a result, applications can source their
	attributes from multiple buffers.  An application might, for example,
	have a model with constant texture coordinates and variable geometry.
	The texture coordinates might be retrieved from a buffer object with
	the usage mode "STATIC_DRAW", indicating to the GL that the
	application does not expect to update the contents of the buffer
	frequently or even at all, while the vertices might be retrieved from
	a buffer object with the usage mode "STREAM_DRAW", indicating that
	the vertices will be updated on a regular basis.
	
	In addition, a binding is defined by which applications can source
	index data (as used by DrawElements, DrawRangeElements, and
	MultiDrawElements) from a buffer object.  On some platforms, this
	enables very large models to be rendered with no more than a few
	small commands to the graphics device.
	
	It is expected that a future extension will allow sourcing pixel data
	from and writing pixel data to a buffer object.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/vertex_buffer_object.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLX import _types, _glgets
from OpenGL.raw.GLX.ARB.vertex_buffer_object import *
from OpenGL.raw.GLX.ARB.vertex_buffer_object import _EXTENSION_NAME

def glInitVertexBufferObjectARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION