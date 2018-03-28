from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

import numpy as np
import os

os.environ["CC"]= "/usr/local/bin/gcc"
os.environ["CXX"]= "/usr/local/bin/gcc"


extensions = [Extension("*", ["*.pyx"], include_dirs = [np.get_include()])]

setup(
    name='Search',
    cmdclass = {'build_ext': build_ext},
    ext_modules = cythonize(extensions)
)
