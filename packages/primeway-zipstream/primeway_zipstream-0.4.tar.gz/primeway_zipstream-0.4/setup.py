#!/usr/bin/env python3
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='primeway-zipstream',
    version='0.4',

    description='Creating zip files on the fly',

    author='Lavrenov Nikita',

    license='MIT',

    keywords='zip streaming',
)
