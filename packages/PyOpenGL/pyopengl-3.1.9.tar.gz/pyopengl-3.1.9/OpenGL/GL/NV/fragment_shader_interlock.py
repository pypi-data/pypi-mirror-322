'''OpenGL extension NV.fragment_shader_interlock

This module customises the behaviour of the 
OpenGL.raw.GL.NV.fragment_shader_interlock to provide a more 
Python-friendly API

Overview (from the spec)
	
	In unextended OpenGL 4.3 or OpenGL ES 3.1, applications may produce a
	large number of fragment shader invocations that perform loads and
	stores to memory using image uniforms, atomic counter uniforms,
	buffer variables, or pointers. The order in which loads and stores
	to common addresses are performed by different fragment shader
	invocations is largely undefined.  For algorithms that use shader
	writes and touch the same pixels more than once, one or more of the
	following techniques may be required to ensure proper execution ordering:
	
	  * inserting Finish or WaitSync commands to drain the pipeline between
	    different "passes" or "layers";
	
	  * using only atomic memory operations to write to shader memory (which
	    may be relatively slow and limits how memory may be updated); or
	
	  * injecting spin loops into shaders to prevent multiple shader
	    invocations from touching the same memory concurrently.
	
	This extension provides new GLSL built-in functions
	beginInvocationInterlockNV() and endInvocationInterlockNV() that delimit a
	critical section of fragment shader code.  For pairs of shader invocations
	with "overlapping" coverage in a given pixel, the OpenGL implementation
	will guarantee that the critical section of the fragment shader will be
	executed for only one fragment at a time.
	
	There are four different interlock modes supported by this extension,
	which are identified by layout qualifiers.  The qualifiers
	"pixel_interlock_ordered" and "pixel_interlock_unordered" provides mutual
	exclusion in the critical section for any pair of fragments corresponding
	to the same pixel.  When using multisampling, the qualifiers
	"sample_interlock_ordered" and "sample_interlock_unordered" only provide
	mutual exclusion for pairs of fragments that both cover at least one
	common sample in the same pixel; these are recommended for performance if
	shaders use per-sample data structures.
	
	Additionally, when the "pixel_interlock_ordered" or
	"sample_interlock_ordered" layout qualifier is used, the interlock also
	guarantees that the critical section for multiple shader invocations with
	"overlapping" coverage will be executed in the order in which the
	primitives were processed by the GL.  Such a guarantee is useful for
	applications like blending in the fragment shader, where an application
	requires that fragment values to be composited in the framebuffer in
	primitive order.
	
	This extension can be useful for algorithms that need to access per-pixel
	data structures via shader loads and stores.  Such algorithms using this
	extension can access such data structures in the critical section without
	worrying about other invocations for the same pixel accessing the data
	structures concurrently.  Additionally, the ordering guarantees are useful
	for cases where the API ordering of fragments is meaningful.  For example,
	applications may be able to execute programmable blending operations in
	the fragment shader, where the destination buffer is read via image loads
	and the final value is written via image stores.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/fragment_shader_interlock.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.NV.fragment_shader_interlock import *
from OpenGL.raw.GL.NV.fragment_shader_interlock import _EXTENSION_NAME

def glInitFragmentShaderInterlockNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION