from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy as np
import os

os.environ["CC"]= "/usr/local/bin/gcc"
os.environ["CXX"]= "/usr/local/bin/gcc"

setup(
    name='Search',
    packages=['ai'],
    cmdclass = {'build_ext': build_ext},
    ext_modules = [
        Extension("search_better",
            ["search_better.pyx"],
            include_dirs = [np.get_include()])]
)
