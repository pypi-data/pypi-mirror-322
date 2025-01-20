'''OpenGL extension SGIS.fog_function

This module customises the behaviour of the 
OpenGL.raw.GL.SGIS.fog_function to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension allows to define application-specific fog blend-factor
	function.  Function is defined by the set of the "control" points and
	should be monotonic. Each control point represented as a pair of the
	eye-space distance value and corresponding value of the fog blending 
	factor. The minimum number of control points is one. The maximum 
	number is implementation dependent.
	

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/SGIS/fog_function.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.SGIS.fog_function import *
from OpenGL.raw.GL.SGIS.fog_function import _EXTENSION_NAME

def glInitFogFunctionSGIS():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# INPUT glFogFuncSGIS.points size not checked against n*2
glFogFuncSGIS=wrapper.wrapper(glFogFuncSGIS).setInputArraySize(
    'points', None
)
glGetFogFuncSGIS=wrapper.wrapper(glGetFogFuncSGIS).setOutput(
    'points',size=_glgets._glget_size_mapping,pnameArg='',orPassIn=True
)
### END AUTOGENERATED SECTION