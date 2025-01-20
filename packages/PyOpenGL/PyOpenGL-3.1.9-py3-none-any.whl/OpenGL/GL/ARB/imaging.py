'''OpenGL extension ARB.imaging

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.imaging to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/imaging.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.ARB.imaging import *
from OpenGL.raw.GL.ARB.imaging import _EXTENSION_NAME

def glInitImagingARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# INPUT glColorTable.table size not checked against 'format,type,width'
glColorTable=wrapper.wrapper(glColorTable).setInputArraySize(
    'table', None
)
# INPUT glColorTableParameterfv.params size not checked against 'pname'
glColorTableParameterfv=wrapper.wrapper(glColorTableParameterfv).setInputArraySize(
    'params', None
)
# INPUT glColorTableParameteriv.params size not checked against 'pname'
glColorTableParameteriv=wrapper.wrapper(glColorTableParameteriv).setInputArraySize(
    'params', None
)
# OUTPUT glGetColorTable.table COMPSIZE(target, format, type) 
glGetColorTableParameterfv=wrapper.wrapper(glGetColorTableParameterfv).setOutput(
    'params',size=_glgets._glget_size_mapping,pnameArg='pname',orPassIn=True
)
glGetColorTableParameteriv=wrapper.wrapper(glGetColorTableParameteriv).setOutput(
    'params',size=_glgets._glget_size_mapping,pnameArg='pname',orPassIn=True
)
# INPUT glColorSubTable.data size not checked against 'format,type,count'
glColorSubTable=wrapper.wrapper(glColorSubTable).setInputArraySize(
    'data', None
)
# INPUT glConvolutionFilter1D.image size not checked against 'format,type,width'
glConvolutionFilter1D=wrapper.wrapper(glConvolutionFilter1D).setInputArraySize(
    'image', None
)
# INPUT glConvolutionFilter2D.image size not checked against 'format,type,width,height'
glConvolutionFilter2D=wrapper.wrapper(glConvolutionFilter2D).setInputArraySize(
    'image', None
)
# INPUT glConvolutionParameterfv.params size not checked against 'pname'
glConvolutionParameterfv=wrapper.wrapper(glConvolutionParameterfv).setInputArraySize(
    'params', None
)
# INPUT glConvolutionParameteriv.params size not checked against 'pname'
glConvolutionParameteriv=wrapper.wrapper(glConvolutionParameteriv).setInputArraySize(
    'params', None
)
# OUTPUT glGetConvolutionFilter.image COMPSIZE(target, format, type) 
glGetConvolutionParameterfv=wrapper.wrapper(glGetConvolutionParameterfv).setOutput(
    'params',size=_glgets._glget_size_mapping,pnameArg='pname',orPassIn=True
)
glGetConvolutionParameteriv=wrapper.wrapper(glGetConvolutionParameteriv).setOutput(
    'params',size=_glgets._glget_size_mapping,pnameArg='pname',orPassIn=True
)
# OUTPUT glGetSeparableFilter.column COMPSIZE(target, format, type) 
# OUTPUT glGetSeparableFilter.row COMPSIZE(target, format, type) 
# OUTPUT glGetSeparableFilter.span COMPSIZE(target, format, type) 
# INPUT glSeparableFilter2D.column size not checked against 'target,format,type,height'
# INPUT glSeparableFilter2D.row size not checked against 'target,format,type,width'
glSeparableFilter2D=wrapper.wrapper(glSeparableFilter2D).setInputArraySize(
    'column', None
).setInputArraySize(
    'row', None
)
# OUTPUT glGetHistogram.values COMPSIZE(target, format, type) 
glGetHistogramParameterfv=wrapper.wrapper(glGetHistogramParameterfv).setOutput(
    'params',size=_glgets._glget_size_mapping,pnameArg='pname',orPassIn=True
)
glGetHistogramParameteriv=wrapper.wrapper(glGetHistogramParameteriv).setOutput(
    'params',size=_glgets._glget_size_mapping,pnameArg='pname',orPassIn=True
)
# OUTPUT glGetMinmax.values COMPSIZE(target, format, type) 
glGetMinmaxParameterfv=wrapper.wrapper(glGetMinmaxParameterfv).setOutput(
    'params',size=_glgets._glget_size_mapping,pnameArg='pname',orPassIn=True
)
glGetMinmaxParameteriv=wrapper.wrapper(glGetMinmaxParameteriv).setOutput(
    'params',size=_glgets._glget_size_mapping,pnameArg='pname',orPassIn=True
)
### END AUTOGENERATED SECTION
from OpenGL.GL import images
from OpenGL.lazywrapper import lazy as _lazy
glColorTable = images.setDimensionsAsInts(
    images.setImageInput(
        glColorTable,
        pixelName = 'table',
        typeName = 'type',
    )
)
glColorSubTable = images.setDimensionsAsInts(
    images.setImageInput(
        glColorSubTable,
        pixelName = 'data',
    )
)
glSeparableFilter2D = images.setDimensionsAsInts(
    images.setImageInput(
        images.setImageInput(
            glSeparableFilter2D,
            pixelName = 'row',
            typeName = 'type',
        ),
        pixelName = 'column',
        typeName = 'type',
    )
)
glConvolutionFilter1D = images.setDimensionsAsInts(
    images.setImageInput(
        glConvolutionFilter1D,
        pixelName = 'image',
        typeName = 'type',
    )
)
glConvolutionFilter2D = images.setDimensionsAsInts(
    images.setImageInput(
        glConvolutionFilter2D,
        pixelName = 'image',
        typeName = 'type',
    )
)

@_lazy( glGetConvolutionFilter )
def glGetConvolutionFilter( baseFunction, target, format, type ):
    """Retrieve 1 or 2D convolution parameter "kernels" as pixel data"""
    dims = (
        glGetConvolutionParameteriv( target, GL_CONVOLUTION_WIDTH )[0],
    )
    if target != GL_CONVOLUTION_1D:
        dims += (
            glGetConvolutionParameteriv( target, GL_CONVOLUTION_HEIGHT )[0],
        )
    # is it always 4?  Seems to be, but the spec/man-page isn't really clear about it...
    dims += (4,)
    array = images.images.SetupPixelRead( format, dims, type )
    arrayType = arrays.GL_CONSTANT_TO_ARRAY_TYPE[
        images.images.TYPE_TO_ARRAYTYPE.get(type,type)
    ]
    baseFunction(
        target, format, type,
        ctypes.c_void_p( arrayType.dataPointer(array))
    )
    return array
@_lazy( glGetSeparableFilter )
def glGetSeparableFilter( baseFunction, target, format, type ):
    """Retrieve 2 1D convolution parameter "kernels" as pixel data"""
    rowDims = (
        glGetConvolutionParameteriv( GL_CONVOLUTION_WIDTH )[0],
        4,
    )
    columnDims = (
        glGetConvolutionParameteriv( GL_CONVOLUTION_HEIGHT )[0],
        4,
    )
    arrayType = arrays.GL_CONSTANT_TO_ARRAY_TYPE[
        images.images.TYPE_TO_ARRAYTYPE.get(type,type)
    ]
    row = images.images.SetupPixelRead( format, rowDims, type )
    column = images.images.SetupPixelRead( format, columnDims, type )
    baseFunction(
        target, format, type,
        ctypes.c_void_p( arrayType.dataPointer(row)),
        ctypes.c_void_p( arrayType.dataPointer(column)),
        None # span
    )
    return row, column
@_lazy( glGetColorTable )
def glGetColorTable( baseFunction, target, format, type ):
    """Retrieve the current 1D color table as a bitmap"""
    dims = (
        glGetColorTableParameteriv(target, GL_COLOR_TABLE_WIDTH),
        4, # Grr, spec *seems* to say that it's different sizes, but it doesn't really say...
    )
    array = images.images.SetupPixelRead( format, dims, type )
    arrayType = arrays.GL_CONSTANT_TO_ARRAY_TYPE[
        images.images.TYPE_TO_ARRAYTYPE.get(type,type)
    ]
    baseFunction(
        target, format, type,
        ctypes.c_void_p( arrayType.dataPointer(array))
    )
    return array
@_lazy( glGetHistogram )
def glGetHistogram( baseFunction, target, reset, format, type, values=None):
    """Retrieve current 1D histogram as a 1D bitmap"""
    if values is None:
        width = glGetHistogramParameteriv(
            target,
            GL_HISTOGRAM_WIDTH,
        )
        values = images.images.SetupPixelRead( format, (width,4), type )
    arrayType = arrays.GL_CONSTANT_TO_ARRAY_TYPE[
        images.images.TYPE_TO_ARRAYTYPE.get(type,type)
    ]
    baseFunction(
        target, reset, format, type,
        ctypes.c_void_p( arrayType.dataPointer(values))
    )
    return values

@_lazy( glGetMinmax )
def glGetMinmax( baseFunction, target, reset, format, type, values=None):
    """Retrieve minimum and maximum values as a 2-element image"""
    if values is None:
        width = 2
        values = images.images.SetupPixelRead( format, (width,4), type )
    arrayType = arrays.GL_CONSTANT_TO_ARRAY_TYPE[
        images.images.TYPE_TO_ARRAYTYPE.get(type,type)
    ]
    baseFunction(
        target, reset, format, type,
        ctypes.c_void_p( arrayType.dataPointer(values))
    )
    return values
