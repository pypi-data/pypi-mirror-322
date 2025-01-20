'''OpenGL extension EXT.pixel_buffer_object

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.pixel_buffer_object to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension expands on the interface provided by buffer objects.
	It is intended to permit buffer objects to be used not only with 
	vertex array data, but also with pixel data.
	Buffer objects were promoted from the ARB_vertex_buffer_object
	extension in OpenGL 1.5.
	
	Recall that buffer objects conceptually are nothing more than arrays
	of bytes, just like any chunk of memory. Buffer objects allow GL
	commands to source data from a buffer object by binding the buffer
	object to a given target and then overloading a certain set of GL
	commands' pointer arguments to refer to offsets inside the buffer,
	rather than pointers to user memory.  An offset is encoded in a
	pointer by adding the offset to a null pointer.
	
	This extension does not add any new functionality to buffer
	objects themselves.  It simply adds two new targets to which buffer
	objects can be bound: PIXEL_PACK_BUFFER and PIXEL_UNPACK_BUFFER.
	When a buffer object is bound to the PIXEL_PACK_BUFFER target,
	commands such as ReadPixels write their data into a buffer object.
	When a buffer object is bound to the PIXEL_UNPACK_BUFFER target,
	commands such as DrawPixels read their data from a buffer object.
	
	There are a wide variety of applications for such functionality.
	Some of the most interesting ones are:
	
	- "Render to vertex array."  The application can use a fragment
	  program to render some image into one of its buffers, then read
	  this image out into a buffer object via ReadPixels.  Then, it can
	  use this buffer object as a source of vertex data.
	
	- Streaming textures.  If the application uses MapBuffer/UnmapBuffer
	  to write its data for TexSubImage into a buffer object, at least
	  one of the data copies usually required to download a texture can
	  be eliminated, significantly increasing texture download
	  performance.
	
	- Asynchronous ReadPixels.  If an application needs to read back a
	  number of images and process them with the CPU, the existing GL
	  interface makes it nearly impossible to pipeline this operation.
	  The driver will typically send the hardware a readback command
	  when ReadPixels is called, and then wait for all of the data to
	  be available before returning control to the application.  Then,
	  the application can either process the data immediately or call
	  ReadPixels again; in neither case will the readback overlap with
	  the processing.  If the application issues several readbacks into
	  several buffer objects, however, and then maps each one to process
	  its data, then the readbacks can proceed in parallel with the data
	  processing.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/pixel_buffer_object.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.EXT.pixel_buffer_object import *
from OpenGL.raw.GL.EXT.pixel_buffer_object import _EXTENSION_NAME

def glInitPixelBufferObjectEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION