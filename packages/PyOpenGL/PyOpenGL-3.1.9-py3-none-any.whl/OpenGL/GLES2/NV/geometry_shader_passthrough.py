'''OpenGL extension NV.geometry_shader_passthrough

This module customises the behaviour of the 
OpenGL.raw.GLES2.NV.geometry_shader_passthrough to provide a more 
Python-friendly API

Overview (from the spec)
	
	Geometry shaders provide the ability for applications to process each
	primitive sent through the GL using a programmable shader.  While geometry
	shaders can be used to perform a number of different operations, including
	subdividing primitives and changing primitive type, one common use case
	treats geometry shaders as largely "passthrough".  In this use case, the
	bulk of the geometry shader code simply copies inputs from each vertex of
	the input primitive to corresponding outputs in the vertices of the output
	primitive.  Such shaders might also compute values for additional built-in
	or user-defined per-primitive attributes (e.g., gl_Layer) to be assigned
	to all the vertices of the output primitive.
	
	This extension provides a shading language abstraction to express such
	shaders without requiring explicit logic to manually copy attributes from
	input vertices to output vertices.  For example, consider the following
	simple geometry shader in unextended OpenGL:
	
	  layout(triangles) in;
	  layout(triangle_strip) out;
	  layout(max_vertices=3) out;
	
	  in Inputs {
	    vec2 texcoord;
	    vec4 baseColor;
	  } v_in[];
	  out Outputs {
	    vec2 texcoord;
	    vec4 baseColor;
	  };
	
	  void main()
	  {
	    int layer = compute_layer();
	    for (int i = 0; i < 3; i++) {
	      gl_Position = gl_in[i].gl_Position;
	      texcoord = v_in[i].texcoord;
	      baseColor = v_in[i].baseColor;
	      gl_Layer = layer;
	      EmitVertex();
	    }
	  }
	
	In this shader, the inputs "gl_Position", "Inputs.texcoord", and
	"Inputs.baseColor" are simply copied from the input vertex to the
	corresponding output vertex.  The only "interesting" work done by the
	geometry shader is computing and emitting a gl_Layer value for the
	primitive.
	
	The following geometry shader, using this extension, is equivalent:
	
	  #extension GL_NV_geometry_shader_passthrough : require
	
	  layout(triangles) in;
	  // No output primitive layout qualifiers required.
	
	  // Redeclare gl_PerVertex to pass through "gl_Position".
	  layout(passthrough) in gl_PerVertex {
	    vec4 gl_Position;
	  } gl_in[];
	
	  // Declare "Inputs" with "passthrough" to automatically copy members.
	  layout(passthrough) in Inputs {
	    vec2 texcoord;
	    vec4 baseColor;
	  } v_in[];
	
	  // No output block declaration required.
	
	  void main()
	  {
	    // The shader simply computes and writes gl_Layer.  We don't
	    // loop over three vertices or call EmitVertex().
	    gl_Layer = compute_layer();
	  }

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/geometry_shader_passthrough.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.NV.geometry_shader_passthrough import *
from OpenGL.raw.GLES2.NV.geometry_shader_passthrough import _EXTENSION_NAME

def glInitGeometryShaderPassthroughNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION