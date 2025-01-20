'''OpenGL extension AMD.compressed_3DC_texture

This module customises the behaviour of the 
OpenGL.raw.GLES2.AMD.compressed_3DC_texture to provide a more 
Python-friendly API

Overview (from the spec)
	
	Two compression formats are introduced:
	
	- A compression format for two component textures.  When used to store 
	  normal vectors, the two components are commonly used with a fragment 
	  shader that derives the third component.
	
	- A compression format for single component textures.  The single component
	  may be used as a luminance or an alpha value.
	
	There are a large number of games that use luminance only and/or alpha only 
	textures.  For example, monochrome light maps used in a few popular games 
	are 8-bit luminance textures.  This extension describes a compression format
	that provides a 2:1 compression ratio for 8-bit single channel textures.
	
	Normal maps are special textures that are used to add detail to 3D surfaces.
	They are an extension of earlier "bump map" textures, which contained per-
	pixel height values and were used to create the appearance of bumpiness on 
	otherwise smooth surfaces.  Normal maps contain more detailed surface 
	information, allowing them to represent much more complex shapes.
	
	Normal mapping is one of the key features that makes the current generation
	of games look so much better than earlier titles.  A limitation to the 
	effectiveness of this technique is the size of the textures required.  In an 
	ideal case where every surface has both a color texture map and a normal 
	texture map, the texture memory and bandwidth requirements would double 
	compared to using color maps alone.
	
	In fact, the problem is much worse because existing block based compression
	methods such as DXTc, ETC, and S3TC are ineffective at compressing normal 
	maps.  They tend to have trouble capturing the small edges and subtle 
	curvature that normal maps are designed to capture, and they also introduce 
	unsightly block artifacts.
	
	Because normal maps are used to capture light reflections and realistic 
	surface highlights, these problems are amplified relative to their impact on
	color textures.  The results are sufficiently poor that game artists and 
	developers would rather not use normal map compression at all on most 
	surfaces, and instead limit themselves to lower resolution maps on selected 
	parts of the rendered scene.
	
	3DC provides an ideal solution to the normal map compression problem.  It 
	provides up to 4:1 compression of normal maps, with image quality that is 
	virtually indistinguishable from the uncompressed version.  The technique is
	hardware accelerated, so the performance impact is minimal.  Thus, 
	developers are freed to use higher resolution, more detailed normal maps, 
	and/or use them on all of the objects in a scene rather than just a select 
	few.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/AMD/compressed_3DC_texture.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.AMD.compressed_3DC_texture import *
from OpenGL.raw.GLES2.AMD.compressed_3DC_texture import _EXTENSION_NAME

def glInitCompressed3DcTextureAMD():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION