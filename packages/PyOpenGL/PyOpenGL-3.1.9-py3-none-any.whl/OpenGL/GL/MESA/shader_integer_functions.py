'''OpenGL extension MESA.shader_integer_functions

This module customises the behaviour of the 
OpenGL.raw.GL.MESA.shader_integer_functions to provide a more 
Python-friendly API

Overview (from the spec)
	
	GL_ARB_gpu_shader5 extends GLSL in a number of useful ways.  Much of this
	added functionality requires significant hardware support.  There are many
	aspects, however, that can be easily implmented on any GPU with "real"
	integer support (as opposed to simulating integers using floating point
	calculations).
	
	This extension provides a set of new features to the OpenGL Shading
	Language to support capabilities of these GPUs, extending the
	capabilities of version 1.30 of the OpenGL Shading Language and version
	3.00 of the OpenGL ES Shading Language.  Shaders using the new
	functionality provided by this extension should enable this
	functionality via the construct
	
	  #extension GL_MESA_shader_integer_functions : require   (or enable)
	
	This extension provides a variety of new features for all shader types,
	including:
	
	  * support for implicitly converting signed integer types to unsigned
	    types, as well as more general implicit conversion and function
	    overloading infrastructure to support new data types introduced by
	    other extensions;
	
	  * new built-in functions supporting:
	
	    * splitting a floating-point number into a significand and exponent
	      (frexp), or building a floating-point number from a significand and
	      exponent (ldexp);
	
	    * integer bitfield manipulation, including functions to find the
	      position of the most or least significant set bit, count the number
	      of one bits, and bitfield insertion, extraction, and reversal;
	
	    * extended integer precision math, including add with carry, subtract
	      with borrow, and extenended multiplication;
	
	The resulting extension is a strict subset of GL_ARB_gpu_shader5.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/MESA/shader_integer_functions.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.MESA.shader_integer_functions import *
from OpenGL.raw.GL.MESA.shader_integer_functions import _EXTENSION_NAME

def glInitShaderIntegerFunctionsMESA():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION