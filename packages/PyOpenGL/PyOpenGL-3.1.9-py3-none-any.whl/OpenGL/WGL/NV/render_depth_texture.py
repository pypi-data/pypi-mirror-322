'''OpenGL extension NV.render_depth_texture

This module customises the behaviour of the 
OpenGL.raw.WGL.NV.render_depth_texture to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/render_depth_texture.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.WGL import _types, _glgets
from OpenGL.raw.WGL.NV.render_depth_texture import *
from OpenGL.raw.WGL.NV.render_depth_texture import _EXTENSION_NAME

def glInitRenderDepthTextureNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION