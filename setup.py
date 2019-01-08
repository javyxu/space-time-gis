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

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PACKAGE_FILE = os.path.join(BASE_DIR, 'package.json')
with open(PACKAGE_FILE) as package_file:
    version_string = json.load(package_file)['version']

with io.open('README.md', encoding='utf-8') as f:
    long_description = f.read()


def get_git_sha():
    try:
        s = subprocess.check_output(['git', 'rev-parse', 'HEAD'])
        return s.decode().strip()
    except Exception:
        return ''


GIT_SHA = get_git_sha()
version_info = {
    'GIT_SHA': GIT_SHA,
    'version': version_string,
}
print('-==-' * 15)
print('VERSION: ' + version_string)
print('GIT SHA: ' + GIT_SHA)
print('-==-' * 15)

with open(os.path.join(BASE_DIR, 'version_info.json'), 'w') as version_file:
    json.dump(version_info, version_file)


setup(
    name='Framework',
    description=(
        ''),
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=version_string,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    # scripts=['Framework/bin/'],
    install_requires=[
        # 'bleach'
    ],
    # extras_require={
    #     'cors': ['flask-cors>=2.0.0'],
    #     'console_log': ['console_log==0.2.10'],
    # },
    author='Javy xu',
    author_email='xujavy@gmail.com',
    url='',
    # download_url=(
        
    # ),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
