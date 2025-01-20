'''OpenGL extension NV.compute_shader_derivatives

This module customises the behaviour of the 
OpenGL.raw.GLES2.NV.compute_shader_derivatives to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension adds OpenGL and OpenGL ES API support for the OpenGL
	Shading Language (GLSL) extension "NV_compute_shader_derivatives".
	
	That extension, when enabled, allows applications to use derivatives in
	compute shaders.  It adds compute shader support for explicit derivative
	built-in functions like dFdx(), automatic derivative computation in
	texture lookup functions like texture(), use of the optional LOD bias
	parameter to adjust the computed level of detail values in texture lookup
	functions, and the texture level of detail query function
	textureQueryLod().

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/compute_shader_derivatives.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.NV.compute_shader_derivatives import *
from OpenGL.raw.GLES2.NV.compute_shader_derivatives import _EXTENSION_NAME

def glInitComputeShaderDerivativesNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION