#!/usr/bin/python
from distutils.core import setup, Extension

core_ext = Extension(
    name                = 'core',
    sources             = ['custommatrix/core.cpp'],
    include_dirs        = ['../../include'],
    library_dirs        = ['../../lib'],
    libraries           = ['custommatrix'],
    extra_compile_args  = ["-O3", "-Wall"],
    language            = 'c++'
)

graphics_ext = Extension(
    name                = 'graphics',
    sources             = ['custommatrix/graphics.cpp'],
    include_dirs        = ['../../include'],
    library_dirs        = ['../../lib'],
    libraries           = ['custommatrix'],
    extra_compile_args  = ["-O3", "-Wall"],
    language            = 'c++'
)

setup(
    name                = 'custommatrix',
    version             = '0.0.1',
    author              = 'Christoph Friedrich',
    author_email        = 'christoph.friedrich@vonaffenfels.de',
    classifiers         = ['Development Status :: 3 - Alpha'],
    ext_package         = 'custommatrix',
    ext_modules         = [core_ext, graphics_ext],
    packages            = ['custommatrix']
)
