'''OpenGL extension EXT.primitive_bounding_box

This module customises the behaviour of the 
OpenGL.raw.GLES2.EXT.primitive_bounding_box to provide a more 
Python-friendly API

Overview (from the spec)
	
	On tile-based architectures, transformed primitives are generally written
	out to memory before rasterization, and then read back from memory for each
	tile they intersect. When geometry expands during transformation due to
	tessellation or one-to-many geometry shaders, the external bandwidth
	required grows proportionally. This extension provides a way for
	implementations to know which tiles incoming geometry will intersect before
	fully transforming (and expanding) the geometry. This allows them to only
	store the unexpanded geometry in memory, and perform expansion on-chip for
	each intersected tile.
	
	New state is added to hold an axis-aligned bounding box which is assumed to
	contain any geometry submitted. An implementation is allowed to ignore any
	portions of primitives outside the bounding box; thus if a primitive extends
	outside of a tile into a neighboring tile that the bounding box didn't
	intersect, the implementation is not required to render those portions. The
	tessellation control shader is optionally able to specify a per-patch
	bounding box that overrides the bounding box state for primitives generated
	from that patch, in order to provide tighter bounds.
	
	The typical usage is that an application will have an object-space bounding
	volume for a primitive or group of primitives, either calculated at runtime
	or provided with the mesh by the authoring tool or content pipeline. It will
	transform this volume to clip space, compute an axis-aligned bounding box
	that contains the transformed bounding volume, and provide that at either
	per-patch or per-draw granularity.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/primitive_bounding_box.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.EXT.primitive_bounding_box import *
from OpenGL.raw.GLES2.EXT.primitive_bounding_box import _EXTENSION_NAME

def glInitPrimitiveBoundingBoxEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION