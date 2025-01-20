'''OpenGL extension ARB.ES2_compatibility

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.ES2_compatibility to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension adds support for features of OpenGL ES 2.0 that are
	missing from OpenGL 3.x. Enabling these features will ease the process
	of porting applications from OpenGL ES 2.0 to OpenGL.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/ES2_compatibility.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.ARB.ES2_compatibility import *
from OpenGL.raw.GL.ARB.ES2_compatibility import _EXTENSION_NAME

def glInitEs2CompatibilityARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# INPUT glShaderBinary.binary size not checked against length
# INPUT glShaderBinary.shaders size not checked against count
glShaderBinary=wrapper.wrapper(glShaderBinary).setInputArraySize(
    'binary', None
).setInputArraySize(
    'shaders', None
)
glGetShaderPrecisionFormat=wrapper.wrapper(glGetShaderPrecisionFormat).setOutput(
    'precision',size=(1,),orPassIn=True
).setOutput(
    'range',size=(2,),orPassIn=True
)
### END AUTOGENERATED SECTION
from OpenGL import lazywrapper as _lazywrapper
from OpenGL.arrays import GLintArray
@_lazywrapper.lazy( glGetShaderPrecisionFormat )
def glGetShaderPrecisionFormat(baseOperation, shadertype, precisiontype, range=None,precision=None ):
    """Provides range and precision if not provided, returns (range,precision)"""
    if range is None:
        range = GLintArray.zeros( (2,))
    if precision is None:
        precision = GLintArray.zeros((2,))
    baseOperation( shadertype, precisiontype, range, precision )
    return range, precision
