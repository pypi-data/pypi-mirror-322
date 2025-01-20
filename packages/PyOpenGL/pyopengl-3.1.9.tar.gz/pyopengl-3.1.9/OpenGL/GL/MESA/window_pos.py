'''OpenGL extension MESA.window_pos

This module customises the behaviour of the 
OpenGL.raw.GL.MESA.window_pos to provide a more 
Python-friendly API

Overview (from the spec)
	
	In order to set the current raster position to a specific window
	coordinate with the RasterPos command, the modelview matrix, projection
	matrix and viewport must be set very carefully.  Furthermore, if the
	desired window coordinate is outside of the window's bounds one must
	rely on a subtle side-effect of the Bitmap command in order to circumvent
	frustum clipping.
	
	This extension provides a set of functions to directly set the
	current raster position, bypassing the modelview matrix, the
	projection matrix and the viewport to window mapping.  Furthermore,
	clip testing is not performed.
	
	This greatly simplifies the process of setting the current raster
	position to a specific window coordinate prior to calling DrawPixels,
	CopyPixels or Bitmap.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/MESA/window_pos.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.MESA.window_pos import *
from OpenGL.raw.GL.MESA.window_pos import _EXTENSION_NAME

def glInitWindowPosMESA():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

glWindowPos2dvMESA=wrapper.wrapper(glWindowPos2dvMESA).setInputArraySize(
    'v', 2
)
glWindowPos2fvMESA=wrapper.wrapper(glWindowPos2fvMESA).setInputArraySize(
    'v', 2
)
glWindowPos2ivMESA=wrapper.wrapper(glWindowPos2ivMESA).setInputArraySize(
    'v', 2
)
glWindowPos2svMESA=wrapper.wrapper(glWindowPos2svMESA).setInputArraySize(
    'v', 2
)
glWindowPos3dvMESA=wrapper.wrapper(glWindowPos3dvMESA).setInputArraySize(
    'v', 3
)
glWindowPos3fvMESA=wrapper.wrapper(glWindowPos3fvMESA).setInputArraySize(
    'v', 3
)
glWindowPos3ivMESA=wrapper.wrapper(glWindowPos3ivMESA).setInputArraySize(
    'v', 3
)
glWindowPos3svMESA=wrapper.wrapper(glWindowPos3svMESA).setInputArraySize(
    'v', 3
)
glWindowPos4dvMESA=wrapper.wrapper(glWindowPos4dvMESA).setInputArraySize(
    'v', 4
)
glWindowPos4fvMESA=wrapper.wrapper(glWindowPos4fvMESA).setInputArraySize(
    'v', 4
)
glWindowPos4ivMESA=wrapper.wrapper(glWindowPos4ivMESA).setInputArraySize(
    'v', 4
)
glWindowPos4svMESA=wrapper.wrapper(glWindowPos4svMESA).setInputArraySize(
    'v', 4
)
### END AUTOGENERATED SECTION