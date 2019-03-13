# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import io
import json
import os
import subprocess

from setuptools import find_packages, setup

with io.open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='SpacetimeGIS',
    description=(''),
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
    author='Javy xu',
    author_email='xujavy@gmail.com',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
