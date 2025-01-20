'''OpenGL extension KHR.shader_subgroup

This module customises the behaviour of the 
OpenGL.raw.GLES2.KHR.shader_subgroup to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension enables support for the KHR_shader_subgroup shading
	language extension in OpenGL and OpenGL ES.
	
	The extension adds API queries to be able to query
	
	  - the size of subgroups in this implementation (SUBGROUP_SIZE_KHR)
	  - which shader stages support subgroup operations
	    (SUBGROUP_SUPPORTED_STAGES_KHR)
	  - which subgroup features are supported (SUBGROUP_SUPPORTED_FEATURES_KHR)
	  - whether quad subgroup operations are supported in all
	    stages supporting subgroup operations (SUBGROUP_QUAD_ALL_STAGES_KHR)
	
	In OpenGL implementations supporting SPIR-V, this extension enables the
	minimal subset of SPIR-V 1.3 which is required to support the subgroup
	features that are supported by the implementation.
	
	In OpenGL ES implementations, this extension does NOT add support for
	SPIR-V or for any of the built-in shading language functions (8.18)
	that have genDType (double) prototypes.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/KHR/shader_subgroup.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.KHR.shader_subgroup import *
from OpenGL.raw.GLES2.KHR.shader_subgroup import _EXTENSION_NAME

def glInitShaderSubgroupKHR():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION