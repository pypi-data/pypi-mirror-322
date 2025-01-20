'''OpenGL extension AMD.shader_atomic_counter_ops

This module customises the behaviour of the 
OpenGL.raw.GL.AMD.shader_atomic_counter_ops to provide a more 
Python-friendly API

Overview (from the spec)
	
	The ARB_shader_atomic_counters extension introduced atomic counters, but
	it limits list of potential operations that can be performed on them to
	increment, decrement, and query. This extension extends the list of GLSL
	built-in functions that can operate on atomic counters. The list of new
	operations include:
	
	  * Increment and decrement with wrap
	  * Addition and subtraction
	  * Minimum and maximum
	  * Bitwise operators (AND, OR, XOR, etc.)
	  * Masked OR operator
	  * Exchange, and compare and exchange operators

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/AMD/shader_atomic_counter_ops.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.AMD.shader_atomic_counter_ops import *
from OpenGL.raw.GL.AMD.shader_atomic_counter_ops import _EXTENSION_NAME

def glInitShaderAtomicCounterOpsAMD():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION