'''OpenGL extension AMD.shader_ballot

This module customises the behaviour of the 
OpenGL.raw.GL.AMD.shader_ballot to provide a more 
Python-friendly API

Overview (from the spec)
	
	The extensions ARB_shader_group_vote and ARB_shader_ballot introduced the
	concept of sub-groups and a set of operations that allow data exchange
	across shader invocations within a sub-group.
	
	This extension further extends the capabilities of these extensions with
	additional sub-group operations.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/AMD/shader_ballot.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.AMD.shader_ballot import *
from OpenGL.raw.GL.AMD.shader_ballot import _EXTENSION_NAME

def glInitShaderBallotAMD():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION