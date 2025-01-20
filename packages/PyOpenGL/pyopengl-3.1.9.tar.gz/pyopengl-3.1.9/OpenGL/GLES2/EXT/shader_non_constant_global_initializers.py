'''OpenGL extension EXT.shader_non_constant_global_initializers

This module customises the behaviour of the 
OpenGL.raw.GLES2.EXT.shader_non_constant_global_initializers to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension adds the ability to use non-constant initializers for
	global variables in the OpenGL ES Shading Language specifications.
	This functionality is already present in the OpenGL Shading language
	specification.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/shader_non_constant_global_initializers.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.EXT.shader_non_constant_global_initializers import *
from OpenGL.raw.GLES2.EXT.shader_non_constant_global_initializers import _EXTENSION_NAME

def glInitShaderNonConstantGlobalInitializersEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION