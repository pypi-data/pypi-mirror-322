#!/usr/bin/env python

import os
from setuptools import setup, find_packages

def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()

LONG_DESCRIPTION = read_file('README.md')
REQUIRES = read_file('requirements.txt')
EXTRAS = {
    'dev': [
        'mypy'
    ]
}

setup(
    name='pygdk',
    version='1.0.3', # .dev1
    description='Python General Development Kit',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    #url='',
    packages=find_packages(),
    #dependency_links=[],
    include_package_data=True,
    install_requires=REQUIRES,
    extras_require=EXTRAS,
    #python_requires=">=3.10",
    zip_safe=False,
    # setup_requires=['setuptools>=42'],
    license='MIT',
    keywords="GUI,Cross-Platform, Lightweight, Fast",
    project_urls={
        # "Documentation": "",
        "Issue Tracker": "https://github.com/pygdk/pygdk/issues",
        "Source": "https://github.com/pygdk/pygdk",
    },
    platforms=["any"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Multimedia :: Graphics",
    ],
)
