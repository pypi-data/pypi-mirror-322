'''OpenGL extension NV.bindless_multi_draw_indirect

This module customises the behaviour of the 
OpenGL.raw.GL.NV.bindless_multi_draw_indirect to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension combines NV_vertex_buffer_unified_memory and 
	ARB_multi_draw_indirect to allow the processing of multiple drawing
	commands, whose vertex and index data can be sourced from arbitrary 
	buffer locations, by a single function call.
	
	The NV_vertex_buffer_unified_memory extension provided a mechanism to 
	specify vertex attrib and element array locations using GPU addresses.
	Prior to this extension, these addresses had to be set through explicit
	function calls. Now the ability to set the pointer addresses indirectly
	by extending the GL_ARB_draw_indirect mechanism has been added.
	
	Combined with other "bindless" extensions, such as NV_bindless_texture and
	NV_shader_buffer_load, it is now possible for the GPU to create draw
	commands that source all resource inputs, which are common to change 
	frequently between draw calls from the GPU: vertex and index buffers, 
	samplers, images and other shader input data stored in buffers.
	

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/bindless_multi_draw_indirect.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.NV.bindless_multi_draw_indirect import *
from OpenGL.raw.GL.NV.bindless_multi_draw_indirect import _EXTENSION_NAME

def glInitBindlessMultiDrawIndirectNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION