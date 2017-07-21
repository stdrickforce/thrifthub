# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="thrifthub",
    version="0.1.0",
    description="A pip package",
    license="MIT",
    author="stdrickforce",
    packages=find_packages(),
    install_requires=[
        "thriftpy",
        "requests",
    ],
    long_description=long_description,
    entry_points={
        "console_scripts": {
            "thub = thub.cmd:main",
        }
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)
