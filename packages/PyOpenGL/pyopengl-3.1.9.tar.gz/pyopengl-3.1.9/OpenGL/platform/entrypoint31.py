"""List of forward-compatible entry points for OpenGL 3.1

Taken from the list at:

    http://www.devklog.net/2008/08/23/forward-compatible-opengl-3-entry-points/
"""
records = """glActiveTexture
glAttachShader
glBeginConditionalRender
glBeginQuery
glBeginTransformFeedback
glBindAttribLocation
glBindBuffer
glBindBufferBase
glBindBufferRange
glBindFragDataLocation
glBindFramebuffer
glBindRenderbuffer
glBindTexture
glBindVertexArray
glBlendColor
glBlendEquation
glBlendEquationSeparate
glBlendFunc
glBlendFuncSeparate
glBlitFramebuffer
glBufferData
glBufferSubData
glCheckFramebufferStatus
glClampColor
glClear
glClearBuffer*
glClearColor
glClearDepth
glClearStencil
glClipPlane
glColorMask*
glCompileShader
glCompressedTexImage*
glCompressedTexSubImage*
glCopyPixels
glCopyTexImage*
glCopyTexSubImage*
glCreateProgram
glCreateShader
glCullFace
glDeleteBuffers
glDeleteFramebuffers
glDeleteProgram
glDeleteQueries
glDeleteRenderbuffers
glDeleteShader
glDeleteTextures
glDeleteVertexArrays
glDepthFunc
glDepthMask
glDepthRange
glDetachShader
glDisable
glDisableVertexAttribArray
glDrawArrays
glDrawBuffer
glDrawBuffers
glDrawElements
glDrawRangeElements
glEnable
glEnableVertexAttribArray
glEndConditionalRender
glEndQuery
glEndTransformFeedback
glFinish
glFlush
glFlushMappedBufferRange
glFramebufferRenderbuffer
glFramebufferTexture*
glFramebufferTextureLayer
glFrontFace
glGenBuffers
glGenerateMipmap
glGenFramebuffers
glGenQueries
glGenRenderbuffers
glGenTextures
glGenVertexArrays
glGetActiveAttrib
glGetActiveUniform
glGetAttachedShaders
glGetAttribLocation
glGetBooleanv
glGetBufferParameter*
glGetBufferPointer*
glGetBufferSubData
glGetClipPlane
glGetCompressedTexImage
glGetDoublev
glGetError
glGetFloatv
glGetFragDataLocation
glGetFramebufferAttachmentParameter*
glGetIntegerv
glGetProgram*
glGetProgramInfoLog
glGetQuery*
glGetQueryObject*
glGetRenderbufferParameter*
glGetShader*
glGetShaderInfoLog
glGetShaderSource
glGetString
glGetTexEnv*
glGetTexImage
glGetTexLevelParameter*
glGetTexParameter*
glGetTransformFeedbackVaryings
glGetUniform*
glGetUniformLocation
glGetVertexAttrib*
glGetVertexAttribIPointer*
glGetVertexAttribPointer*
glHint
glIsBuffer
glIsEnabled
glIsFramebuffer
glIsProgram
glIsQuery
glIsRenderbuffer
glIsShader
glIsTexture
glIsVertexArray
glLineWidth
glLinkProgram
glLogicOp
glMapBuffer
glMapBufferRange
glMultiDrawArrays
glMultiDrawElements
glPixelStore*
glPointParameter*
glPointSize
glPolygonMode
glReadBuffer
glReadPixels
glRenderbufferStorage
glRenderbufferStorageMultisample
glSampleCoverage
glScissor
glShadeModel
glShaderSource
glStencilFunc
glStencilFuncSeparate
glStencilMask
glStencilMaskSeparate
glStencilOp
glStencilOpSeparate
glTexEnv
glTexImage*
glTexParameter*
glTexSubImage*
glTransformFeedbackVaryings
glUniform1*
glUniform2*
glUniform3*
glUniform4*
glUniformMatrix2*
glUniformMatrix2x3*
glUniformMatrix2x4*
glUniformMatrix3*
glUniformMatrix3x2*
glUniformMatrix3x4*
glUniformMatrix4*
glUniformMatrix4x2*
glUniformMatrix4x3*
glUnmapBuffer
glUseProgram
glValidateProgram
glVertexAttrib1*
glVertexAttrib2*
glVertexAttrib3*
glVertexAttrib4*
glVertexAttrib4N*
glVertexAttribI*
glVertexAttribI4
glVertexAttribIPointer
glVertexAttribPointer
glViewport""".splitlines()
def deprecated( name ):
    for allowed in records:
        if name == allowed:
            return False 
        elif allowed.endswith( '*' ) and allowed.startswith(name[:len(allowed)-1]):
            return False 
    return True 