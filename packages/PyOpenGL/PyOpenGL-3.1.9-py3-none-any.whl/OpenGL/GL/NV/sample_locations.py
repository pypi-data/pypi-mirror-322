'''OpenGL extension NV.sample_locations

This module customises the behaviour of the 
OpenGL.raw.GL.NV.sample_locations to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension allows an application to modify the locations of samples
	within a pixel used in multisample rasterization.  Additionally, it allows
	applications to specify different sample locations for each pixel in a
	group of adjacent pixels, which may increase antialiasing quality
	(particularly if a custom resolve shader is used that takes advantage of
	these different locations).
	
	It is common for implementations to optimize the storage of depth values
	by storing values that can be used to reconstruct depth at each sample
	location, rather than storing separate depth values for each sample. For
	example, the depth values from a single triangle can be represented using
	plane equations.  When the depth value for a sample is needed, it is
	automatically evaluated at the sample location. Modifying the sample
	locations causes the reconstruction to no longer evaluate the same depth
	values as when the samples were originally generated.  This extension
	provides a command to "resolve" and store per-sample depth values using
	the currently programmed sample locations, which allows the application to
	manage this issue if/when necessary.
	
	The programmable sample locations are used during rasterization and for
	evaluation of depth functions during normal geometric rendering. The
	programmable locations are associated with a framebuffer object rather
	than an individual depth buffer, so if the depth buffer is used as a
	texture the texture sampling may be done at the standard sample
	locations. Additionally, commands that do not render geometric primitives
	(e.g. ReadPixels, BlitFramebuffer, CopyTexSubImage2D, etc.) may use the
	standard sample locations to resolve depth functions rather than the
	programmable locations. If a single depth buffer is used at different
	times with different sample locations, the depth functions may be
	interpreted using the current sample locations.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/sample_locations.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.NV.sample_locations import *
from OpenGL.raw.GL.NV.sample_locations import _EXTENSION_NAME

def glInitSampleLocationsNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION