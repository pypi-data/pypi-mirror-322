'''OpenGL extension APPLE.row_bytes

This module customises the behaviour of the 
OpenGL.raw.GL.APPLE.row_bytes to provide a more 
Python-friendly API

Overview (from the spec)
	
	The APPLE_row_bytes extension was developed to relax the limitations
	within GL regarding the packing and unpacking of pixel data from
	arbitrary arrangements in memory.
	
	Prior to this extension, similar, albeit more restrictive, functionality
	existed in GL using pixel storage modes for unpacking, packing, and
	alignment.  The limitation of the existing mechanism lies primarily in how
	packing or unpacking of data is specified with pixel atomicity rather than
	basic machine units.  To some extent, this pixel granularity can be
	overcome using pixel storage modes GL_UNPACK_ALIGNMENT and
	GL_PACK_ALIGNMENT.  Both of these parameters are specified in basic
	machine units but their range of possible values is restricted and even
	then they do not allow for the packing and unpacking of pixel data in a
	fully arbitrary manner.
	
	Consider this simple example:
	
	    Consider a column of pixels in memory.  The pixels are of GL_RGB 
	    format and GL_UNSIGNED_BYTE type resulting in 3 bytes per pixel.
	    Now consider that this column of pixel data was arranged in memory
	    such that each row of the image (in this case each pixel) has two
	    bytes padding or space between them.
	
	    Each row of 1 pixel then has 5 bytes.  An attempting to express this
	    memory arrangement with existing pixel storage semantics would
	    naturally start with a GL_UNPACK_ROW_LENGTH of 1 because there is
	    one pixel per row.  However, no valid value of GL_UNPACK_ALIGNMENT,
	    1, 2, 4, or 8, will allow the proper row padding to express this 
	    memory arrangement.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/APPLE/row_bytes.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.APPLE.row_bytes import *
from OpenGL.raw.GL.APPLE.row_bytes import _EXTENSION_NAME

def glInitRowBytesAPPLE():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION