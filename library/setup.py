#!/usr/bin/env python

"""
Copyright (c) 2017 pi-top
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from os import path
import sys

here = path.abspath(path.dirname(__file__))

if sys.version_info >= (3, 0):
    with open(path.join(here, 'CHANGELOG.txt'), encoding='utf-8') as f:
        long_description = f.read()
else:
    with open(path.join(here, 'CHANGELOG.txt')) as f:
        long_description = f.read()


setup(
    name            = 'ptpulse',
    version         = '0.1.1',
    author          = 'Mike Roberts',
    author_email    = 'mike@pi-top.com',
    description     = """Python library for pi-topPULSE""",
    long_description= long_description,
    license         = 'MIT',
    keywords        = 'pi-top pulse pi-topPULSE Raspberry Pi HAT',
    url             = 'http://pi-top.com',
    classifiers     = ['Development Status :: 5 - Production/Stable',
                       'Operating System :: POSIX :: Linux',
                       'License :: OSI Approved :: MIT License',
                       'Intended Audience :: Developers',
                       'Programming Language :: Python :: 2.7',
                       'Programming Language :: Python :: 3.4',
                       'Topic :: Software Development',
                       'Topic :: System :: Hardware'],
    py_modules      = [ 'ptpulse' ]
)
