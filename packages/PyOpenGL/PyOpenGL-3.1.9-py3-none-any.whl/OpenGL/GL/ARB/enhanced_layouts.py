'''OpenGL extension ARB.enhanced_layouts

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.enhanced_layouts to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension adds the following functionality to layout qualifiers,
	including broadening the API where this functionality is reflected.
	
	The following are added:
	
	1) Use compile-time constant expressions. E.g.,
	
	      const int start = 6;
	      layout(location = start + 2) int vec4 v;
	
	2) Specify explicit byte offsets within a uniform or shader storage block.
	   For example, if you want two vec4 variables "batman" and "robin" to
	   appear at byte offsets 0 and 64 in your block, you can say:
	
	      uniform Block {
	        layout(offset = 0) vec4 batman;
	        layout(offset = 64) vec4 robin;
	      };
	
	3) Force alignment within a uniform or shader storage block.  The previous
	   example could also be expressed:
	
	      uniform Block {
	        vec4 batman;
	        layout(align = 64) vec4 robin;
	      };
	
	   This says the member 'robin' must start at the next address that is a
	   multiple of 64.  It allows constructing the same layout in C and in GLSL
	   without inventing explicit offsets.
	
	   Explicit offsets and aligned offsets can be combined:
	
	      uniform Block {
	        vec4 batman;
	        layout(offset = 44, align = 8) vec4 robin;
	      };
	
	   would make 'robin' be at the first 8-byte aligned address, starting at
	   44, which is 48.  This is more useful when using the *align* at
	   the block level, which will apply to all members.
	
	4) Specify component numbers to more fully utilize the vec4-slot interfaces
	   between shader outputs and shader inputs.
	
	   For example, you could fit the following
	
	      - an array of 32 vec3
	      - a single float
	
	   into the space of 32 vec4 slots using the following code:
	
	      // consume X/Y/Z components of 32 vectors
	      layout(location = 0) in vec3 batman[32];
	
	      // consumes W component of first vector
	      layout(location = 0, component = 3) in float robin;
	
	   Further, an array of vec3 and an array of float can be stored
	   interleaved, using the following.
	
	      // consumes W component of 32 vectors
	      layout(location = 0, component = 3) in float robin[32];
	
	      // consume X/Y/Z components of 32 vectors
	      layout(location = 0) in vec3 batman[32];
	
	5) Specify transform/feedback buffers, locations, and widths. For example:
	
	       layout(xfb_buffer = 0, xfb_offset = 0)  out vec3 var1;
	       layout(xfb_buffer = 0, xfb_offset = 24) out vec3 var2;
	       layout(xfb_buffer = 1, xfb_offset = 0)  out vec4 var3;
	
	   The second line above says to write var2 out to byte offset 24 of
	   transform/feedback buffer 0.  (When doing this, output are only
	   captured when xfb_offset is used.)
	
	   To specify the total number of bytes per entry in a buffer:
	
	       layout(xfb_buffer = 1, xfb_stride = 32) out;
	
	   This is necessary if, say, var3 above, which uses bytes 0-11,
	   does not fully fill the buffer, which in this case takes 32 bytes.
	
	   Use of this feature effectively eliminates the need to use previously
	   existing API commands to describe the transform feedback layout.
	
	6) Allow locations on input and output blocks for SSO interface matching.
	
	   For example:
	
	      layout(location = 4) in block {
	          vec4 batman;   // gets location 4
	          vec4 robin;    // gets location 5
	          layout(location = 7) vec4 joker;  // gets location 7
	          vec4 riddler;  // location 8
	      };

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/enhanced_layouts.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.ARB.enhanced_layouts import *
from OpenGL.raw.GL.ARB.enhanced_layouts import _EXTENSION_NAME

def glInitEnhancedLayoutsARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION