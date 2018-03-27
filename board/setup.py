from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy as np
import os

os.environ["CC"]= "/usr/local/bin/gcc"
os.environ["CXX"]= "/usr/local/bin/gcc"

setup(
    name='BitBoard',
    packages=['board'],
    cmdclass = {'build_ext': build_ext},
    ext_modules = [
        Extension("bit_board",
            ["bit_board.pyx"],
            include_dirs = [np.get_include()])]
)
