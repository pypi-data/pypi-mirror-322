'''OpenGL extension NV.uniform_buffer_std430_layout

This module customises the behaviour of the 
OpenGL.raw.GL.NV.uniform_buffer_std430_layout to provide a more 
Python-friendly API

Overview (from the spec)
	
	OpenGL 4.3 (and ARB_enhanced_layouts) provide an enhanced layout
	qualifier syntax for aligning members of uniform and shader storage
	blocks.  The std430 enhanced layout qualifier is advantageous,
	compared with std140, because it provides a more space-efficient
	layout of arrays that more easily matches the data layout in C/C++
	structures stored in CPU memory.
	
	However OpenGL 4.3 precluded using the std430 layout qualifier for
	uniform blocks (by mandating a compilation error be generated).
	
	This extension makes std430 a legal layout qualifier for uniform
	blocks in GLSL when the extension's GLSL #extension functionality
	is enabled or required.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/uniform_buffer_std430_layout.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.NV.uniform_buffer_std430_layout import *
from OpenGL.raw.GL.NV.uniform_buffer_std430_layout import _EXTENSION_NAME

def glInitUniformBufferStd430LayoutNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION