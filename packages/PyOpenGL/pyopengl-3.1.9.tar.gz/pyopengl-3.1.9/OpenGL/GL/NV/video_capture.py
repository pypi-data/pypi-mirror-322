'''OpenGL extension NV.video_capture

This module customises the behaviour of the 
OpenGL.raw.GL.NV.video_capture to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension provides a mechanism for streaming video data
	directly into texture objects and buffer objects.  Applications can
	then display video streams in interactive 3D scenes and/or
	manipulate the video data using the GL's image processing
	capabilities.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/video_capture.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.NV.video_capture import *
from OpenGL.raw.GL.NV.video_capture import _EXTENSION_NAME

def glInitVideoCaptureNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

glGetVideoCaptureivNV=wrapper.wrapper(glGetVideoCaptureivNV).setOutput(
    'params',size=_glgets._glget_size_mapping,pnameArg='pname',orPassIn=True
)
glGetVideoCaptureStreamivNV=wrapper.wrapper(glGetVideoCaptureStreamivNV).setOutput(
    'params',size=_glgets._glget_size_mapping,pnameArg='pname',orPassIn=True
)
glGetVideoCaptureStreamfvNV=wrapper.wrapper(glGetVideoCaptureStreamfvNV).setOutput(
    'params',size=_glgets._glget_size_mapping,pnameArg='pname',orPassIn=True
)
glGetVideoCaptureStreamdvNV=wrapper.wrapper(glGetVideoCaptureStreamdvNV).setOutput(
    'params',size=_glgets._glget_size_mapping,pnameArg='pname',orPassIn=True
)
# glVideoCaptureNV.capture_time is OUTPUT without known output size
# glVideoCaptureNV.sequence_num is OUTPUT without known output size
# INPUT glVideoCaptureStreamParameterivNV.params size not checked against 'pname'
glVideoCaptureStreamParameterivNV=wrapper.wrapper(glVideoCaptureStreamParameterivNV).setInputArraySize(
    'params', None
)
# INPUT glVideoCaptureStreamParameterfvNV.params size not checked against 'pname'
glVideoCaptureStreamParameterfvNV=wrapper.wrapper(glVideoCaptureStreamParameterfvNV).setInputArraySize(
    'params', None
)
# INPUT glVideoCaptureStreamParameterdvNV.params size not checked against 'pname'
glVideoCaptureStreamParameterdvNV=wrapper.wrapper(glVideoCaptureStreamParameterdvNV).setInputArraySize(
    'params', None
)
### END AUTOGENERATED SECTION