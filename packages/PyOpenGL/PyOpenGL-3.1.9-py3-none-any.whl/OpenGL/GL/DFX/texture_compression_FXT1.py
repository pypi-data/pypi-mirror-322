'''OpenGL extension DFX.texture_compression_FXT1

This module customises the behaviour of the 
OpenGL.raw.GL.DFX.texture_compression_FXT1 to provide a more 
Python-friendly API

Overview (from the spec)
	
	    This extension additional texture compression functionality 's FXT1
	    format, specific to 3dfxsubject to all the requirements and
	    limitations described by the extension GL_ARB_texture_compression.
	    The FXT1 texture format supports only 2D and 3D images without
	    borders.
	
	    Because 3dfx expects to make continual improvement to its FXT1
	    compressor implementation, 3dfx recommends that to achieve best
	    visual quality applications adopt the following procedure with
	    respect to reuse of textures compressed by the GL:
	
		1) Save the RENDERER and VERSION strings along with images
		   compressed by the GL;
		2) Before reuse of the textures, compare the stored strings with
		   strings newly returned from the current GL;
		3) If out-of-date, repeat the compression and storage steps.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/DFX/texture_compression_FXT1.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.DFX.texture_compression_FXT1 import *
from OpenGL.raw.GL.DFX.texture_compression_FXT1 import _EXTENSION_NAME

def glInitTextureCompressionFxt1DFX():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION