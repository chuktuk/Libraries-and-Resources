#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""Packaging:

run the following from the terminal in the outer package directory (utility_scripts_package):
(or python for windows)
python3 -m pip install --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel

install the package by navigating to the /dist dir and running the command below,
replacing the Maj.Min.Pat with the major/minor/patch for the version (e.g. 1.0.0)
pip install utility_scripts-Maj.Min.Pat-py3-none-any.whl

"""

import setuptools

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setuptools.setup(
    name='utility_scripts',
    version='1.0.0',
    author='Chuck Tucker',
    author_email='',
    description='Utility Scripts for Simplifying App Development',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/chuktuk/Libraries-and-Resources/utility_scripts_package',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'dash',
        'dash-bootstrap-components',
        'jaydebeapi',
        'pandas',
        'paramiko',
        'pymongo'
    ]
)
