#!/usr/bin/env python

"""
Copyright (c) 2017 pi-top
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
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
    license         = 'Apache 2.0',
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
