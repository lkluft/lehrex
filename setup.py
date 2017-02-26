# -*- coding: utf-8 -*-
import sys
from distutils.core import setup
from setuptools import find_packages

from lehrex import __version__

if not sys.version_info >= (3, 5, 1):
    sys.exit('Only support Python version >=3.5.1.\n'
             'Found version is {}'.format(sys.version))

setup(
    name='lehrex',
    author='Lukas Kluft',
    author_email='lukas.kluft@gmail.com',
    url='https://github.com/lkluft/lehrex',
    download_url='https://github.com/lkluft/lehrex/tarball/' + __version__,
    version=__version__,
    packages=find_packages(),
    license='MIT',
    description='Support the research during the Lehrexkursion.',
    classifiers=[
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    include_package_data=True,
    install_requires=[
        'matplotlib>=1.5.1',
        'numpy>=1.10.4',
    ],
)
