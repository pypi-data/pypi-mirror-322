'''OpenGL extension ARB.framebuffer_sRGB

This module customises the behaviour of the 
OpenGL.raw.WGL.ARB.framebuffer_sRGB to provide a more 
Python-friendly API

Overview (from the spec)
	
	Conventionally, OpenGL assumes framebuffer color components are stored
	in a linear color space.  In particular, framebuffer blending is a
	linear operation.
	
	The sRGB color space is based on typical (non-linear) monitor
	characteristics expected in a dimly lit office.  It has been
	standardized by the International Electrotechnical Commission (IEC)
	as IEC 61966-2-1. The sRGB color space roughly corresponds to 2.2
	gamma correction.
	
	This extension adds a framebuffer capability for sRGB framebuffer
	update and blending.  When blending is disabled but the new sRGB
	updated mode is enabled (assume the framebuffer supports the
	capability), high-precision linear color component values for red,
	green, and blue generated by fragment coloring are encoded for sRGB
	prior to being written into the framebuffer.  When blending is enabled
	along with the new sRGB update mode, red, green, and blue framebuffer
	color components are treated as sRGB values that are converted to
	linear color values, blended with the high-precision color values
	generated by fragment coloring, and then the blend result is encoded
	for sRGB just prior to being written into the framebuffer.
	
	The primary motivation for this extension is that it allows OpenGL
	applications to render into a framebuffer that is scanned to a monitor
	configured to assume framebuffer color values are sRGB encoded.
	This assumption is roughly true of most PC monitors with default
	gamma correction.  This allows applications to achieve faithful
	color reproduction for OpenGL rendering without adjusting the
	monitor's gamma correction.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/framebuffer_sRGB.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.WGL import _types, _glgets
from OpenGL.raw.WGL.ARB.framebuffer_sRGB import *
from OpenGL.raw.WGL.ARB.framebuffer_sRGB import _EXTENSION_NAME

def glInitFramebufferSrgbARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION