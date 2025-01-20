'''OpenGL extension AMD.name_gen_delete

This module customises the behaviour of the 
OpenGL.raw.GL.AMD.name_gen_delete to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension simply creates 2 new entry-points that name generic
	creation and deletion of names.  The intent is to go away from API
	functionality that provides a create/delete function for each specific 
	object.  
	
	For example: 
	    glGenTextures/glDeleteTextures/glIsTexture
	    glGenBuffers/glDeleteBuffers/IsBuffer
	    glGenFramebuffers/glDeleteFramebuffers/IsFramebuffer
	
	Instead, everything is created using one entry-point GenNamesAMD and
	everything is now deleted with another entry-point DeleteNamesAMD with
	the appropriate identifier set.  In addition, everything can now be 
	queried with IsNameAMD.
	
	This alleviates the problem we may eventually encounter where we have
	many Gen/Delete/Is functions where 3 might suffice.  All that is needed
	in the new case is to add a valid identifier to the accepted parameters
	list.
	

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/AMD/name_gen_delete.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.AMD.name_gen_delete import *
from OpenGL.raw.GL.AMD.name_gen_delete import _EXTENSION_NAME

def glInitNameGenDeleteAMD():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

glGenNamesAMD=wrapper.wrapper(glGenNamesAMD).setOutput(
    'names',size=lambda x:(x,),pnameArg='num',orPassIn=True
)
# INPUT glDeleteNamesAMD.names size not checked against num
glDeleteNamesAMD=wrapper.wrapper(glDeleteNamesAMD).setInputArraySize(
    'names', None
)
### END AUTOGENERATED SECTION