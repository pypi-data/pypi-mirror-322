'''OpenGL extension EXT.visual_info

This module customises the behaviour of the 
OpenGL.raw.GLX.EXT.visual_info to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/visual_info.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLX import _types, _glgets
from OpenGL.raw.GLX.EXT.visual_info import *
from OpenGL.raw.GLX.EXT.visual_info import _EXTENSION_NAME

def glInitVisualInfoEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION