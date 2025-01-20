'''OpenGL extension SGIS.texture_filter4

This module customises the behaviour of the 
OpenGL.raw.GL.SGIS.texture_filter4 to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension allows 1D and 2D textures to be filtered using an
	application-defined, four sample per dimension filter.  (In addition to
	the NEAREST and LINEAR filters defined in the original GL Specification.)
	Such filtering results in higher image quality.  It is defined only
	for non-mipmapped filters.  The filter that is specified must be
	symmetric and separable (in the 2D case).

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/SGIS/texture_filter4.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.SGIS.texture_filter4 import *
from OpenGL.raw.GL.SGIS.texture_filter4 import _EXTENSION_NAME

def glInitTextureFilter4SGIS():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# OUTPUT glGetTexFilterFuncSGIS.weights COMPSIZE(target, filter) 
# INPUT glTexFilterFuncSGIS.weights size not checked against n
glTexFilterFuncSGIS=wrapper.wrapper(glTexFilterFuncSGIS).setInputArraySize(
    'weights', None
)
### END AUTOGENERATED SECTION