# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import io
import json
import os
import subprocess
import imp

from setuptools import find_packages, setup

# Kept manually in sync with version.__version__
version = imp.load_source(
    'spacetimegis.version', os.path.join('spacetimegis', 'version.py')).version

with io.open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='spacetimegis',
    description=('Store, index, query, transform and image-recognition spatio-temporal in HBase、 PostGIS and Spark.'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=['spacetimegis/bin/spacetimegis'],
    install_requires=[
        'alembic',
        'colorama',
        'gunicorn',
        'Flask-Migrate',
        'flask_cors',
        'pathlib2'
    ],
    author='Javy xu',
    author_email='xujavy@gmail.com',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
