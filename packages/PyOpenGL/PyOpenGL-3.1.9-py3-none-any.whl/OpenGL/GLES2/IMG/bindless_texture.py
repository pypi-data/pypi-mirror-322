'''OpenGL extension IMG.bindless_texture

This module customises the behaviour of the 
OpenGL.raw.GLES2.IMG.bindless_texture to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension allows OpenGL ES applications to access texture objects in
	shaders without first binding each texture to one of a limited number of
	texture image units.  Using this extension, an application can query a
	64-bit unsigned integer texture handle for each texture that it wants to
	access and then use that handle directly in GLSL ES. This extensions
	significantly reduces the amount of API and internal GL driver overhead
	needed to manage resource bindings.
	
	This extension adds no new data types to GLSL.  Instead, it uses existing
	sampler data types and allows them to be populated with texture handles.
	This extension also permits sampler types to be used as uniform block
	members as well as default uniforms. Additionally, new APIs are provided to
	load values for sampler uniforms with 64-bit handle inputs.  The use of
	existing integer-based Uniform* APIs is still permitted, in which case the
	integer specified will identify a texture image.  For samplers with values
	specified as texture image units, the GL implementation will translate the
	unit number to an internal handle as required.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/IMG/bindless_texture.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.IMG.bindless_texture import *
from OpenGL.raw.GLES2.IMG.bindless_texture import _EXTENSION_NAME

def glInitBindlessTextureIMG():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# INPUT glUniformHandleui64vIMG.value size not checked against count
glUniformHandleui64vIMG=wrapper.wrapper(glUniformHandleui64vIMG).setInputArraySize(
    'value', None
)
# INPUT glProgramUniformHandleui64vIMG.values size not checked against count
glProgramUniformHandleui64vIMG=wrapper.wrapper(glProgramUniformHandleui64vIMG).setInputArraySize(
    'values', None
)
### END AUTOGENERATED SECTION