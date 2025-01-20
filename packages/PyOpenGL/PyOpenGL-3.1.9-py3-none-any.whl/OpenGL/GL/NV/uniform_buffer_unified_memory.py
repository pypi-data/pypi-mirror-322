'''OpenGL extension NV.uniform_buffer_unified_memory

This module customises the behaviour of the 
OpenGL.raw.GL.NV.uniform_buffer_unified_memory to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension provides a mechanism to specify uniform buffers
	using GPU addresses.
	
	Binding uniform buffers is one of the most frequent and expensive
	operations in many GL applications, due to the cost of chasing 
	pointers and binding objects described in the overview of 
	NV_shader_buffer_load. The intent of this extension is to enable a 
	way for the application to specify uniform buffer state that alleviates
	the overhead of object binds and driver memory management.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/uniform_buffer_unified_memory.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.NV.uniform_buffer_unified_memory import *
from OpenGL.raw.GL.NV.uniform_buffer_unified_memory import _EXTENSION_NAME

def glInitUniformBufferUnifiedMemoryNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION