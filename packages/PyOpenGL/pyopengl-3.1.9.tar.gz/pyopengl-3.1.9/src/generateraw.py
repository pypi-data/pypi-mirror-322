#! /usr/bin/env python
"""Script to generate the raw sub-package APIs

Basically just drives OpenGLGenerator with options to produce
the various modules we want...
"""
import os, sys, logging, re, compileall
import openglgenerator
from OpenGL import platform
try:
    from OpenGL import GL
except (ImportError, AttributeError), err:
    pass

# put our OpenGL directory on the search path, just in case...
sys.path.insert( 0, os.path.abspath( '..' ) )

log = logging.getLogger( 'generateraw' )

MODULE_DEFINITIONS = [
    ('GL', ('gl[A-Z0-9].*','GL_.*')),
    ('GLU',('glu[A-Z0-9].*','GLU[_a-z0-9].*')),
    ('GLUT', ('glut[A-Z0-9].*','GLUT[_a-z0-9].*')),
    ('GLE', None),
    ('GLX', None),
    ('WGL', ('wgl.*','WGL.*',)),
    ('AGL', None),
]
def filterModules( arguments ):
    """Filter the set of modules according to command-line options

    Basically no args == do everything, otherwise only process modules
    declared here...
    """
    if arguments:
        definitions = [
            x for x in MODULE_DEFINITIONS
            if x[0] in arguments
        ]
    else:
        definitions = MODULE_DEFINITIONS
    return definitions

def main():
    baseModules = [
        'OpenGL.constants',
    ]
    known_symbols = openglgenerator.OpenGLGenerator.loadKnownSymbols( 
        baseModules 
    )
    definedSymbols = known_symbols.copy()
    for (module,expressions) in filterModules( sys.argv[1:] ):
        log.info( "Processing module: %s", module )
        if expressions:
            expressions = [re.compile(e) for e in expressions]
        xmlFile = '%s.xml'%( module.lower(), )
        directory = '../OpenGL/raw/%(module)s'%locals()
        try:
            os.makedirs( directory )
        except OSError, err:
            pass
        constantsFile = os.path.join( directory, 'constants.py' )
        rawFile = os.path.join( directory, '__init__.py' )
        open( rawFile, 'w' ).close()
        annotationsFile = os.path.join( directory, 'annotations.py' )
        dll = getattr( platform, module, None )
        if dll and os.path.isfile( xmlFile ):
            log.info( "Found DLL: %s and have XML source file: %s", dll, xmlFile )
            # first the constants file...
            log.info( "Generating constants %s", constantsFile )
            gen = openglgenerator.OpenGLGenerator(
                open(constantsFile,'w'),
                generate_comments = False,
                searched_dlls = [ dll ],
                known_symbols = definedSymbols,
                module_header = '''"""Constants for OpenGL.%(module)s

Automatically generated by the generateraw script, do not edit!
"""
'''%locals(),
            )
            items = gen.load_typedefs( xmlFile , types = [
                openglgenerator.codegenerator.typedesc.Variable, # ick!
            ], expressions = expressions)
            gen.produce( items )
            gen.output.close()
            
            log.info( "Generating raw API %s", rawFile )
            constantSymbols = gen.loadKnownSymbols( 
                ['OpenGL.raw.%(module)s.constants'%locals()], 
                flags = gen.EXPORT_SYMBOL, # don't import, do export
                doReload = True,
            )
            constantSymbols.update( definedSymbols )
            constantSymbols.update( known_symbols )
            gen = openglgenerator.OpenGLGenerator(
                open(rawFile,'w'),
                generate_comments = True,
                searched_dlls = [ dll ],
                known_symbols = constantSymbols,
                module_header = '''# -*- coding: iso-8859-1 -*-
"""Raw (C-style) API for OpenGL.%(module)s

Automatically generated by the generateraw script, do not edit!
"""
from OpenGL.raw.%(module)s.constants import *
'''%locals(),
            )
            items = gen.load_typedefs( xmlFile, expressions = expressions )
            gen.produce( items )
            gen.output.close()

            log.info( "Generating annotations %s", annotationsFile )
            gen = openglgenerator.OpenGLGenerator(
                open(annotationsFile,'w'),
                generate_comments = True,
                searched_dlls = [ dll ],
                emitters = [ openglgenerator.OpenGLDecorator() ],
                known_symbols = definedSymbols,
                module_header = '''"""Array-size annotations for OpenGL.raw.%(module)s

Automatically generated by the generateraw script, do not edit!
"""
from OpenGL.raw import %(module)s as raw
'''%locals(),
            )
            items = gen.load_typedefs( xmlFile, types = [
                openglgenerator.codegenerator.typedesc.Function, # ick!
            ], expressions = expressions)
            gen.produce( items )
            gen.output.close()

            log.info( """Suppressing future output of already-defined functions/structures: %s""", module )
            definedSymbols.update( 
                gen.loadKnownSymbols( 
                    ['OpenGL.raw.%(module)s'%locals()], 
                    flags = 0, # neither import nor export from future operations...
                    doReload = True,
                )
            )
            definedSymbols.update( 
                gen.loadKnownSymbols( 
                    ['OpenGL.raw.%(module)s.constants'%locals()], 
                    flags = 0, # suppress future export of the constants
                    doReload = True,
                ) 
            )
            definedSymbols.update( known_symbols )
            if module == 'GL':
                # filter out the higher GL version stuff as well...
                # obviously you need to have the version stuff generated already 
                # to make this work!
                for version in ('1_2','1_3','1_4','1_5','2_0'):
                    log.info( 'Suppressing exports from Core GL Version %s', version )
                    definedSymbols.update( 
                        gen.loadKnownSymbols( 
                            ['OpenGL.raw.GL.VERSION.GL_%(version)s'%locals()], 
                            flags = 0, # suppress future export of the constants
                            doReload = True,
                        ) 
                    )
            path = '../OpenGL/raw/%(module)s'%locals()
            log.info( 'Forcing recompilation of %s', path )
            compileall.compile_dir(path, maxlevels=2, force=True, quiet=True)
    

if __name__ == "__main__":
    logging.basicConfig()
    #logging.getLogger( 'codegenerator' ).setLevel( logging.DEBUG )
    log.setLevel( logging.INFO )
    main()
