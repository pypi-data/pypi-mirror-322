'''OpenGL extension ARB.fragment_coord_conventions

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.fragment_coord_conventions to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension provides alternative conventions for the fragment
	coordinate XY location available for programmable fragment processing.
	
	The scope of this extension deals *only* with how the fragment
	coordinate XY location appears during programming fragment processing.
	Beyond the scope of this extension are coordinate conventions used
	for rasterization or transformation.
	
	In the case of the coordinate conventions for rasterization and
	transformation, some combination of the viewport, depth range, culling
	state, and projection matrix state can be reconfigured to adopt other
	arbitrary clip-space and window-space coordinate space conventions.
	Adopting other clip-space and window-space conventions involves
	adjusting existing OpenGL state.  However it is non-trivial to massage
	an arbitrary fragment shader or program to adopt a different
	window-space coordinate system because such shaders are encoded in
	various textual representations.
	
	The dominant 2D and 3D rendering APIs make two basic choices of
	convention when locating fragments in window space.
	
	The two choices are:
	
	1)  Is the origin nearest the lower-left- or upper-left-most pixel
	    of the window?
	
	2)  Is the (x,y) location of the pixel nearest the origin at (0,0)
	    or (0.5,0.5)?
	
	OpenGL assumes a lower-left origin for window coordinates and assumes
	pixel centers are located at half-pixel coordinates.  This means
	the XY location (0.5,0.5) corresponds to the lower-left-most pixel
	in a window.
	
	Other window coordinate conventions exist for other rendering APIs.
	X11, GDI, and Direct3D version through DirectX 9 assume an upper-left
	window origin and locate pixel centers at integer XY values.
	By this alternative convention, the XY location (0,0) corresponds
	to the upper-left-most pixel in a window.
	
	Direct3D for DirectX 10 assumes an upper-left origin (as do prior
	DirectX versions) yet assumes half-pixel coordinates (unlike prior
	DirectX versions).  By the DirectX 10 convention, the XY location
	(0.5,0.5) corresponds to the upper-left-most pixel in a window.
	
	Fragment shaders can directly access the location of a given
	processed fragment in window space.  We call this location the
	"fragment coordinate".
	
	This extension provides a means for fragment shaders written in GLSL
	or OpenGL assembly extensions to specify alternative conventions
	for determining the fragment coordinate value accessed during
	programmable fragment processing.
	
	The motivation for this extension is to provide an easy, efficient
	means for fragment shaders accessing a fragment's window-space
	location to adopt the fragment coordinate convention for which the
	shader was originally written.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/fragment_coord_conventions.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.ARB.fragment_coord_conventions import *
from OpenGL.raw.GL.ARB.fragment_coord_conventions import _EXTENSION_NAME

def glInitFragmentCoordConventionsARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION