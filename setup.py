#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='pkscan_print_server',
      version='1.0',
      description='Utilities for pkscan',
      author='Himanshu',
      author_email='himansuh.goel86121@gmail.com',
      packages=find_packages(),
      scripts=[
          "pkscan_print_server/bin/pk",
          "pkscan_print_server/bin/pk.bat"
      ],
      install_requires=[
          "pandas",
          "requests",
          "xmltodict",
          "argparse"
      ]
     )
