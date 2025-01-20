'''OpenGL extension KHR.client_get_all_proc_addresses

This module customises the behaviour of the 
OpenGL.raw.EGL.KHR.client_get_all_proc_addresses to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/KHR/client_get_all_proc_addresses.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.EGL import _types, _glgets
from OpenGL.raw.EGL.KHR.client_get_all_proc_addresses import *
from OpenGL.raw.EGL.KHR.client_get_all_proc_addresses import _EXTENSION_NAME

def glInitClientGetAllProcAddressesKHR():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION