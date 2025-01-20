'''OpenGL extension ARB.sync

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.sync to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension introduces the concept of "sync objects". Sync
	objects are a synchronization primitive - a representation of events
	whose completion status can be tested or waited upon. One specific
	type of sync object, the "fence sync object", is supported in this
	extension, and additional types can easily be added in the future.
	
	Fence sync objects have corresponding fences, which are inserted
	into the OpenGL command stream at the time the sync object is
	created. A sync object can be queried for a given condition. The
	only condition supported for fence sync objects is completion of the
	corresponding fence command. Fence completion allows applications to
	request a partial Finish, wherein all commands prior to the fence
	will be forced to complete before control is returned to the calling
	process.
	
	These new mechanisms allow for synchronization between the host CPU
	and the GPU, which may be accessing the same resources (typically
	memory), as well as between multiple GL contexts bound to multiple
	threads in the host CPU.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/sync.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.ARB.sync import *
from OpenGL.raw.GL.ARB.sync import _EXTENSION_NAME

def glInitSyncARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

glGetInteger64v=wrapper.wrapper(glGetInteger64v).setOutput(
    'data',size=_glgets._glget_size_mapping,pnameArg='pname',orPassIn=True
)
glGetSynciv=wrapper.wrapper(glGetSynciv).setOutput(
    'length',size=(1,),orPassIn=True
).setOutput(
    'values',size=lambda x:(x,),pnameArg='count',orPassIn=True
)
### END AUTOGENERATED SECTION
from OpenGL.raw.GL._types import GLint
from OpenGL.arrays import GLintArray

def glGetSync( sync, pname, bufSize=1,length=None,values=None ):
    """Wrapper around glGetSynciv that auto-allocates buffers
    
    sync -- the GLsync struct pointer (see glGetSynciv)
    pname -- constant to retrieve (see glGetSynciv)
    bufSize -- defaults to 1, maximum number of items to retrieve,
        currently all constants are defined to return a single 
        value 
    length -- None or a GLint() instance (ONLY!), must be a byref()
        capable object with a .value attribute which retrieves the 
        set value
    values -- None or an array object, if None, will be a default 
        return-array-type of length bufSize
    
    returns values[:length.value], i.e. an array with the values set 
    by the call, currently always a single-value array.
    """
    if values is None:
        values = GLintArray.zeros( (bufSize,) )
    if length is None:
        length = GLint()
    glGetSynciv( sync, pname, bufSize, length, values )
    written = length.value 
    return values[:written]
