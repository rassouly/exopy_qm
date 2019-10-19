#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import os.path
import sys

sys.path.insert(0, os.path.abspath('.'))

PROJECT_NAME = 'exopy_qm'
with open("VERSION", "r") as f:
    version = f.readline()

if len(version) < 1:
    raise Exception("No version specified")

print("Building version {}".format(version))


def long_description():
    """Read the project description from the README file.
    """
    # with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    #     return f.read()
    return ""


setup(
    name=PROJECT_NAME,
    description='QM Exopy package',
    version=version,
    long_description=long_description(),
    author='Michael Greenbaum',
    author_email='michael@quantum-machines.co',
    url="https://quantum-machines.co",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Physics',
        'Programming Language :: Python :: 3.6'
    ],
    zip_safe=False,
    packages=find_packages(exclude=['tests', 'tests.*']),
    data_files=["VERSION"],
    package_data={'': ['*.enaml']},
    requires=['exopy'],
    install_requires=['exopy'],
    entry_points={
        'exopy_package_extension':
        'exopy_qm = %s:list_manifests' % PROJECT_NAME}
)
