'''OpenGL extension NV.command_list

This module customises the behaviour of the 
OpenGL.raw.GL.NV.command_list to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension adds a few new features designed to provide very low 
	overhead batching and replay of rendering commands and state changes:
	
	- A state object, which stores a pre-validated representation of the
	  the state of (almost) the entire pipeline.
	
	- A more flexible and extensible MultiDrawIndirect (MDI) type of mechanism, using
	  a token-based command stream, allowing to setup binding state and emit draw calls.
	
	- A set of functions to execute a list of the token-based command streams with state object
	  changes interleaved with the streams.
	
	- Command lists enabling compilation and reuse of sequences of command
	  streams and state object changes.
	
	Because state objects reflect the state of the entire pipeline, it is 
	expected that they can be pre-validated and executed efficiently. It is 
	also expected that when state objects are combined into a command list,
	the command list can diff consecutive state objects to produce a reduced/
	optimized set of state changes specific to that transition.
	
	The token-based command stream can also be stored in regular buffer objects
	and therefore be modified by the server itself. This allows more 
	complex work creation than the original MDI approach, which was limited
	to emitting draw calls only.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/command_list.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.NV.command_list import *
from OpenGL.raw.GL.NV.command_list import _EXTENSION_NAME

def glInitCommandListNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# INPUT glCreateStatesNV.states size not checked against n
glCreateStatesNV=wrapper.wrapper(glCreateStatesNV).setInputArraySize(
    'states', None
)
# INPUT glDeleteStatesNV.states size not checked against n
glDeleteStatesNV=wrapper.wrapper(glDeleteStatesNV).setInputArraySize(
    'states', None
)
# INPUT glCreateCommandListsNV.lists size not checked against n
glCreateCommandListsNV=wrapper.wrapper(glCreateCommandListsNV).setInputArraySize(
    'lists', None
)
# INPUT glDeleteCommandListsNV.lists size not checked against n
glDeleteCommandListsNV=wrapper.wrapper(glDeleteCommandListsNV).setInputArraySize(
    'lists', None
)
# INPUT glListDrawCommandsStatesClientNV.fbos size not checked against count
# INPUT glListDrawCommandsStatesClientNV.indirects size not checked against count
# INPUT glListDrawCommandsStatesClientNV.sizes size not checked against count
# INPUT glListDrawCommandsStatesClientNV.states size not checked against count
glListDrawCommandsStatesClientNV=wrapper.wrapper(glListDrawCommandsStatesClientNV).setInputArraySize(
    'fbos', None
).setInputArraySize(
    'indirects', None
).setInputArraySize(
    'sizes', None
).setInputArraySize(
    'states', None
)
### END AUTOGENERATED SECTION