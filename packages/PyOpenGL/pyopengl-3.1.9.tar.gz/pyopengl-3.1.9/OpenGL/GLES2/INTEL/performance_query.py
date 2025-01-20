'''OpenGL extension INTEL.performance_query

This module customises the behaviour of the 
OpenGL.raw.GLES2.INTEL.performance_query to provide a more 
Python-friendly API

Overview (from the spec)
	
	The purpose of this extension is to expose Intel proprietary hardware
	performance counters to the OpenGL applications. Performance counters may
	count:
	
	- number of hardware events such as number of spawned vertex shaders. In
	  this case the results represent the number of events.
	
	- duration of certain activity, like time took by all fragment shader
	  invocations. In that case the result usually represents the number of
	  clocks in which the particular HW unit was busy. In order to use such
	  counter efficiently, it should be normalized to the range of <0,1> by
	  dividing its value by the number of render clocks.
	
	- used throughput of certain memory types such as texture memory. In that
	  case the result of performance counter usually represents the number of
	  bytes transferred between GPU and memory.
	
	This extension specifies universal API to manage performance counters on
	different Intel hardware platforms. Performance counters are grouped
	together into proprietary, hardware-specific, fixed sets of counters that
	are measured together by the GPU.
	
	It is assumed that performance counters are started and ended on any
	arbitrary boundaries during rendering. 
	
	A set of performance counters is represented by a unique query type. Each
	query type is identified by assigned name and ID. Multiple query types
	(sets of performance counters) are supported by the Intel hardware. However
	each Intel hardware generation supports different sets of performance
	counters.  Therefore the query types between hardware generations can be
	different. The definition of query types and their results structures can
	be learned through the API. It is also documented in a separate document of
	Intel OGL Performance Counters Specification issued per each new hardware
	generation.
	
	The API allows to create multiple instances of any query type and to sample
	different fragments of 3D rendering with such instances. Query instances
	are identified with handles.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/INTEL/performance_query.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.INTEL.performance_query import *
from OpenGL.raw.GLES2.INTEL.performance_query import _EXTENSION_NAME

def glInitPerformanceQueryINTEL():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# INPUT glGetPerfCounterInfoINTEL.counterDesc size not checked against counterDescLength
# INPUT glGetPerfCounterInfoINTEL.counterName size not checked against counterNameLength
glGetPerfCounterInfoINTEL=wrapper.wrapper(glGetPerfCounterInfoINTEL).setInputArraySize(
    'counterDesc', None
).setInputArraySize(
    'counterName', None
)
# INPUT glGetPerfQueryInfoINTEL.queryName size not checked against queryNameLength
glGetPerfQueryInfoINTEL=wrapper.wrapper(glGetPerfQueryInfoINTEL).setInputArraySize(
    'queryName', None
)
### END AUTOGENERATED SECTION